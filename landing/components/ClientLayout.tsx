'use client'

import { DocumentProvider } from '@/lib/DocumentContext'
import DocumentDraftOverlay from '@/components/DocumentDraftOverlay'
import { ReactNode } from 'react'

export default function ClientLayout({ children }: { children: ReactNode }) {
  return (
    <DocumentProvider>
      {children}
      <DocumentDraftOverlay />
    </DocumentProvider>
  )
}
