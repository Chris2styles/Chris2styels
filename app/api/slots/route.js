import { NextResponse } from 'next/server'
import { supabaseAdmin as supabase, getUserFromReq, isAdmin } from '../../lib/server'

export async function GET() {
  const today = new Date().toISOString().slice(0, 10)
  const { data, error } = await supabase
    .from('slots')
    .select('id, slot_date, slot_time, duration_mins, stylist_id, booked')
    .eq('is_blocked', false)
    .eq('booked', false)
    .gte('slot_date', today)
    .order('slot_date', { ascending: true })
    .order('slot_time', { ascending: true })

  if (error) return NextResponse.json({ error: 'Could not load times' }, { status: 500 })
  return NextResponse.json({ slots: data || [] })
}

export async function POST(req) {
  const user = await getUserFromReq(req)
  if (!user || !(await isAdmin(user.email))) return NextResponse.json({ error: 'Admin only' }, { status: 403 })
  const { date, time, duration, stylistId } = await req.json()
  const { data, error } = await supabase.from('slots').insert({
    slot_date: date, slot_time: time, duration_mins: duration || 60, stylist_id: stylistId || null,
    members_only: true, is_blocked: false, booked: false,
  }).select().single()
  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ slot: data })
}
