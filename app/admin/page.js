import { createClient } from '@supabase/supabase-js'
import { redirect } from 'next/navigation'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SECRET_KEY
)

export default async function AdminPage() {
  const { data: { session } } = await supabase.auth.getSession()
  
  if (!session) {
    redirect('/?admin=true')
  }

  const { data: adminUser } = await supabase
    .from('admin_users')
    .select('email')
    .eq('email', session.user.email)
    .single()

  if (!adminUser) {
    redirect('/')
  }

  return null
}