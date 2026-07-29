'use client'
import dynamic from 'next/dynamic'
const HHCApp = dynamic(() => import('./HHCApp.jsx').then(m => m.default || m), { ssr: false })
export default function Page() {
  return <HHCApp />
}