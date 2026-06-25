import Stripe from 'stripe'
import { NextResponse } from 'next/server'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)

const PRICE_IDS = {
  essential: process.env.NEXT_PUBLIC_STRIPE_PRICE_ESSENTIAL,
  signature:  process.env.NEXT_PUBLIC_STRIPE_PRICE_SIGNATURE,
  elite:      process.env.NEXT_PUBLIC_STRIPE_PRICE_ELITE,
}

export async function POST(req) {
  try {
    const { package: pkg, email, name } = await req.json()

    const priceId = PRICE_IDS[pkg]
    if (!priceId) {
      return NextResponse.json({ error: 'Invalid package' }, { status: 400 })
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      customer_email: email,
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.NEXT_PUBLIC_APP_URL || 'https://chris2styles.co.uk'}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url:  `${process.env.NEXT_PUBLIC_APP_URL || 'https://chris2styles.co.uk'}`,
      metadata: { name, package: pkg },
    })

    return NextResponse.json({ url: session.url })
  } catch (err) {
    console.error('Checkout error:', err)
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}
