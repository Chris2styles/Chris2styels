import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY
)

export async function POST(req) {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')

  let event
  try {
    const Stripe = (await import('stripe')).default
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET)
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 400 })
  }

  // DUPLICATE PROTECTION - check if event already processed
  const { data: existing } = await supabase
    .from('processed_events')
    .select('id')
    .eq('stripe_event_id', event.id)
    .single()

  if (existing) {
    return NextResponse.json({ received: true, duplicate: true })
  }

  // Mark event as processed
  await supabase.from('processed_events').insert({ stripe_event_id: event.id })

  // CHECKOUT COMPLETED - create member
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object
    const { name, package: pkg } = session.metadata || {}
    const email = session.customer_email

    let { data: clients } = await supabase.from('clients').select('*')
    let client = clients && clients.find(c => c.email === email)
    let clientId = client?.id

    if (!clientId) {
      const { data: newClient } = await supabase
        .from('clients')
        .insert({ full_name: name || email, email })
        .select('id')
        .single()
      clientId = newClient?.id
    }

    if (clientId) {
      const sessions = pkg === 'essential' ? 0 : 1
      const credit = pkg === 'elite' ? 30 : 0
      const creditExpiry = new Date()
      creditExpiry.setMonth(creditExpiry.getMonth() + 1)

      await supabase.from('memberships').insert({
        client_id: clientId,
        package: pkg || 'essential',
        status: 'active',
        stripe_customer_id: session.customer,
        stripe_sub_id: session.subscription,
        sessions_used: 0,
        sessions_total: sessions,
        style_credit: credit,
      })
    }
  }

     // PAYMENT FAILED
  if (event.type === 'invoice.payment_failed') {
    const invoice = event.data.object
    await supabase
      .from('memberships')
      .update({ status: 'payment_failed' })
      .eq('stripe_customer_id', invoice.customer)
    // Notify client and admin
    const { data: clients } = await supabase.from('clients').select('*')
    const client = clients && clients.find(c => {
      return supabase.from('memberships').select('client_id').eq('stripe_customer_id', invoice.customer)
    })
    try {
      await fetch(`${process.env.NEXT_PUBLIC_APP_URL || 'https://chris2styles.co.uk'}/api/notify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'payment_failed', data: { clientEmail: invoice.customer_email || '', clientName: 'Member' } })
      })
    } catch(e) { console.log('Notify error:', e) }
  }

  // PAYMENT SUCCEEDED - renewal
  if (event.type === 'invoice.paid') {
    const invoice = event.data.object
    const { data: m } = await supabase
      .from('memberships')
      .select('package')
      .eq('stripe_customer_id', invoice.customer)
      .single()

    if (m) {
      const sessions = m.package === 'essential' ? 0 : 1
      const credit = m.package === 'elite' ? 30 : 0
      await supabase
        .from('memberships')
        .update({ 
          status: 'active', 
          sessions_used: 0, 
          sessions_total: sessions,
          style_credit: credit,
        })
        .eq('stripe_customer_id', invoice.customer)
    }
  }

  // SUBSCRIPTION CANCELLED
  if (event.type === 'customer.subscription.deleted') {
    const sub = event.data.object
    await supabase
      .from('memberships')
      .update({ status: 'cancelled' })
      .eq('stripe_sub_id', sub.id)
  }

  return NextResponse.json({ received: true })
}