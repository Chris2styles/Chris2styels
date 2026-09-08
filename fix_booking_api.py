import os

# Create the booking API route
os.makedirs('app/api/book', exist_ok=True)

content = '''import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY
)

export async function POST(req) {
  try {
    const { clientEmail, service, slotDate, slotTime, addons } = await req.json()

    // Find client
    const { data: clients } = await supabase.from('clients').select('*')
    const client = clients && clients.find(c => c.email === clientEmail)
    if (!client) {
      return NextResponse.json({ error: 'Client not found' }, { status: 404 })
    }

    // Save booking
    const { data: booking, error } = await supabase.from('bookings').insert({
      client_id: client.id,
      service: service,
      status: 'pending',
      notes: `Date: ${slotDate} at ${slotTime}. Add-ons: ${addons.join(', ')}`,
    }).select().single()

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ success: true, bookingId: booking.id })
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}
'''

with open('app/api/book/route.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Booking API created!")