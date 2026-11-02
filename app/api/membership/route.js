import { NextResponse } from 'next/server'
import Stripe from 'stripe'
import { supabaseAdmin as supabase, getUserFromReq, notify } from '../../lib/server'

// Member actions on their own membership: pause, resume (end a pause early, or cancel a booked pause),
// cancel (at the end of the paid month) and undo_cancel.
// Rules (Christine, 2 Nov 2026): pause 1-3 months from the next payment date; at most 3 months in a membership year;
// no booking while paused; payments restart automatically; resume early = payment taken that day.

function ymd(d) { return d.toISOString().slice(0, 10) }
function addMonths(d, n) { const x = new Date(d.getTime()); x.setUTCMonth(x.getUTCMonth() + n); return x }
function nice(s) { return new Date(s + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) }

export async function POST(req) {
  try {
    const user = await getUserFromReq(req)
    if (!user) return NextResponse.json({ error: 'Please sign in.' }, { status: 401 })
    const { action, months } = await req.json()

    const { data: client } = await supabase.from('clients').select('id, full_name, email').ilike('email', user.email).maybeSingle()
    if (!client) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })
    const { data: m } = await supabase.from('memberships').select('*')
      .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
    if (!m || !m.stripe_sub_id) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    const today = ymd(new Date())
    const { data: ben } = await supabase.rpc('membership_benefits', { p_membership: m.id })
    const info = { clientName: client.full_name || client.email, clientEmail: client.email }

    if (action === 'pause') {
      const n = Number(months)
      if (![1, 2, 3].includes(n)) return NextResponse.json({ error: 'Choose 1, 2 or 3 months.' }, { status: 400 })
      if (m.status !== 'active') return NextResponse.json({ error: 'Your membership needs to be active to pause.' }, { status: 403 })
      if (m.cancel_at) return NextResponse.json({ error: 'Your membership is set to cancel, so it cannot be paused.' }, { status: 409 })
      if (m.pending_package) return NextResponse.json({ error: 'You have a package change booked. Please cancel it before pausing.' }, { status: 409 })
      if (ben?.pause) return NextResponse.json({ error: 'You already have a pause booked.' }, { status: 409 })
      if ((ben?.pause_months_left ?? 0) < n) {
        return NextResponse.json({ error: `You can pause for up to 3 months in each membership year. You have ${ben?.pause_months_left ?? 0} month(s) left this year.` }, { status: 409 })
      }
      const sub = await stripe.subscriptions.retrieve(m.stripe_sub_id)
      const periodEnd = sub.items?.data?.[0]?.current_period_end || sub.current_period_end
      const start = new Date(periodEnd * 1000)            // next payment date: first skipped payment
      const end = addMonths(start, n)                     // payments restart on this date
      // Collection resumes just before the restart date so that day's payment is taken.
      await stripe.subscriptions.update(sub.id, { pause_collection: { behavior: 'void', resumes_at: Math.floor(end.getTime() / 1000) - 3600 } })
      const { error } = await supabase.from('membership_pauses').insert({
        membership_id: m.id, client_id: client.id, starts_on: ymd(start), ends_on: ymd(end), months: n, status: 'scheduled',
      })
      if (error) throw error
      await notify(req, 'membership_paused', { ...info, from: nice(ymd(start)), until: nice(ymd(end)), months: String(n) })
      return NextResponse.json({ success: true, starts_on: ymd(start), ends_on: ymd(end) })
    }

    if (action === 'resume') {
      const p = ben?.pause
      if (!p) return NextResponse.json({ error: 'You do not have a pause booked.' }, { status: 409 })
      if (!p.started) {
        // Pause hasn't started yet: simply cancel it. Nothing changes with payments.
        await stripe.subscriptions.update(m.stripe_sub_id, { pause_collection: '' })
        await supabase.from('membership_pauses').update({ status: 'cancelled', updated_at: new Date().toISOString() }).eq('id', p.id)
        return NextResponse.json({ success: true, cancelled_pause: true })
      }
      // Ending a pause early: restart payments today (full monthly price, new payment date from today).
      await stripe.subscriptions.update(m.stripe_sub_id, { pause_collection: '', billing_cycle_anchor: 'now', proration_behavior: 'none' })
      await supabase.from('membership_pauses').update({ status: 'ended', ends_on: today, updated_at: new Date().toISOString() }).eq('id', p.id)
      await notify(req, 'membership_resumed', info)
      return NextResponse.json({ success: true, resumed: true })
    }

    if (action === 'cancel') {
      if (!['active', 'pending'].includes(m.status)) return NextResponse.json({ error: 'This membership cannot be cancelled online. Please contact the salon.' }, { status: 409 })
      const sub = await stripe.subscriptions.retrieve(m.stripe_sub_id)
      // A booked package change (schedule) must be released before the subscription can be set to cancel.
      const schedId = typeof sub.schedule === 'string' ? sub.schedule : sub.schedule?.id
      if (schedId) await stripe.subscriptionSchedules.release(schedId)
      const updated = await stripe.subscriptions.update(sub.id, { cancel_at_period_end: true, pause_collection: '' })
      const endTs = updated.items?.data?.[0]?.current_period_end || updated.current_period_end
      const endsOn = ymd(new Date(endTs * 1000))
      await supabase.from('memberships').update({ cancel_at: endsOn, pending_package: null, pending_package_from: null }).eq('id', m.id)
      await supabase.from('membership_pauses').update({ status: 'cancelled' }).eq('membership_id', m.id).eq('status', 'scheduled').gt('starts_on', today)
      await notify(req, 'membership_cancelled', { ...info, until: nice(endsOn) })
      return NextResponse.json({ success: true, cancel_at: endsOn })
    }

    if (action === 'undo_cancel') {
      if (!m.cancel_at) return NextResponse.json({ error: 'Your membership is not set to cancel.' }, { status: 409 })
      await stripe.subscriptions.update(m.stripe_sub_id, { cancel_at_period_end: false })
      await supabase.from('memberships').update({ cancel_at: null }).eq('id', m.id)
      return NextResponse.json({ success: true })
    }

    return NextResponse.json({ error: 'Unknown action.' }, { status: 400 })
  } catch (err) {
    console.error('membership action error', err)
    return NextResponse.json({ error: 'Something went wrong. Please try again or contact the salon.' }, { status: 500 })
  }
}
