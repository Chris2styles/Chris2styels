import { NextResponse } from 'next/server'
import { supabaseAdmin as supabase, getUserFromReq, SERVICES, notify, isMaintenance } from '../../lib/server'

export async function POST(req) {
  try {
    const user = await getUserFromReq(req)
    if (!user) return NextResponse.json({ error: 'Please sign in to book.' }, { status: 401 })

    const { service, slotId, addons, complimentaryAddon } = await req.json()
    if (!service || !slotId) return NextResponse.json({ error: 'Choose a service and a time.' }, { status: 400 })

    const { data: client } = await supabase.from('clients').select('id, full_name, email').ilike('email', user.email).maybeSingle()
    if (!client) return NextResponse.json({ error: 'We could not find your membership.' }, { status: 404 })

    const { data: membership } = await supabase.from('memberships').select('package, status')
      .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
    if (membership?.status === 'pending') {
      return NextResponse.json({ error: 'Your membership starts on your first payment date. You will be able to book once your first payment has gone through.' }, { status: 403 })
    }
    if (!membership || membership.status !== 'active') {
      return NextResponse.json({ error: 'Your membership is not active, so booking is paused. Please update your payment details or contact the salon.' }, { status: 403 })
    }
    // No booking while paused (checked for both today and the appointment date).
    const { data: mid } = await supabase.from('memberships').select('id')
      .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
    const { data: slotRow } = await supabase.from('slots').select('slot_date').eq('id', slotId).maybeSingle()
    for (const day of [undefined, slotRow?.slot_date]) {
      const { data: pb } = mid ? await supabase.rpc('membership_benefits', { p_membership: mid.id, ...(day ? { p_on: day } : {}) }) : { data: null }
      if (pb?.paused_now) {
        return NextResponse.json({ error: `Your membership is paused${pb.pause?.ends_on ? ' until ' + new Date(pb.pause.ends_on + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long' }) : ''}, so booking isn't available${day ? ' on that date' : ''}. You can end your pause early from your dashboard.` }, { status: 403 })
      }
    }
    if (!(SERVICES[membership.package] || []).includes(service)) {
      return NextResponse.json({ error: 'That service is not included in your membership.' }, { status: 403 })
    }

    // Maintenance services are limited (Essential: 1 per 3-month block from the 3rd month; Signature/Elite: 1 per month).
    // Check before taking the slot so the member gets a clear message; approval re-checks in the database.
    if (isMaintenance(service)) {
      const { data: s0 } = await supabase.from('slots').select('slot_date').eq('id', slotId).maybeSingle()
      const { data: mem } = await supabase.from('memberships').select('id')
        .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
      if (s0 && mem) {
        const { data: ben } = await supabase.rpc('membership_benefits', { p_membership: mem.id, p_on: s0.slot_date })
        const mt = ben?.maintenance
        if (mt && !mt.started) {
          return NextResponse.json({ error: `Your first quarterly maintenance service is available from ${new Date(mt.window_start + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}. Please choose a later date.` }, { status: 409 })
        }
        if (mt && mt.remaining < 1) {
          return NextResponse.json({ error: 'You have already used your maintenance service for this period. Please choose a date in your next period, or contact the salon.' }, { status: 409 })
        }
      }
    }

    const addonList = Array.isArray(addons) ? addons.map(String).slice(0, 20) : []

    // Optional: one add-on the member wants as complimentary. Must be on this booking and they must have one left.
    let freeAddon = null
    if (complimentaryAddon) {
      freeAddon = String(complimentaryAddon)
      if (!addonList.includes(freeAddon)) return NextResponse.json({ error: 'The complimentary add-on must be one of your chosen add-ons.' }, { status: 400 })
      const { data: s1 } = await supabase.from('slots').select('slot_date').eq('id', slotId).maybeSingle()
      const { data: mem1 } = await supabase.from('memberships').select('id')
        .eq('client_id', client.id).order('created_at', { ascending: false }).limit(1).maybeSingle()
      const { data: ben1 } = mem1 && s1 ? await supabase.rpc('membership_benefits', { p_membership: mem1.id, p_on: s1.slot_date }) : { data: null }
      if (!ben1 || ben1.complimentary.remaining < 1) {
        return NextResponse.json({ error: 'You have no complimentary add-ons left this membership year.' }, { status: 409 })
      }
    }
    const { data: bookingId, error } = await supabase.rpc('create_booking', {
      p_client: client.id, p_slot: slotId, p_service: service, p_addons: addonList, p_notes: null,
    })
    if (error) {
      const taken = /slot no longer available|bookings_one_active_per_slot/.test(error.message)
      return NextResponse.json({ error: taken ? 'Sorry, that time has just been taken. Please choose another.' : 'Booking failed. Please try again.' }, { status: taken ? 409 : 500 })
    }

    if (freeAddon) await supabase.from('bookings').update({ complimentary_addon: freeAddon }).eq('id', bookingId)

    const { data: slot } = await supabase.from('slots').select('slot_date, slot_time').eq('id', slotId).single()
    await notify(req, 'booking_submitted', {
      clientName: client.full_name || client.email,
      service,
      date: slot ? new Date(slot.slot_date).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }) : '',
      time: slot ? String(slot.slot_time).slice(0, 5) : '',
      addons: addonList.join(', ') + (freeAddon ? ` (complimentary requested: ${freeAddon})` : ''),
      pkg: membership.package,
    })

    return NextResponse.json({ success: true, bookingId })
  } catch (err) {
    console.error('book error', err)
    return NextResponse.json({ error: 'Booking failed. Please try again.' }, { status: 500 })
  }
}
