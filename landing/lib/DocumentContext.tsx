'use client'

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react'

type DocType = string | null

interface DocumentContextValue {
  activeDoc: DocType
  setActiveDoc: (doc: DocType) => void
  clearActiveDoc: () => void
}

const DocumentContext = createContext<DocumentContextValue>({
  activeDoc: null,
  setActiveDoc: () => {},
  clearActiveDoc: () => {},
})

const STORAGE_KEY = 'instadeed_active_doc'

export function DocumentProvider({ children }: { children: ReactNode }) {
  const [activeDoc, setActiveDocState] = useState<DocType>(null)

  useEffect(() => {
    const saved = sessionStorage.getItem(STORAGE_KEY)
    if (saved) {
      setActiveDocState(saved)
    }
  }, [])

  const setActiveDoc = useCallback((doc: DocType) => {
    setActiveDocState(doc)
    if (doc) {
      sessionStorage.setItem(STORAGE_KEY, doc)
    } else {
      sessionStorage.removeItem(STORAGE_KEY)
    }
  }, [])

  const clearActiveDoc = useCallback(() => {
    setActiveDocState(null)
    sessionStorage.removeItem(STORAGE_KEY)
  }, [])

  return (
    <DocumentContext.Provider value={{ activeDoc, setActiveDoc, clearActiveDoc }}>
      {children}
    </DocumentContext.Provider>
  )
}

export function useDocument() {
  return useContext(DocumentContext)
}
