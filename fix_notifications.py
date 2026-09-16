import os

os.makedirs('app/api/notify', exist_ok=True)

content = '''import { NextResponse } from 'next/server'
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

const ADMIN_EMAIL = 'christine.walker@hairdresser.net'
const FROM_EMAIL = 'noreply@chris2styles.co.uk'
const APP_URL = 'https://chris2styles.co.uk'

export async function POST(req) {
  try {
    const { type, data } = await req.json()

    if (type === 'booking_submitted') {
      // Notify admin of new booking
      await resend.emails.send({
        from: FROM_EMAIL,
        to: ADMIN_EMAIL,
        subject: 'New Booking Request — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
              <p style="color:#999;margin:4px 0 0;font-size:12px;letter-spacing:2px;text-transform:uppercase">Healthy Hair Club</p>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#1A1A1A;margin:0 0 16px">New Booking Request</h2>
              <p style="color:#555"><strong>Client:</strong> ${data.clientName}</p>
              <p style="color:#555"><strong>Service:</strong> ${data.service}</p>
              <p style="color:#555"><strong>Date:</strong> ${data.date}</p>
              <p style="color:#555"><strong>Time:</strong> ${data.time}</p>
              <p style="color:#555"><strong>Add-ons:</strong> ${data.addons||'None'}</p>
              <a href="${APP_URL}/admin" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">View in Admin</a>
            </div>
          </div>
        `
      })
    }

    if (type === 'booking_confirmed') {
      // Notify client their booking is confirmed
      await resend.emails.send({
        from: FROM_EMAIL,
        to: data.clientEmail,
        subject: 'Your Appointment is Confirmed — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
              <p style="color:#999;margin:4px 0 0;font-size:12px;letter-spacing:2px;text-transform:uppercase">Healthy Hair Club</p>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#1A1A1A;margin:0 0 8px">Your appointment is confirmed</h2>
              <p style="color:#555;margin:0 0 24px">Hi ${data.clientName}, we look forward to seeing you.</p>
              <div style="background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF">
                <p style="color:#555;margin:0 0 8px"><strong>Service:</strong> ${data.service}</p>
                <p style="color:#555;margin:0 0 8px"><strong>Date:</strong> ${data.date}</p>
                <p style="color:#555;margin:0"><strong>Time:</strong> ${data.time}</p>
              </div>
              <p style="color:#888;font-size:13px;margin-top:20px">Please provide at least 24 hours notice if you need to reschedule.</p>
              <a href="${APP_URL}" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">View My Dashboard</a>
            </div>
            <div style="padding:20px;text-align:center;background:#1A1A1A">
              <p style="color:#666;font-size:12px;margin:0">Chris 2 Styles Salon · Mitcham Lane · London SW16</p>
            </div>
          </div>
        `
      })
    }

    if (type === 'booking_declined') {
      await resend.emails.send({
        from: FROM_EMAIL,
        to: data.clientEmail,
        subject: 'Appointment Update — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
              <p style="color:#999;margin:4px 0 0;font-size:12px;letter-spacing:2px;text-transform:uppercase">Healthy Hair Club</p>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#1A1A1A;margin:0 0 8px">Appointment Update</h2>
              <p style="color:#555">Hi ${data.clientName}, unfortunately we were unable to confirm your requested appointment at this time.</p>
              <p style="color:#555">Please log in to your Healthy Hair Club account to choose another available appointment.</p>
              <a href="${APP_URL}" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">Choose Another Appointment</a>
            </div>
            <div style="padding:20px;text-align:center;background:#1A1A1A">
              <p style="color:#666;font-size:12px;margin:0">Chris 2 Styles Salon · Mitcham Lane · London SW16</p>
            </div>
          </div>
        `
      })
    }

    if (type === 'message_received') {
      // Notify admin of new client message
      await resend.emails.send({
        from: FROM_EMAIL,
        to: ADMIN_EMAIL,
        subject: 'New Message — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#1A1A1A;margin:0 0 16px">New Message from ${data.clientName}</h2>
              <div style="background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF">
                <p style="color:#555;margin:0">${data.message}</p>
              </div>
              <a href="${APP_URL}/admin" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">Reply in Admin</a>
            </div>
          </div>
        `
      })
    }

    if (type === 'message_replied') {
      // Notify client of admin reply
      await resend.emails.send({
        from: FROM_EMAIL,
        to: data.clientEmail,
        subject: 'New Message from Chris 2 Styles Salon — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
              <p style="color:#999;margin:4px 0 0;font-size:12px;letter-spacing:2px;text-transform:uppercase">Healthy Hair Club</p>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#1A1A1A;margin:0 0 8px">You have a new message from Chris 2 Styles Salon</h2>
              <p style="color:#555">Hi ${data.clientName},</p>
              <div style="background:#fff;border-radius:8px;padding:20px;border:1px solid #EDE8DF;margin:16px 0">
                <p style="color:#555;margin:0">${data.preview}</p>
              </div>
              <a href="${APP_URL}" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">View Message</a>
            </div>
            <div style="padding:20px;text-align:center;background:#1A1A1A">
              <p style="color:#666;font-size:12px;margin:0">Chris 2 Styles Salon · Mitcham Lane · London SW16</p>
            </div>
          </div>
        `
      })
    }

    if (type === 'payment_failed') {
      await resend.emails.send({
        from: FROM_EMAIL,
        to: data.clientEmail,
        subject: 'Action Required — Healthy Hair Club Membership',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#B71C1C;margin:0 0 16px">Action Required — Payment Issue</h2>
              <p style="color:#555">Hi ${data.clientName}, there is an issue with your Healthy Hair Club membership payment.</p>
              <p style="color:#555">Your booking access has been temporarily paused. Please update your payment details to restore your membership.</p>
              <a href="https://billing.stripe.com" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#C9A84C;color:#1A1A1A;text-decoration:none;border-radius:4px;font-weight:700;font-family:Trebuchet MS,sans-serif;letter-spacing:1px;text-transform:uppercase">Update Payment Details</a>
            </div>
            <div style="padding:20px;text-align:center;background:#1A1A1A">
              <p style="color:#666;font-size:12px;margin:0">Chris 2 Styles Salon · Mitcham Lane · London SW16</p>
            </div>
          </div>
        `
      })
      // Also notify admin
      await resend.emails.send({
        from: FROM_EMAIL,
        to: ADMIN_EMAIL,
        subject: 'Payment Failed — ' + data.clientName,
        html: `<p>Payment failed for <strong>${data.clientName}</strong> (${data.clientEmail}). Their membership has been paused automatically.</p>`
      })
    }

    if (type === 'payment_restored') {
      await resend.emails.send({
        from: FROM_EMAIL,
        to: data.clientEmail,
        subject: 'Your Membership is Active Again — Healthy Hair Club',
        html: `
          <div style="font-family:Helvetica Neue,sans-serif;max-width:600px;margin:0 auto">
            <div style="background:#1A1A1A;padding:24px;text-align:center">
              <h1 style="color:#C9A84C;font-family:Georgia,serif;font-style:italic;margin:0">Chris 2 Styles</h1>
            </div>
            <div style="padding:32px;background:#F5F3EE">
              <h2 style="color:#2E7D32;margin:0 0 16px">Your membership is active again</h2>
              <p style="color:#555">Hi ${data.clientName}, your Healthy Hair Club membership