'use client'

import { motion } from 'framer-motion'
import { Users, Star, Clock, ShieldCheck } from 'lucide-react'

const stats = [
  {
    value: '10,000+',
    label: 'Happy Customers',
    icon: Users,
  },
  {
    value: '4.9',
    label: 'Rating',
    icon: Star,
  },
  {
    value: '20 Min',
    label: 'Delivery',
    icon: Clock,
  },
  {
    value: '100%',
    label: 'Legal',
    icon: ShieldCheck,
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
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut' as const },
  },
}

export default function TrustStrip() {
  return (
    <section className="w-full bg-slate-50 py-14 sm:py-16 lg:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={containerVariants}
          initial={false}
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid grid-cols-2 gap-8 sm:gap-12 lg:grid-cols-4 lg:gap-8"
        >
          {stats.map((stat) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={stat.label}
                variants={itemVariants}
                className="flex flex-col items-center text-center"
              >
                <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary sm:h-14 sm:w-14">
                  <Icon className="h-6 w-6 sm:h-7 sm:w-7" />
                </div>
                <span className="text-2xl font-bold tracking-tight text-dark sm:text-3xl lg:text-4xl">
                  {stat.value}
                </span>
                <span className="mt-1 text-sm font-medium text-muted sm:text-base">
                  {stat.label}
                </span>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
