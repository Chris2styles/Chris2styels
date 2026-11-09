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
  const [showPw, setShowPw] = useState(false)
  const [notice, setNotice] = useState('')
  const [recovery, setRecovery] = useState(false)   // arrived from a "reset your password" email
  const [newPw, setNewPw] = useState('')

  useEffect(() => {
    if (typeof window !== 'undefined' && window.location.hash.includes('type=recovery')) setRecovery(true)
    const { data: sub } = supabase.auth.onAuthStateChange((event) => { if (event === 'PASSWORD_RECOVERY') setRecovery(true) })
    return () => sub.subscription.unsubscribe()
  }, [])

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
    const { error: e } = await supabase.auth.signInWithPassword({ email: email.trim(), password })
    if (e) { setError(e.message); setLoading(false); return; }
    const { data: adminUser } = await supabase
      .from('admin_users')
      .select('email')
      .eq('email', email.trim())
      .single()
    if (!adminUser) { setError('Access denied. Admin only.'); setLoading(false); return; }
    setVerified(true)
    setLoading(false)
  }

  async function forgot() {
    setError(''); setNotice('')
    if (!email.trim()) { setError('Type your admin email address first, then tap "Forgot password?" again.'); return }
    const { error: e } = await supabase.auth.resetPasswordForEmail(email.trim(), { redirectTo: window.location.origin + '/admin' })
    if (e) { setError(e.message); return }
    setNotice('If that email is your admin email, a link to choose a new password is on its way. Check your inbox (and spam), then tap the link on this phone.')
  }

  async function saveNewPassword() {
    setError(''); setNotice('')
    if (newPw.length < 8) { setError('Please use at least 8 characters.'); return }
    setLoading(true)
    const { error: e } = await supabase.auth.updateUser({ password: newPw })
    setLoading(false)
    if (e) { setError(e.message); return }
    setRecovery(false); setNewPw('')
    if (typeof window !== 'undefined') window.history.replaceState(null, '', '/admin')
    const { data: { user } } = await supabase.auth.getUser()
    const { data: adminUser } = user ? await supabase.from('admin_users').select('email').eq('email', user.email).single() : { data: null }
    if (adminUser) setVerified(true); else setNotice('Password changed. You can sign in now.')
  }

  const inputStyle = {width:'100%',padding:'12px 14px',background:'#272727',border:'1px solid #3A3A3A',borderRadius:4,color:'#FFF',fontSize:14,outline:'none',boxSizing:'border-box'}
  const eye = (on, toggle) => (
    <button type="button" onClick={toggle} aria-label={on ? 'Hide password' : 'Show password'}
      style={{position:'absolute',right:8,top:'50%',transform:'translateY(-50%)',background:'none',border:'none',color:'#C9A84C',cursor:'pointer',fontSize:12,fontWeight:700,padding:'6px 8px'}}>
      {on ? 'Hide' : 'Show'}
    </button>
  )

  if (recovery) return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#080808',fontFamily:'Helvetica Neue,sans-serif',padding:16}}>
      <div style={{background:'#111',border:'1px solid #3A3A3A',borderRadius:8,padding:32,width:'100%',maxWidth:380,boxSizing:'border-box'}}>
        <div style={{textAlign:'center',marginBottom:24}}>
          <div style={{fontFamily:'Georgia,serif',fontSize:22,color:'#C9A84C',fontStyle:'italic'}}>Choose a new password</div>
        </div>
        {error && <div style={{background:'#FFEBEE',color:'#B71C1C',padding:'10px 14px',borderRadius:4,marginBottom:16,fontSize:13}}>{error}</div>}
        <div style={{position:'relative',marginBottom:20}}>
          <input type={showPw ? 'text' : 'password'} value={newPw} onChange={e=>setNewPw(e.target.value)} placeholder="New password (8+ characters)" autoComplete="new-password" style={{...inputStyle,paddingRight:64}}/>
          {eye(showPw, ()=>setShowPw(!showPw))}
        </div>
        <button onClick={saveNewPassword} disabled={loading}
          style={{width:'100%',padding:'14px 0',background:'linear-gradient(135deg,#E2C97E,#C9A84C)',color:'#1A1A1A',border:'none',borderRadius:4,fontWeight:700,fontSize:13,letterSpacing:1.5,textTransform:'uppercase',cursor:'pointer'}}>
          Save new password
        </button>
      </div>
    </div>
  )

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
        {notice && <div style={{background:'#1E1A0E',color:'#E2C97E',border:'1px solid #6B5A2A',padding:'10px 14px',borderRadius:4,marginBottom:16,fontSize:13,lineHeight:1.5}}>{notice}</div>}
        <div style={{marginBottom:14}}>
          <div style={{color:'#999',fontSize:11,fontWeight:700,letterSpacing:2,textTransform:'uppercase',marginBottom:6}}>Email</div>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)} autoCapitalize="none" autoCorrect="off" autoComplete="username"
            style={{width:'100%',padding:'12px 14px',background:'#272727',border:'1px solid #3A3A3A',borderRadius:4,color:'#FFF',fontSize:14,outline:'none',boxSizing:'border-box'}}/>
        </div>
        <div style={{marginBottom:24}}>
          <div style={{color:'#999',fontSize:11,fontWeight:700,letterSpacing:2,textTransform:'uppercase',marginBottom:6}}>Password</div>
          <div style={{position:'relative'}}>
            <input type={showPw ? 'text' : 'password'} value={password} onChange={e=>setPassword(e.target.value)}
              onKeyDown={e=>e.key==='Enter'&&signIn()} autoComplete="current-password"
              style={{...inputStyle,paddingRight:64}}/>
            {eye(showPw, ()=>setShowPw(!showPw))}
          </div>
          <button type="button" onClick={forgot} style={{background:'none',border:'none',color:'#C9A84C',fontSize:12,marginTop:8,padding:0,cursor:'pointer',textDecoration:'underline'}}>Forgot password?</button>
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