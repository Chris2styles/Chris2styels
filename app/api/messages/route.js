import { NextResponse } from 'next/server'
import { supabaseAdmin as supabase, getUserFromReq, notify } from '../../lib/server'

// A signed-in member sends a message from the Help button. It is saved for the admin Messages tab and the salon
// is emailed. If they leave a phone number, the salon calls them back within 24 hours.
export async function POST(req) {
  try {
    const user = await getUserFromReq(req)
    if (!user) return NextResponse.json({ error: 'Please sign in to send a message.' }, { status: 401 })
    const { message, phone } = await req.json()
    const body = String(message || '').trim().slice(0, 2000)
    if (!body) return NextResponse.json({ error: 'Please type your message.' }, { status: 400 })
    const ph = String(phone || '').replace(/[^\d+ ]/g, '').trim().slice(0, 20)
    if (ph && ph.replace(/\D/g, '').length < 10) return NextResponse.json({ error: 'Please check your phone number.' }, { status: 400 })

    const { data: client } = await supabase.from('clients').select('id, full_name, email, phone').ilike('email', user.email).maybeSingle()
    const name = client?.full_name || user.email

    // Simple protection against repeated sending: at most 10 messages an hour per member.
    const since = new Date(Date.now() - 3600 * 1000).toISOString()
    const { count } = await supabase.from('messages').select('id', { count: 'exact', head: true }).eq('client_email', user.email).gte('created_at', since)
    if ((count || 0) >= 10) return NextResponse.json({ error: 'You have sent several messages already. Christine will be in touch soon.' }, { status: 429 })

    const { error } = await supabase.from('messages').insert({
      client_id: client?.id || null, client_name: name, client_email: user.email,
      type: ph ? 'callback' : 'message', body, phone: ph || null, read: false,
    })
    if (error) throw error
    // Remember the number on their record if we didn't have one.
    if (ph && client && !client.phone) await supabase.from('clients').update({ phone: ph }).eq('id', client.id)

    await notify(req, 'message_received', { clientName: name, clientEmail: user.email, phone: ph, message: body })
    return NextResponse.json({ success: true, callback: !!ph })
  } catch (err) {
    console.error('message error', err)
    return NextResponse.json({ error: 'Your message could not be sent. Please try again, or call the salon on 020 3754 7889.' }, { status: 500 })
  }
}
