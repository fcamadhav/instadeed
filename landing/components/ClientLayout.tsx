'use client'

import { useEffect, ReactNode } from 'react'
import { initializeFromStorage } from '@/lib/documentState'
import DocumentDraftOverlay from '@/components/DocumentDraftOverlay'

export default function ClientLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    initializeFromStorage()
  }, [])

  return (
    <>
      {children}
      <DocumentDraftOverlay />
    </>
  )
}
