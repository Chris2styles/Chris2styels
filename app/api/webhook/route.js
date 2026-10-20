import { NextResponse } from 'next/server'
import Stripe from 'stripe'
import { supabaseAdmin as supabase, ELITE_MONTHLY_CREDIT, notify } from '../../lib/server'

const SESSIONS = { essential: 0, signature: 1, elite: 1 }

function subIdOf(invoice) {
  return invoice.subscription
    || invoice.parent?.subscription_details?.subscription
    || invoice.lines?.data?.[0]?.parent?.subscription_item_details?.subscription
    || invoice.lines?.data?.[0]?.subscription
    || null
}

function periodOf(invoice) {
  const p = invoice.lines?.data?.[0]?.period
  if (!p) return {}
  return {
    current_period_start: new Date(p.start * 1000).toISOString(),
    current_period_end: new Date(p.end * 1000).toISOString(),
  }
}

async function membershipForSub(subId) {
  if (!subId) return null
  const { data } = await supabase.from('memberships').select('*, clients(full_name,email)').eq('stripe_sub_id', subId).maybeSingle()
  return data
}

class RetryLater extends Error {}

async function handleCheckoutCompleted(session) {
  if (session.mode !== 'subscription' || !session.subscription) return
  const existing = await membershipForSub(session.subscription)
  if (existing) return

  const { name, package: pkgRaw } = session.metadata || {}
  const pkg = ['essential', 'signature', 'elite'].includes(pkgRaw) ? pkgRaw : 'essential'
  const email = (session.customer_email || session.customer_details?.email || '').toLowerCase()
  if (!email) throw new Error('checkout session has no email')

  let { data: client } = await supabase.from('clients').select('id').ilike('email', email).maybeSingle()
  if (!client) {
    const { data, error } = await supabase.from('clients').insert({ full_name: name || email, email }).select('id').single()
    if (error) throw error
    client = data
  }

  const { error } = await supabase.from('memberships').insert({
    client_id: client.id,
    package: pkg,
    status: 'active',
    stripe_customer_id: session.customer,
    stripe_sub_id: session.subscription,
    sessions_used: 0,
    sessions_total: SESSIONS[pkg],
    style_credit: 0, // credit is only ever added from a paid invoice (see invoice.paid)
  })
  if (error) throw error
}

async function handleInvoicePaid(req, invoice) {
  const subId = subIdOf(invoice)
  if (!subId) return // not a membership invoice
  const m = await membershipForSub(subId)
  // invoice.paid can arrive before checkout.session.completed; ask Stripe to retry shortly.
  if (!m) throw new RetryLater('membership not created yet for ' + subId)

  await supabase.from('payments').upsert({
    client_id: m.client_id,
    membership_id: m.id,
    stripe_payment_id: invoice.id,
    amount: (invoice.amount_paid || 0) / 100,
    currency: invoice.currency || 'gbp',
    status: 'paid',
  }, { onConflict: 'stripe_payment_id' })

  const qualifying = (invoice.amount_paid || 0) > 0 && ['subscription_create', 'subscription_cycle'].includes(invoice.billing_reason)
  if (!qualifying) return

  const wasFailed = m.status === 'payment_failed'
  const { error } = await supabase.from('memberships').update({
    status: 'active',
    sessions_used: 0,
    sessions_total: SESSIONS[m.package] ?? 0,
    ...periodOf(invoice),
  }).eq('id', m.id)
  if (error) throw error

  if (m.package === 'elite') {
    // Database guarantees one credit per invoice, even if Stripe sends this event twice.
    const { error: cErr } = await supabase.rpc('issue_elite_credit', { p_membership: m.id, p_invoice: invoice.id, p_amount: ELITE_MONTHLY_CREDIT })
    if (cErr) throw cErr
  }

  if (wasFailed && m.clients?.email) {
    await notify(req, 'payment_restored', { clientEmail: m.clients.email, clientName: m.clients.full_name })
  }
}

async function handlePaymentFailed(req, invoice) {
  const m = await membershipForSub(subIdOf(invoice))
  if (!m) return
  await supabase.from('memberships').update({ status: 'payment_failed' }).eq('id', m.id)
  await supabase.from('payments').upsert({
    client_id: m.client_id, membership_id: m.id, stripe_payment_id: invoice.id,
    amount: (invoice.amount_due || 0) / 100, currency: invoice.currency || 'gbp', status: 'failed',
  }, { onConflict: 'stripe_payment_id' })
  await notify(req, 'payment_failed', {
    clientEmail: m.clients?.email || invoice.customer_email || '',
    clientName: m.clients?.full_name || 'Member',
  })
}

async function handleSubscriptionDeleted(sub) {
  await supabase.from('memberships').update({ status: 'cancelled' }).eq('stripe_sub_id', sub.id)
}

export async function POST(req) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')

  let event
  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET)
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  // Duplicate protection: claiming the event id is atomic, so two copies can't both get through.
  const { data: claimed, error: claimErr } = await supabase
    .from('processed_events')
    .upsert({ stripe_event_id: event.id }, { onConflict: 'stripe_event_id', ignoreDuplicates: true })
    .select('id')
  if (claimErr) return NextResponse.json({ error: 'db unavailable' }, { status: 500 })
  if (!claimed || claimed.length === 0) return NextResponse.json({ received: true, duplicate: true })

  try {
    switch (event.type) {
      case 'checkout.session.completed': await handleCheckoutCompleted(event.data.object); break
      case 'invoice.paid': await handleInvoicePaid(req, event.data.object); break
      case 'invoice.payment_failed': await handlePaymentFailed(req, event.data.object); break
      case 'customer.subscription.deleted': await handleSubscriptionDeleted(event.data.object); break
      default: break
    }
  } catch (err) {
    // Release the claim so Stripe's automatic retry is processed properly.
    await supabase.from('processed_events').delete().eq('stripe_event_id', event.id)
    console.error('webhook error', event.type, event.id, err)
    return NextResponse.json({ error: 'processing failed, will retry' }, { status: 500 })
  }

  return NextResponse.json({ received: true })
}
