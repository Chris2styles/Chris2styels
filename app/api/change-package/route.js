import { NextResponse } from 'next/server'
import Stripe from 'stripe'
import { supabaseAdmin as supabase, getUserFromReq, notify, packageForPrice } from '../../lib/server'

const NAMES = { essential: 'Essential', signature: 'Signature', elite: 'Elite' }

function priceFor(pkg) {
  return {
    essential: process.env.NEXT_PUBLIC_STRIPE_PRICE_ESSENTIAL,
    signature: process.env.NEXT_PUBLIC_STRIPE_PRICE_SIGNATURE,
    elite: process.env.NEXT_PUBLIC_STRIPE_PRICE_ELITE,
  }[pkg]
}

// A member changes (or cancels a change to) their package themselves.
// The change is scheduled in Stripe for their next payment date: until then they keep their current package;
// on that date Stripe charges the new price and the webhook switches the package in the app.
export async function POST(req) {
  try {
    const user = await getUserFromReq(req)
    if (!user) return NextResponse.json({ error: 'Please sign in.' }, { status: 401 })
    const { package: wanted } = await req.json()
    if (!NAMES[wanted]) return NextResponse.json({ error: 'Please choose a package.' }, { status: 400 })
    if (wanted === 'elite' && process.env.ELITE_SALES_ENABLED === 'false') {
      return NextResponse.json({ error: 'Elite is not available to join at the moment. Please contact the salon.' }, { status: 403 })
    }

    const { data: client } = await supabase.from('clients').select('id, full_name, email').ilike('email', user.email).maybeSingle()
    if (!client) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })
    const { data: m } = await supabase.from('memberships').select('*')
      .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
    if (!m || !m.stripe_sub_id) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })
    if (m.cancel_at) return NextResponse.json({ error: 'Your membership is set to cancel. Keep your membership first to change package.' }, { status: 409 })
    const { data: ben } = await supabase.rpc('membership_benefits', { p_membership: m.id })
    if (ben?.pause) return NextResponse.json({ error: 'You have a pause booked. Please end or cancel your pause before changing package.' }, { status: 409 })
    if (!['active', 'pending'].includes(m.status)) {
      return NextResponse.json({ error: 'Your membership needs to be active to change package. Please contact the salon.' }, { status: 403 })
    }

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    const sub = await stripe.subscriptions.retrieve(m.stripe_sub_id)
    const currentPrice = sub.items.data[0].price.id
    const currentPkg = packageForPrice(currentPrice) || m.package

    // Find or create the schedule that controls this subscription.
    const schedId = typeof sub.schedule === 'string' ? sub.schedule : sub.schedule?.id
    let schedule = schedId ? await stripe.subscriptionSchedules.retrieve(schedId) : null

    // Choosing the package they already have = cancel any scheduled change.
    if (wanted === currentPkg) {
      if (schedule && schedule.status !== 'released' && schedule.status !== 'canceled') await stripe.subscriptionSchedules.release(schedule.id)
      await supabase.from('memberships').update({ pending_package: null, pending_package_from: null }).eq('id', m.id)
      return NextResponse.json({ success: true, cancelled: true })
    }

    if (!schedule || schedule.status === 'released' || schedule.status === 'canceled') {
      schedule = await stripe.subscriptionSchedules.create({ from_subscription: sub.id })
    }
    const now = Math.floor(Date.now() / 1000)
    const current = schedule.phases.find(p => p.start_date <= now && now < p.end_date) || schedule.phases[0]
    const switchAt = current.end_date // the next payment date
    await stripe.subscriptionSchedules.update(schedule.id, {
      end_behavior: 'release',
      phases: [
        { items: [{ price: currentPrice, quantity: 1 }], start_date: current.start_date, end_date: switchAt, proration_behavior: 'none' },
        { items: [{ price: priceFor(wanted), quantity: 1 }], duration: { interval: 'month', interval_count: 1 }, proration_behavior: 'none' },
      ],
    })

    const from = new Date(switchAt * 1000).toISOString().slice(0, 10)
    await supabase.from('memberships').update({ pending_package: wanted, pending_package_from: from }).eq('id', m.id)

    await notify(req, 'package_change_requested', {
      clientName: client.full_name || client.email,
      clientEmail: client.email,
      from: NAMES[currentPkg],
      to: NAMES[wanted],
      date: new Date(switchAt * 1000).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }),
    })
    return NextResponse.json({ success: true, package: wanted, from })
  } catch (err) {
    console.error('change-package error', err)
    return NextResponse.json({ error: 'We could not change your package just now. Please try again or contact the salon.' }, { status: 500 })
  }
}
