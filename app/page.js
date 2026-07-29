'use client'
import dynamic from 'next/dynamic'
const HHCApp = dynamic(() => import('./HHCApp.jsx').then(m => ({ default: m.App || m.default })), { ssr: false })
export default function Page() {
  return <HHCApp />
}