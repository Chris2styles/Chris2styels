'use client'
import { useEffect, useState } from 'react'

export default function Success() {
  const [startsOn, setStartsOn] = useState(null)
  useEffect(() => {
    const s = new URLSearchParams(window.location.search).get('start')
    if (s && /^\d{4}-\d{2}-\d{2}$/.test(s)) setStartsOn(new Date(s + 'T00:00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }))
    const t = setTimeout(() => { window.location.href = '/' }, s ? 8000 : 3000)
    return () => clearTimeout(t)
  }, [])

  return (
    <div style={{minHeight:'100vh',background:'#F5F3EE',display:'flex',alignItems:'center',justifyContent:'center',fontFamily:'Helvetica Neue,sans-serif'}}>
      <div style={{textAlign:'center',padding:40}}>
        <div style={{fontSize:60,marginBottom:20}}>🖤</div>
        <h1 style={{fontFamily:'Georgia,serif',fontSize:32,fontStyle:'italic',color:'#1A1A1A',marginBottom:12}}>Welcome to the Healthy Hair Club!</h1>
        {startsOn ? (
          <p style={{color:'#666',fontSize:16,lineHeight:1.8,maxWidth:420,margin:'0 auto 12px'}}>You're all signed up. Nothing has been taken today. Your first payment and your membership start on <strong>{startsOn}</strong>, and you'll be able to book from then.</p>
        ) : (
          <p style={{color:'#666',fontSize:16,lineHeight:1.8,maxWidth:400,margin:'0 auto 12px'}}>Your membership is now active. Christine and the team will be in touch shortly to book your first appointment.</p>
        )}
        <p style={{color:'#999',fontSize:13}}>Returning you to the app shortly...</p>
      </div>
    </div>
  )
}
