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
    const { package: pkg, email, name } = await req.json()
    // Emergency off-switch: set ELITE_SALES_ENABLED=false in Netlify to pause Elite sales.
    if (pkg === 'elite' && process.env.ELITE_SALES_ENABLED === 'false') {
      return NextResponse.json({ error: 'Elite membership is coming soon. Please contact the salon to register your interest.' }, { status: 403 })
    }
    const priceId = PRICE_IDS[pkg]
    if (!priceId) {
      return NextResponse.json({ error: 'Invalid package' }, { status: 400 })
    }
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      customer_email: email,
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: 'https://chris2styles.co.uk/success',
      cancel_url: 'https://chris2styles.co.uk',
      metadata: { name, package: pkg },
    })
    return NextResponse.json({ url: session.url })
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}
