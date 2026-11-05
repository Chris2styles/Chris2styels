import { supabaseAdmin as supabase } from '../../../lib/server'

// Private "busy times" calendar feed for Treatwell (Team → Christine → External calendar).
// URL: https://chris2styles.co.uk/api/calendar/<CALENDAR_FEED_TOKEN>.ics
// Only free/busy blocks are published: no client names, services or contact details.

export const dynamic = 'force-dynamic'

// Convert a London wall-clock date+time to a UTC ICS timestamp (handles GMT/BST).
function londonToUtc(date, time) {
  const [y, mo, d] = date.split('-').map(Number)
  const [h, mi] = time.split(':').map(Number)
  const guess = Date.UTC(y, mo - 1, d, h, mi)
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', hourCycle: 'h23',
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).formatToParts(new Date(guess))
  const g = Object.fromEntries(parts.map(p => [p.type, p.value]))
  const shown = Date.UTC(+g.year, +g.month - 1, +g.day, +g.hour, +g.minute)
  return new Date(guess - (shown - guess))
}
const ics = d => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')

export async function GET(req, { params }) {
  const { file } = await params
  const token = String(file || '').replace(/\.ics$/i, '')
  if (!process.env.CALENDAR_FEED_TOKEN || token !== process.env.CALENDAR_FEED_TOKEN) {
    return new Response('Not found', { status: 404 })
  }
  const from = new Date(Date.now() - 2 * 86400000).toISOString().slice(0, 10)
  const { data: rows, error } = await supabase.from('bookings')
    .select('id, booking_date, booking_time, status, updated_at, slots(duration_mins)')
    .gte('booking_date', from)
    .not('status', 'in', '(cancelled,declined,rejected)')
  if (error) return new Response('Error', { status: 500 })

  const now = ics(new Date())
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Chris 2 Styles Salon//Healthy Hair Club//EN',
    'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'X-WR-CALNAME:Healthy Hair Club bookings', 'X-PUBLISHED-TTL:PT15M',
    'REFRESH-INTERVAL;VALUE=DURATION:PT15M']
  for (const b of rows || []) {
    if (!b.booking_date || !b.booking_time) continue
    const start = londonToUtc(b.booking_date, b.booking_time)
    const mins = b.slots?.duration_mins || 60
    const end = new Date(start.getTime() + mins * 60000)
    lines.push('BEGIN:VEVENT', `UID:hhc-${b.id}@chris2styles.co.uk`, `DTSTAMP:${now}`,
      `DTSTART:${ics(start)}`, `DTEND:${ics(end)}`, 'SUMMARY:Healthy Hair Club booking', 'TRANSP:OPAQUE', 'STATUS:CONFIRMED', 'END:VEVENT')
  }
  lines.push('END:VCALENDAR')
  return new Response(lines.join('\r\n') + '\r\n', {
    headers: { 'Content-Type': 'text/calendar; charset=utf-8', 'Cache-Control': 'no-store' },
  })
}
