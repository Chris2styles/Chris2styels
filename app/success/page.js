'use client'
import { useEffect } from 'react'

export default function Success() {
  useEffect(() => {
    setTimeout(() => {
      window.location.href = '/'
    }, 3000)
  }, [])

  return (
    <div style={{minHeight:'100vh',background:'#F5F3EE',display:'flex',alignItems:'center',justifyContent:'center',fontFamily:'Helvetica Neue,sans-serif'}}>
      <div style={{textAlign:'center',padding:40}}>
        <div style={{fontSize:60,marginBottom:20}}>🖤</div>
        <h1 style={{fontFamily:'Georgia,serif',fontSize:32,fontStyle:'italic',color:'#1A1A1A',marginBottom:12}}>Welcome to the Healthy Hair Club!</h1>
        <p style={{color:'#666',fontSize:16,lineHeight:1.8,maxWidth:400,margin:'0 auto 12px'}}>Your membership is now active. Christine and the team will be in touch shortly to book your first appointment.</p>
        <p style={{color:'#999',fontSize:13}}>Returning you to the app in 3 seconds...</p>
      </div>
    </div>
  )
}