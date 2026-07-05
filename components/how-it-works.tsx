'use client'

import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import { Search, Edit3, FileCheck, CreditCard, Truck, Bell } from 'lucide-react'

const steps = [
  {
    icon: Search,
    title: 'Choose Service',
    desc: 'Select the legal document you need — rent agreement, sale deed, affidavit, and more.',
  },
  {
    icon: Edit3,
    title: 'Fill Details',
    desc: 'Answer a few simple questions in our easy online form. Takes just 2 minutes.',
  },
  {
    icon: FileCheck,
    title: 'Review Draft',
    desc: 'Our expert team drafts your document. You get a preview to verify before finalising.',
  },
  {
    icon: CreditCard,
    title: 'Pay',
    desc: 'Secure online payment with zero hidden charges. Starting at just ₹150.',
  },
  {
    icon: Truck,
    title: 'Physical Delivery',
    desc: 'Get the final signed deed delivered to your doorstep anywhere in India.',
  },
  {
    icon: Bell,
    title: 'Renewal Reminder',
    desc: 'We keep track of expiry dates and notify you before renewal is due.',
  },
]

function StepCard({
  step,
  index,
}: {
  step: (typeof steps)[number]
  index: number
}) {
  const ref = useRef<HTMLDivElement>(null)
  const isInView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <div ref={ref} className="relative flex items-start gap-5 sm:gap-8 group">
      {/* Timeline connector */}
      <div className="flex flex-col items-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={isInView ? { scale: 1 } : {}}
          transition={{ type: 'spring', damping: 18, stiffness: 250, delay: 0.1 }}
          className="relative z-10 flex items-center justify-center w-11 h-11 sm:w-13 sm:h-13 rounded-full bg-[#2563EB] text-white text-sm sm:text-base font-bold shadow-md shadow-[#2563EB]/20"
          style={{ width: 48, height: 48, minWidth: 48, minHeight: 48 }}
        >
          {index + 1}
        </motion.div>
        {index < steps.length - 1 && (
          <motion.div
            initial={{ scaleY: 0 }}
            animate={isInView ? { scaleY: 1 } : {}}
            transition={{ duration: 0.6, delay: 0.25 }}
            className="w-0.5 flex-1 bg-gradient-to-b from-[#2563EB] to-[#BFDBFE] origin-top"
            style={{ minHeight: 40 }}
          />
        )}
      </div>

      {/* Content */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={isInView ? { opacity: 1, x: 0 } : {}}
        transition={{ type: 'spring', damping: 22, stiffness: 280, delay: 0.15 }}
        className="flex-1 pb-10 sm:pb-14"
        style={{ paddingBottom: index < steps.length - 1 ? undefined : 0 }}
      >
        <div className="bg-[#FFFFFF] border border-[#E5E7EB] rounded-xl p-5 sm:p-6 transition-shadow duration-300 hover:shadow-md">
          <div className="flex items-center gap-3 mb-2">
            <div className="flex items-center justify-center w-9 h-9 rounded-full bg-[#2563EB]/10">
              <step.icon className="w-4.5 h-4.5 text-[#2563EB]" strokeWidth={1.75} />
            </div>
            <h3 className="text-base sm:text-lg font-semibold text-[#0F172A]">{step.title}</h3>
          </div>
          <p className="text-sm leading-relaxed text-[#64748B] ml-0 sm:ml-12">{step.desc}</p>
        </div>
      </motion.div>
    </div>
  )
}

export default function HowItWorks() {
  return (
    <section className="py-20 sm:py-24 bg-[#FFFFFF]">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.span
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-block px-4 py-1.5 text-xs font-semibold tracking-wider uppercase text-[#2563EB] bg-[#2563EB]/10 rounded-full mb-4"
          >
            Process
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl sm:text-4xl font-bold tracking-tight text-[#0F172A]"
          >
            How It <span className="text-[#2563EB]">Works</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-[#64748B] max-w-xl mx-auto"
          >
            From selection to doorstep delivery in six simple steps.
          </motion.p>
        </div>

        <div className="relative">
          {steps.map((step, i) => (
            <StepCard key={step.title} step={step} index={i} />
          ))}
        </div>
      </div>
    </section>
  )
}
