import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY
)

export async function GET() {
  const { data, error } = await supabase
    .from('slots')
    .select('*')
    .eq('is_blocked', false)
    .eq('booked', false)
    .order('slot_date', { ascending: true })

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ slots: data || [] })
}

export async function POST(req) {
  const { date, time, duration, stylistId } = await req.json()
  const { data, error } = await supabase.from('slots').insert({
    slot_date: date,
    slot_time: time,
    duration_mins: duration || 60,
    stylist_id: stylistId || null,
    members_only: true,
    is_blocked: false,
    booked: false,
  }).select().single()

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })
  return NextResponse.json({ slot: data })
}
