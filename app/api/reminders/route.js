import { NextResponse } from 'next/server'
import { supabaseAdmin as supabase, notify } from '../../lib/server'

// Sends appointment reminders about 24 hours before each confirmed booking.
// Called every hour by the scheduled Netlify function (netlify/functions/send-reminders.mjs).
// Email always; a text too when Twilio is set up (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM).

export const dynamic = 'force-dynamic'

const SALON_PHONE = '020 3754 7889'

// London wall-clock date+time -> real Date (handles GMT/BST).
function londonToDate(date, time) {
  const [y, mo, d] = date.split('-').map(Number)
  const [h, mi] = String(time).split(':').map(Number)
  const guess = Date.UTC(y, mo - 1, d, h, mi)
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).formatToParts(new Date(guess))
  const g = Object.fromEntries(parts.map(p => [p.type, p.value]))
  return new Date(guess - (Date.UTC(+g.year, +g.month - 1, +g.day, +g.hour, +g.minute) - guess))
}
const niceTime = t => { const [h, m] = String(t).split(':').map(Number); return `${h % 12 || 12}${m ? ':' + String(m).padStart(2, '0') : ''}${h < 12 ? 'am' : 'pm'}` }
const niceDate = d => new Date(d + 'T12:00:00Z').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'Europe/London' })
const londonDay = dt => dt.toLocaleDateString('en-GB', { timeZone: 'Europe/London' })

function ukMobile(p) {
  let d = String(p || '').replace(/\D/g, '')
  if (d.startsWith('0044')) d = d.slice(2)
  if (d.startsWith('44')) d = '0' + d.slice(2)
  if (d.length === 10 && d.startsWith('7')) d = '0' + d
  return /^07\d{9}$/.test(d) ? '+44' + d.slice(1) : null
}

async function sendSms(to, body) {
  const sid = process.env.TWILIO_ACCOUNT_SID, token = process.env.TWILIO_AUTH_TOKEN, from = process.env.TWILIO_FROM
  if (!sid || !token || !from) return { skipped: true }
  const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${sid}/Messages.json`, {
    method: 'POST',
    headers: { Authorization: 'Basic ' + Buffer.from(`${sid}:${token}`).toString('base64'), 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ To: to, From: from, Body: body }),
  })
  if (!res.ok) { const e = await res.json().catch(() => ({})); return { error: (e.message || 'Twilio error ' + res.status).slice(0, 300) } }
  return { ok: true }
}

async function run(req, { dryRun = false } = {}) {
  const now = new Date()
  const today = now.toISOString().slice(0, 10)
  const inTwoDays = new Date(now.getTime() + 2 * 86400000).toISOString().slice(0, 10)
  const { data: rows, error } = await supabase.from('bookings')
    .select('id, service, booking_date, booking_time, status, reminder_email_at, reminder_sms_at, clients(full_name, email, phone)')
    .eq('status', 'confirmed').gte('booking_date', today).lte('booking_date', inTwoDays)
  if (error) throw error

  const out = []
  for (const b of rows || []) {
    if (!b.booking_date || !b.booking_time || !b.clients) continue
    const start = londonToDate(b.booking_date, b.booking_time)
    const hoursAway = (start - now) / 3600000
    // Due once the appointment is 24 hours (or less) away, and still at least 1 hour in the future.
    if (hoursAway > 24 || hoursAway < 1) continue
    const first = (b.clients.full_name || '').split(' ')[0] || 'there'
    const when = londonDay(start) === londonDay(now) ? 'today' : 'tomorrow'
    const time = niceTime(b.booking_time)
    const item = { booking: b.id, when, time }

    if (!b.reminder_email_at && b.clients.email) {
      if (!dryRun) {
        await notify(req, 'appointment_reminder', { clientName: first, clientEmail: b.clients.email, service: b.service || 'Appointment', date: niceDate(b.booking_date), time, when })
        await supabase.from('bookings').update({ reminder_email_at: new Date().toISOString() }).eq('id', b.id)
      }
      item.email = true
    }
    const to = ukMobile(b.clients.phone)
    if (!b.reminder_sms_at && to) {
      const body = `Hi ${first}, a reminder of your Healthy Hair Club appointment ${when} at ${time} at Chris 2 Styles Salon, 87 Mitcham Lane SW16. To change it, please call ${SALON_PHONE}. See you soon!`
      if (!dryRun) {
        const r = await sendSms(to, body)
        if (r.ok) await supabase.from('bookings').update({ reminder_sms_at: new Date().toISOString(), reminder_sms_error: null }).eq('id', b.id)
        else if (r.error) await supabase.from('bookings').update({ reminder_sms_error: r.error }).eq('id', b.id)
        item.sms = r.ok ? true : r.skipped ? 'not set up yet' : 'failed'
      } else item.sms = 'would send'
    }
    out.push(item)
  }
  return out
}

export async function POST(req) {
  const ok = process.env.SUPABASE_SECRET_KEY && req.headers.get('x-internal-key') === process.env.SUPABASE_SECRET_KEY
  if (!ok) return NextResponse.json({ error: 'Not allowed' }, { status: 403 })
  try {
    const { dryRun } = await req.json().catch(() => ({}))
    const sent = await run(req, { dryRun: !!dryRun })
    return NextResponse.json({ success: true, sent })
  } catch (e) {
    console.error('reminders error', e)
    return NextResponse.json({ error: 'Reminder run failed' }, { status: 500 })
  }
}
