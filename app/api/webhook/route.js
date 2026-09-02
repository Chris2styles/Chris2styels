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

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object
    const { name, package: pkg } = session.metadata || {}
    const email = session.customer_email

    let { data: existing } = await supabase
      .from('clients')
      .select('id')
      .eq('email', email)
      .single()

    let clientId = existing?.id

    if (!clientId) {
      const { data: newClient } = await supabase
        .from('clients')
        .insert({ full_name: name || email, email })
        .select('id')
        .single()
      clientId = newClient?.id
    }

    if (clientId) {
      await supabase.from('memberships').insert({
        client_id: clientId,
        package: pkg || 'essential',
        status: 'active',
        stripe_customer_id: session.customer,
        stripe_sub_id: session.subscription,
        sessions_used: 0,
        sessions_total: pkg === 'essential' ? 0 : 1,
      })
    }
  }

  if (event.type === 'invoice.payment_failed') {
    const invoice = event.data.object
    await supabase
      .from('memberships')
      .update({ status: 'payment_failed' })
      .eq('stripe_customer_id', invoice.customer)
  }

  if (event.type === 'invoice.paid') {
    const invoice = event.data.object
    const { data: m } = await supabase
      .from('memberships')
      .select('package')
      .eq('stripe_customer_id', invoice.customer)
      .single()
    if (m) {
      await supabase
        .from('memberships')
        .update({ status: 'active', sessions_used: 0, sessions_total: m.package === 'essential' ? 0 : 1 })
        .eq('stripe_customer_id', invoice.customer)
    }
  }

  return NextResponse.json({ received: true })
}