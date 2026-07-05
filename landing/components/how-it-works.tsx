'use client'

import { motion } from 'framer-motion'
import {
  Hand,
  FileEdit,
  FileCheck2,
  CreditCard,
  Truck,
  BellRing,
} from 'lucide-react'

const steps = [
  {
    title: 'Choose Service',
    description: 'Select the document you need.',
    icon: Hand,
  },
  {
    title: 'Fill Details',
    description: 'Answer a few simple questions.',
    icon: FileEdit,
  },
  {
    title: 'Review Draft',
    description: 'We create your draft. You review & approve.',
    icon: FileCheck2,
  },
  {
    title: 'Pay Securely',
    description: 'Pay online securely. Starting at ₹150.',
    icon: CreditCard,
  },
  {
    title: 'Physical Delivery',
    description: 'Get the final document delivered to your door.',
    icon: Truck,
  },
  {
    title: 'Renewal Reminder',
    description: 'We remind you before your document expires.',
    icon: BellRing,
  },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: 'easeOut' as const },
  },
}

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="w-full bg-white py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-16 text-center"
        >
          <span className="mb-2 inline-block text-xs font-bold uppercase tracking-widest text-primary">
            HOW IT WORKS
          </span>
          <div className="flex items-center justify-center gap-4">
            <h2 className="text-xl font-bold tracking-tight text-dark sm:text-2xl">
              From selection to doorstep delivery in 6 simple steps
            </h2>
            <div className="hidden sm:block h-px w-24 bg-border/50 relative">
               <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rotate-45 border-t border-r border-border/80"></div>
            </div>
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-6 lg:gap-4 relative"
        >
          {steps.map((step, index) => {
            const Icon = step.icon
            return (
              <motion.div
                key={step.title}
                variants={itemVariants}
                className="relative flex flex-col items-center text-center group"
              >
                {/* Connecting Line for desktop */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute right-0 top-10 w-full h-px border-t border-dashed border-primary/20 -z-10 translate-x-1/2">
                    <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rotate-45 border-t border-r border-primary/40 bg-white"></div>
                  </div>
                )}
                
                <div className="relative mb-6">
                  <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/5 text-primary shadow-sm border border-primary/10 transition-transform duration-300 group-hover:scale-110 group-hover:bg-primary/10">
                    <Icon className="h-8 w-8" strokeWidth={1.5} />
                  </div>
                  <div className="absolute -bottom-2 -right-2 flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-bold text-white shadow-sm ring-2 ring-white">
                    {index + 1}
                  </div>
                </div>
                
                <h3 className="mb-2 text-sm font-extrabold text-dark tracking-tight">
                  {step.title}
                </h3>
                <p className="text-[11px] font-medium leading-relaxed text-muted max-w-[140px]">
                  {step.description}
                </p>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
