'use client'

type DocType = string | null

type Listener = (doc: DocType) => void

let currentDoc: DocType = null
const listeners = new Set<Listener>()

function notify(doc: DocType) {
  currentDoc = doc
  listeners.forEach(fn => fn(doc))
}

export function getActiveDoc(): DocType {
  if (typeof window === 'undefined') return null
  return currentDoc
}

export function setActiveDoc(doc: DocType) {
  notify(doc)
  if (typeof window !== 'undefined') {
    if (doc) {
      sessionStorage.setItem('instadeed_active_doc', doc)
    } else {
      sessionStorage.removeItem('instadeed_active_doc')
    }
  }
}

export function subscribe(fn: Listener): () => void {
  listeners.add(fn)
  return () => listeners.delete(fn)
}

export function initializeFromStorage() {
  if (typeof window !== 'undefined') {
    const saved = sessionStorage.getItem('instadeed_active_doc')
    if (saved) {
      currentDoc = saved
    }
  }
}
