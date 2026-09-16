'use client'
import { useState, useEffect } from 'react'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY
)

export default function AdminPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [verified, setVerified] = useState(false)

  useEffect(() => {
    async function check() {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        const { data: adminUser } = await supabase
          .from('admin_users')
          .select('email')
          .eq('email', user.email)
          .single()
        if (adminUser) {
          setVerified(true)
        }
      }
      setLoading(false)
    }
    check()
  }, [])

  async function signIn() {
    setLoading(true)
    setError('')
    const { error: e } = await supabase.auth.signInWithPassword({ email, password })
    if (e) { setError(e.message); setLoading(false); return; }
    const { data: adminUser } = await supabase
      .from('admin_users')
      .select('email')
      .eq('email', email)
      .single()
    if (!adminUser) { setError('Access denied. Admin only.'); setLoading(false); return; }
    setVerified(true)
    setLoading(false)
  }

  if (loading) return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#080808',color:'#C9A84C',fontFamily:'Georgia,serif',fontSize:24,fontStyle:'italic'}}>
      Verifying access...
    </div>
  )

  if (!verified) return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#080808',fontFamily:'Helvetica Neue,sans-serif'}}>
      <div style={{background:'#111',border:'1px solid #3A3A3A',borderRadius:8,padding:40,width:'100%',maxWidth:380}}>
        <div style={{textAlign:'center',marginBottom:32}}>
          <div style={{fontFamily:'Trebuchet MS,sans-serif',fontSize:13,color:'#FFF',letterSpacing:2,textTransform:'uppercase'}}>Chris 2 Styles</div>
          <div style={{fontFamily:'Georgia,serif',fontSize:22,color:'#C9A84C',fontStyle:'italic',marginTop:4}}>Admin Portal</div>
        </div>
        {error && <div style={{background:'#FFEBEE',color:'#B71C1C',padding:'10px 14px',borderRadius:4,marginBottom:16,fontSize:13}}>{error}</div>}
        <div style={{marginBottom:14}}>
          <div style={{color:'#999',fontSize:11,fontWeight:700,letterSpacing:2,textTransform:'uppercase',marginBottom:6}}>Email</div>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)}
            style={{width:'100%',padding:'12px 14px',background:'#272727',border:'1px solid #3A3A3A',borderRadius:4,color:'#FFF',fontSize:14,outline:'none',boxSizing:'border-box'}}/>
        </div>
        <div style={{marginBottom:24}}>
          <div style={{color:'#999',fontSize:11,fontWeight:700,letterSpacing:2,textTransform:'uppercase',marginBottom:6}}>Password</div>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)}
            onKeyDown={e=>e.key==='Enter'&&signIn()}
            style={{width:'100%',padding:'12px 14px',background:'#272727',border:'1px solid #3A3A3A',borderRadius:4,color:'#FFF',fontSize:14,outline:'none',boxSizing:'border-box'}}/>
        </div>
        <button onClick={signIn} disabled={loading}
          style={{width:'100%',padding:'14px 0',background:'linear-gradient(135deg,#E2C97E,#C9A84C)',color:'#1A1A1A',border:'none',borderRadius:4,fontFamily:'Trebuchet MS,sans-serif',fontWeight:700,fontSize:13,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
          Sign In to Admin
        </button>
      </div>
    </div>
  )

  // Load main app in admin mode
  const App = require('../HHCApp.jsx').default
  return <App startAdmin={true} />
}