'use client'

import { motion } from 'framer-motion'
import { Users, Star, Clock, ShieldCheck } from 'lucide-react'

const stats = [
  {
    value: 'Fast',
    label: 'Delivery',
    icon: Clock,
  },
  {
    value: 'Easy',
    label: 'Online Process',
    icon: Users,
  },
  {
    value: 'Expert',
    label: 'Legal Support',
    icon: Star,
  },
  {
    value: '100%',
    label: 'Legal & Secure',
    icon: ShieldCheck,
  },
]

const containerVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { staggerChildren: 0.1, duration: 0.6, ease: 'easeOut' as const },
  },
}

const itemVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.4, ease: 'easeOut' as const },
  },
}

export default function TrustStrip() {
  return (
    <section className="w-full bg-white pb-12 pt-0 sm:pb-16 sm:pt-4">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-40px' }}
          className="mx-auto flex flex-col sm:flex-row items-center justify-between gap-8 sm:gap-4 rounded-3xl border border-border/60 bg-white px-8 py-6 shadow-xl shadow-primary/5 lg:px-12"
        >
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={stat.label}
                variants={itemVariants}
                className="flex items-center gap-4 sm:w-1/4 sm:justify-center"
              >
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary border border-primary/20">
                  <Icon className="h-6 w-6" />
                </div>
                <div className="flex flex-col text-left">
                  <span className="text-xl font-extrabold text-dark tracking-tight">
                    {stat.value}
                  </span>
                  <span className="text-xs font-semibold text-muted">
                    {stat.label}
                  </span>
                </div>
                {/* Vertical Divider for all but last item on desktop */}
                {index !== stats.length - 1 && (
                  <div className="hidden sm:block h-10 w-px bg-border ml-auto opacity-50" />
                )}
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
