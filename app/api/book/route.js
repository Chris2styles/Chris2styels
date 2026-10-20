import { NextResponse } from 'next/server'
import { supabaseAdmin as supabase, getUserFromReq, SERVICES, notify } from '../../lib/server'

export async function POST(req) {
  try {
    const user = await getUserFromReq(req)
    if (!user) return NextResponse.json({ error: 'Please sign in to book.' }, { status: 401 })

    const { service, slotId, addons } = await req.json()
    if (!service || !slotId) return NextResponse.json({ error: 'Choose a service and a time.' }, { status: 400 })

    const { data: client } = await supabase.from('clients').select('id, full_name, email').ilike('email', user.email).maybeSingle()
    if (!client) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })

    const { data: membership } = await supabase.from('memberships').select('package, status')
      .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
    if (!membership || membership.status !== 'active') {
      return NextResponse.json({ error: 'Your membership is not active, so booking is paused. Please update your payment details or contact the salon.' }, { status: 403 })
    }
    if (!(SERVICES[membership.package] || []).includes(service)) {
      return NextResponse.json({ error: 'That service is not included in your membership.' }, { status: 403 })
    }

    const addonList = Array.isArray(addons) ? addons.map(String).slice(0, 20) : []
    const { data: bookingId, error } = await supabase.rpc('create_booking', {
      p_client: client.id, p_slot: slotId, p_service: service, p_addons: addonList, p_notes: null,
    })
    if (error) {
      const taken = /slot no longer available|bookings_one_active_per_slot/.test(error.message)
      return NextResponse.json({ error: taken ? 'Sorry, that time has just been taken. Please choose another.' : 'Booking failed. Please try again.' }, { status: taken ? 409 : 500 })
    }

    const { data: slot } = await supabase.from('slots').select('slot_date, slot_time').eq('id', slotId).single()
    await notify(req, 'booking_submitted', {
      clientName: client.full_name || client.email,
      service,
      date: slot ? new Date(slot.slot_date).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }) : '',
      time: slot ? String(slot.slot_time).slice(0, 5) : '',
      addons: addonList.join(', '),
      pkg: membership.package,
    })

    return NextResponse.json({ success: true, bookingId })
  } catch (err) {
    console.error('book error', err)
    return NextResponse.json({ error: 'Booking failed. Please try again.' }, { status: 500 })
  }
}
