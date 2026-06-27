'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown } from 'lucide-react'

const faqs = [
  {
    q: 'What property documents can I prepare through INSTADEED?',
    a: 'You can prepare Rent Agreements, Sale Deeds, Registry documents, Mutation applications, Transfer Memorandums (TM), and Partial Transfer Memorandums (PTM) for properties across GNIDA, Noida Authority, and YEIDA jurisdictions.',
  },
  {
    q: 'How much does it cost to draft a document?',
    a: 'Our pricing starts at ₹299 for basic rent agreements and goes up to ₹1,999 for complete registry and mutation documentation. All prices are transparent with no hidden charges. You only pay after you review the draft.',
  },
  {
    q: 'How quickly will I receive my drafted document?',
    a: 'Most documents are delivered within 20 minutes of order confirmation. Complex documents like registry and mutation may take up to 1 hour. You will receive a notification the moment your draft is ready.',
  },
  {
    q: 'Which authorities accept INSTADEED documents?',
    a: 'Our documents are accepted by GNIDA (Greater Noida Industrial Development Authority), Noida Authority, YEIDA (Yamuna Expressway Industrial Development Authority), and all relevant sub-registrar offices in Gautam Buddha Nagar district.',
  },
  {
    q: 'How long is my document valid?',
    a: 'Rent agreements are valid for the tenancy period mentioned (up to 11 months typically). Registry and mutation documents have permanent validity. Transfer Memorandums remain valid until ownership is legally transferred in authority records.',
  },
  {
    q: 'What payment methods do you accept?',
    a: 'We accept all major payment methods including UPI (Google Pay, PhonePe, Paytm), credit/debit cards, net banking, and NEFT/RTGS. All payments are processed securely through our payment gateway.',
  },
  {
    q: 'Do you offer renewal reminders for expiring documents?',
    a: 'Yes, we send automated reminders 30 days and 7 days before your rent agreement or other time-bound documents expire. You can renew directly from the reminder with one click.',
  },
  {
    q: 'Which areas does INSTADEED currently cover?',
    a: 'We currently cover all sectors and areas under GNIDA, Noida Authority, and YEIDA in Gautam Buddha Nagar, Uttar Pradesh. This includes Greater Noida, Noida, Yamuna Expressway, Jewar, and surrounding regions.',
  },
]

function FaqItem({
  faq,
  isOpen,
  onToggle,
}: {
  faq: (typeof faqs)[number]
  isOpen: boolean
  onToggle: () => void
}) {
  return (
    <div className="border-b border-border last:border-b-0">
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between gap-4 py-5 text-left transition-colors duration-200 hover:text-primary"
      >
        <span className="text-base font-semibold leading-snug text-dark">
          {faq.q}
        </span>
        <motion.span
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.25, ease: 'easeInOut' as const }}
          className="shrink-0 text-muted"
        >
          <ChevronDown className="h-5 w-5" />
        </motion.span>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' as const }}
            className="overflow-hidden"
          >
            <p className="pb-5 leading-relaxed text-muted">{faq.a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function Faq() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  const handleToggle = (index: number) => {
    setOpenIndex((prev) => (prev === index ? null : index))
  }

  return (
    <section id="faq" className="bg-background py-20 sm:py-28">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="mb-14 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-dark sm:text-4xl">
            Frequently Asked Questions
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Everything you need to know about INSTADEED and our document drafting service.
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-card px-6 sm:px-8 shadow-sm">
          {faqs.map((faq, i) => (
            <FaqItem
              key={i}
              faq={faq}
              isOpen={openIndex === i}
              onToggle={() => handleToggle(i)}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
