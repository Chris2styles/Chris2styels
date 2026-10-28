// Shared server-only helpers. Never import this file from browser code.
import { createClient } from '@supabase/supabase-js'

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY,
  { auth: { persistSession: false } }
)

// Which package each Stripe price belongs to. Includes the original £69 Essential price that existing members keep.
export const LEGACY_PRICE_PACKAGE = { price_1U3fH3CQkQsronIFf170dIQy: 'essential' }
export function packageForPrice(priceId) {
  if (!priceId) return null
  const map = {
    ...LEGACY_PRICE_PACKAGE,
    [process.env.NEXT_PUBLIC_STRIPE_PRICE_ESSENTIAL]: 'essential',
    [process.env.NEXT_PUBLIC_STRIPE_PRICE_SIGNATURE]: 'signature',
    [process.env.NEXT_PUBLIC_STRIPE_PRICE_ELITE]: 'elite',
  }
  return map[priceId] || null
}

// Elite monthly styling credit (GBP). Change here only.
export const ELITE_MONTHLY_CREDIT = 30

// Services each package may book. Keep in sync with SVCMAP in HHCApp.jsx.
export const SERVICES = {
  essential: ['Quarterly Maintenance', 'Priority Appointment', 'Consultation', 'Basic Styling', 'Sustenance Treatment', 'Olaplex Treatment', 'K18 Treatment'],
  signature: ['Monthly Maintenance', 'Wash and Treatment', 'Sustenance Treatment', 'Olaplex Treatment', 'K18 Treatment', 'Scalp Care', 'Basic Styling', 'Braids', 'Wig Install', 'Priority Appointment'],
  elite: ['Monthly Maintenance', 'Wash and Treatment', 'Sustenance Treatment', 'Olaplex Treatment', 'K18 Treatment', 'Scalp Care', 'Basic Styling', 'Braids', 'Wig Install', 'Premium Styling', 'Priority Appointment', 'Consultation', 'Birthday Glam'],
}

// Returns the signed-in Supabase user from the "Authorization: Bearer <token>" header, or null.
export async function getUserFromReq(req) {
  const auth = req.headers.get('authorization') || ''
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : null
  if (!token) return null
  const { data, error } = await supabaseAdmin.auth.getUser(token)
  if (error) return null
  return data.user || null
}

export async function isAdmin(email) {
  if (!email) return false
  const { data } = await supabaseAdmin.from('admin_users').select('email').eq('email', email).maybeSingle()
  return !!data
}

// Server-to-server calls to /api/notify carry this header so client-facing emails can't be triggered by the public.
export function internalHeaders() {
  return { 'Content-Type': 'application/json', 'x-internal-key': process.env.SUPABASE_SECRET_KEY }
}

export function appUrl(req) {
  return process.env.NEXT_PUBLIC_APP_URL || (req ? new URL(req.url).origin : 'https://chris2styles.co.uk')
}

export async function notify(req, type, data) {
  try {
    await fetch(`${appUrl(req)}/api/notify`, { method: 'POST', headers: internalHeaders(), body: JSON.stringify({ type, data }) })
  } catch (e) {
    console.error('notify failed', type, e)
  }
}
