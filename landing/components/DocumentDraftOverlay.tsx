'use client'

import { useState, useEffect } from 'react'
import { X, Maximize2, Minimize2 } from 'lucide-react'
import { getActiveDoc, subscribe, setActiveDoc } from '@/lib/documentState'

const DOC_LABELS: Record<string, string> = {
  'rent-agreement': 'Rent Agreement',
  'registered-rent': 'Registered Rent Agreement',
  'ats': 'Agreement to Sell / ATS',
  'tm48': 'Transfer Memorandum / TM',
  'gnida_registry': 'Registry',
  'gnida_ptm': 'Permission to Mortgage / PTM',
  'mutation': 'Mutation',
  'gnida_package': 'GNIDA 5-in-1 Package',
}

export default function DocumentDraftOverlay() {
  const [activeDoc, setActiveDocState] = useState<string | null>(null)
  const [fullscreen, setFullscreen] = useState(false)

  useEffect(() => {
    setActiveDocState(getActiveDoc())
    const unsub = subscribe((doc) => setActiveDocState(doc))
    return unsub
  }, [])

  const handleClose = () => {
    setActiveDoc(null)
  }

  if (!activeDoc) return null

  const label = DOC_LABELS[activeDoc] || activeDoc

  return (
    <div className="fixed inset-0 z-[9999] flex flex-col bg-white">
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2.5 shadow-sm">
        <div className="flex items-center gap-3">
          <button
            onClick={handleClose}
            className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-semibold text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <X className="h-4 w-4" />
            Back
          </button>
          <div className="h-5 w-px bg-gray-200" />
          <span className="text-sm font-bold text-gray-900">{label}</span>
        </div>
        <button
          onClick={() => setFullscreen(!fullscreen)}
          className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
        >
          {fullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
        </button>
      </div>

      <div className="flex-1">
        <iframe
          src={`/api/draft-serve?doc=${encodeURIComponent(activeDoc)}`}
          className="h-full w-full border-0"
          title={label}
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"
        />
      </div>
    </div>
  )
}
