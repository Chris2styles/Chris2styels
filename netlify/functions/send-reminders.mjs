// Runs every hour and asks the app to send any 24-hour appointment reminders that are due.
export default async () => {
  const base = process.env.NEXT_PUBLIC_APP_URL || process.env.URL || 'https://chris2styles.co.uk'
  const res = await fetch(`${base}/api/reminders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-internal-key': process.env.SUPABASE_SECRET_KEY },
    body: '{}',
  })
  console.log('reminders', res.status, (await res.text()).slice(0, 500))
}

export const config = { schedule: '@hourly' }
