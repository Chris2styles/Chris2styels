'use client'
import dynamic from 'next/dynamic'
const HHCApp = dynamic(() => import('./HHCApp.jsx'), { ssr: false })
export default function Page() {
  return <HHCApp />
}