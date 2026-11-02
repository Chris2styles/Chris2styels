import { NextResponse } from 'next/server'

export async function POST(req) {
  try {
    const Stripe = (await import('stripe')).default
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    const PRICE_IDS = {
      essential: process.env.NEXT_PUBLIC_STRIPE_PRICE_ESSENTIAL,
      signature: process.env.NEXT_PUBLIC_STRIPE_PRICE_SIGNATURE,
      elite: process.env.NEXT_PUBLIC_STRIPE_PRICE_ELITE,
    }
    const { package: pkg, email, name, payDay } = await req.json()
    // Emergency off-switch: set ELITE_SALES_ENABLED=false in Netlify to pause Elite sales.
    if (pkg === 'elite' && process.env.ELITE_SALES_ENABLED === 'false') {
      return NextResponse.json({ error: 'Elite membership is coming soon. Please contact the salon to register your interest.' }, { status: 403 })
    }
    const priceId = PRICE_IDS[pkg]
    if (!priceId) {
      return NextResponse.json({ error: 'Invalid package' }, { status: 400 })
    }
    // Chosen payment date (1st-28th). If it isn't today, nothing is charged now: the first full payment is taken on
    // that date and the membership starts then (Stripe billing_cycle_anchor with no proration).
    let startOn = null
    const subscription_data = { metadata: { package: pkg } }
    const day = Number(payDay)
    if (Number.isInteger(day) && day >= 1 && day <= 28) {
      const now = new Date()
      const today = now.getUTCDate()
      if (day !== today) {
        const y = now.getUTCFullYear(), m = now.getUTCMonth() + (day < today ? 1 : 0)
        const anchor = new Date(Date.UTC(y, m, day, 9, 0, 0)) // 9am UK time on the chosen day
        startOn = anchor.toISOString().slice(0, 10)
        subscription_data.billing_cycle_anchor = Math.floor(anchor.getTime() / 1000)
        subscription_data.proration_behavior = 'none'
        subscription_data.metadata.start_on = startOn
      }
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      customer_email: email,
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: 'https://chris2styles.co.uk/success' + (startOn ? '?start=' + startOn : ''),
      cancel_url: 'https://chris2styles.co.uk',
      subscription_data,
      metadata: { name, package: pkg, ...(startOn ? { start_on: startOn } : {}) },
    })
    return NextResponse.json({ url: session.url })
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}
