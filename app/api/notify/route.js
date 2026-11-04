import { NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)
const ADMIN = 'christine.walker@hairdresser.net'
const FROM = 'Chris 2 Styles Salon <bookings@chris2styles.co.uk>'
const URL = 'https://chris2styles.co.uk'

function emailWrap(body) {
  return `<div style='font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto'><div style='background:#1A1A1A;padding:24px;text-align:center'><h1 style='color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0'>Chris 2 Styles</h1><p style='color:#999;margin:4px 0 0;font-size:12px;letter-spacing:2px;text-transform:uppercase'>Healthy Hair Club</p></div><div style='padding:32px;background:#F5F3EE'>${body}</div><div style='padding:20px;text-align:center;background:#1A1A1A'><p style='color:#666;font-size:12px;margin:0'>Chris 2 Styles Salon · Mitcham Lane · London SW16</p></div></div>`
}

function btn(text, url) {
  return `<a href='${url}' style='display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase'>${text}</a>`
}

import { getUserFromReq, isAdmin } from '../../lib/server'

// Plain-text version of an email, so it isn't HTML-only (which spam filters distrust).
function toText(html) {
  return html
    .replace(/<a [^>]*href='([^']*)'[^>]*>([^<]*)<\/a>/g, '$2: $1')
    .replace(/<\/(h1|h2|p|div)>/g, '\n')
    .replace(/<br\s*\/?>/g, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s*\n+/g, '\n\n')
    .trim()
}

function esc(v) {
  return String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
}

// Emails anyone signed in may trigger (they only ever go to the salon).
const MEMBER_TYPES = ['message_received', 'credit_gifted']
// Emails that go to clients: only the server itself or a signed-in admin may trigger them.
const PROTECTED_TYPES = ['membership_paused', 'membership_resumed', 'membership_cancelled', 'package_change_requested', 'booking_submitted', 'booking_confirmed', 'booking_declined', 'message_replied', 'payment_failed', 'payment_restored']

export async function POST(req) {
  try {
    const { type, data: raw } = await req.json()
    const internal = process.env.SUPABASE_SECRET_KEY && req.headers.get('x-internal-key') === process.env.SUPABASE_SECRET_KEY
    if (!internal) {
      const user = await getUserFromReq(req)
      const allowed = MEMBER_TYPES.includes(type) ? !!user : (PROTECTED_TYPES.includes(type) && user && await isAdmin(user.email))
      if (!allowed) return NextResponse.json({ error: 'Not allowed' }, { status: 403 })
    }
    const data = Object.fromEntries(Object.entries(raw || {}).map(([k, v]) => [k, k === 'clientEmail' ? String(v ?? '') : esc(v)]))
    // Sends one email with a plain-text copy, replies going to the salon inbox.
    // Resend reports refusals in its return value rather than throwing, so check it and log the reason.
    const send = async (to, subject, html) => {
      const { error } = await resend.emails.send({ from: FROM, to, subject, html, text: toText(html), replyTo: ADMIN })
      if (error) console.error('Email not sent:', type, subject, error.name, error.message)
    }

    if (type === 'booking_submitted') {
      await send(ADMIN, 'New Booking Request — Healthy Hair Club',
        emailWrap(`<h2>New Booking Request</h2><p><strong>Client:</strong> ${data.clientName}</p><p><strong>Service:</strong> ${data.service}</p><p><strong>Date:</strong> ${data.date} at ${data.time}</p><p><strong>Add-ons:</strong> ${data.addons||'None'}</p>${btn('View in Admin', URL+'/admin')}`)
      )
    }

    if (type === 'booking_confirmed') {
      await send(data.clientEmail, 'Your Appointment is Confirmed — Healthy Hair Club',
        emailWrap(`<h2 style='color:#2E7D32'>Your appointment is confirmed</h2><p>Hi ${data.clientName}, we look forward to seeing you.</p><div style='background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF'><p><strong>Service:</strong> ${data.service}</p><p><strong>Date:</strong> ${data.date}</p><p><strong>Time:</strong> ${data.time}</p>${data.creditApplied && data.creditApplied !== '0' ? `<p><strong>Styling credit used:</strong> £${data.creditApplied} (remaining £${data.creditBalance})</p>` : ''}</div><p style='color:#888;font-size:13px'>Please provide at least 24 hours notice if you need to reschedule.</p>${btn('View My Dashboard', URL)}`)
      )
    }

    if (type === 'booking_declined') {
      await send(data.clientEmail, 'Appointment Update — Healthy Hair Club',
        emailWrap(`<h2>Appointment Update</h2><p>Hi ${data.clientName}, unfortunately we were unable to confirm your requested appointment at this time.</p><p>Please log in to choose another available appointment.</p>${btn('Choose Another Appointment', URL)}`)
      )
    }

    if (type === 'message_received') {
      const tel = data.phone ? String(data.phone).replace(/[^\d+]/g, '') : ''
      await send(ADMIN, (data.phone ? 'Call Back Request — ' : 'New Message — ') + data.clientName,
        emailWrap(`<h2>${data.phone ? 'Call back request' : 'New message'} from ${data.clientName}</h2>${data.phone ? `<p style='font-size:18px'><strong>Phone:</strong> <a href='tel:${tel}'>${data.phone}</a></p><p>They've been told you'll ring them back <strong>within 24 hours</strong>.</p>` : ''}<p><strong>Email:</strong> ${esc(data.clientEmail)}</p><div style='background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF'><p style='white-space:pre-wrap'>${data.message}</p></div>${btn('Open Messages in Admin', URL+'/admin')}`)
      )
    }

    if (type === 'message_replied') {
      await send(data.clientEmail, 'A Reply from Chris 2 Styles Salon',
        emailWrap(`<h2>Christine has replied to your message</h2><p>Hi ${data.clientName},</p><div style='background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF'><p style='white-space:pre-wrap'>${data.preview}</p></div><p style='color:#888;font-size:13px'>You can reply to this email, or send another message from the Help button in the app.</p>${btn('Open the App', URL)}`)
      )
    }

    if (type === 'membership_paused') {
      await send(ADMIN, 'Membership Paused — ' + data.clientName,
        emailWrap(`<h2>A member has paused their membership</h2><p><strong>Client:</strong> ${data.clientName}</p><p><strong>Paused:</strong> ${data.months} month(s), from ${data.from}</p><p><strong>Payments restart:</strong> ${data.until}</p><p>Nothing for you to do: Stripe and the app handle it automatically.</p>${btn('View in Admin', URL+'/admin')}`))
      if (data.clientEmail) await send(data.clientEmail, 'Your Membership Pause — Healthy Hair Club',
        emailWrap(`<h2>Your pause is booked</h2><p>Hi ${data.clientName},</p><p>Your membership will pause from <strong>${data.from}</strong> (your next payment date). No payments will be taken and booking is unavailable while paused.</p><p>Your membership restarts automatically on <strong>${data.until}</strong>, when your monthly payment will be taken again. If you'd rather not continue, please cancel from your dashboard before then.</p><p>Want to come back sooner? You can end your pause early from your dashboard.</p>${btn('View My Dashboard', URL)}`))
    }

    if (type === 'membership_resumed') {
      await send(ADMIN, 'Membership Resumed Early — ' + data.clientName,
        emailWrap(`<p><strong>${data.clientName}</strong> has ended their pause early. Their payment restarts today and they can book again.</p>${btn('View in Admin', URL+'/admin')}`))
    }

    if (type === 'membership_cancelled') {
      await send(ADMIN, 'Membership Cancelled — ' + data.clientName,
        emailWrap(`<h2>A member has cancelled</h2><p><strong>Client:</strong> ${data.clientName}</p><p><strong>Membership ends:</strong> ${data.until} (end of the month they've paid for). No further payments will be taken.</p>${btn('View in Admin', URL+'/admin')}`))
      if (data.clientEmail) await send(data.clientEmail, 'Your Membership Cancellation — Healthy Hair Club',
        emailWrap(`<h2>We're sorry to see you go</h2><p>Hi ${data.clientName},</p><p>Your Healthy Hair Club membership is cancelled and will end on <strong>${data.until}</strong>. You can keep using your benefits until then, and no further payments will be taken.</p><p>Changed your mind? You can keep your membership from your dashboard before that date.</p>${btn('View My Dashboard', URL)}`))
    }

    if (type === 'package_change_requested') {
      await send(ADMIN, 'Package Change — ' + data.clientName,
        emailWrap(`<h2>A member has changed their package</h2><p><strong>Client:</strong> ${data.clientName}</p><p><strong>From:</strong> ${data.from}</p><p><strong>To:</strong> ${data.to}</p><p><strong>Takes effect:</strong> ${data.date} (their next payment date)</p><p>Nothing for you to do: Stripe and the app switch it automatically.</p>${btn('View in Admin', URL+'/admin')}`)
      )
      if (data.clientEmail) await send(data.clientEmail, 'Your Package Change — Healthy Hair Club',
        emailWrap(`<h2>Your package change is booked in</h2><p>Hi ${data.clientName},</p><p>You're moving from <strong>${data.from}</strong> to <strong>${data.to}</strong>. The change takes effect on <strong>${data.date}</strong>, your next payment date, when the new monthly price is taken. Until then you keep your current benefits.</p><p>Changed your mind? You can cancel the change from your dashboard before that date.</p>${btn('View My Dashboard', URL)}`)
      )
    }

    if (type === 'credit_gifted') {
      const user = internal ? null : await getUserFromReq(req)
      await send(ADMIN, 'Elite Credit Gifted — Healthy Hair Club',
        emailWrap(`<h2>An Elite member has gifted credit</h2><p><strong>From:</strong> ${esc(user?.email || 'Member')}</p><p><strong>To:</strong> ${data.recipient} (${data.contact})</p><p><strong>Amount:</strong> £${data.amount}</p><p><strong>Use by:</strong> ${data.expires}</p><p>You'll find it under Bookings → Gifted Elite credit when they come in.</p>${btn('View in Admin', URL+'/admin')}`)
      )
    }

    if (type === 'payment_failed') {
      await send(data.clientEmail, 'Action Required — Healthy Hair Club Membership',
        emailWrap(`<h2 style='color:#B71C1C'>Action Required — Payment Issue</h2><p>Hi ${data.clientName}, there is an issue with your Healthy Hair Club membership payment.</p><p>Your booking access has been temporarily paused. Please update your payment details to restore your membership.</p>${btn('Update Payment Details', 'https://billing.stripe.com')}`)
      )
      await send(ADMIN, 'Payment Failed — '+data.clientName,
        emailWrap(`<p>Payment failed for <strong>${data.clientName}</strong> (${data.clientEmail}). Their membership has been paused automatically.</p>`)
      )
    }

    if (type === 'payment_restored') {
      await send(data.clientEmail, 'Your Membership is Active Again — Healthy Hair Club',
        emailWrap(`<h2 style='color:#2E7D32'>Your membership is active again</h2><p>Hi ${data.clientName}, your payment has been successfully processed and your booking access has been fully restored.</p>${btn('View My Dashboard', URL)}`)
      )
    }

    return NextResponse.json({ sent: true })
  } catch (err) {
    console.error('Notification error:', err)
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}