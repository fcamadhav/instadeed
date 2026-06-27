'use client'

import { motion } from 'framer-motion'
import { Building2, Landmark, ScrollText, Check } from 'lucide-react'

const authorities = [
  {
    name: 'GNIDA',
    fullName: 'Greater Noida Industrial Development Authority',
    icon: Building2,
    gradient: 'from-emerald-500/20 to-emerald-600/10',
    borderGlow: 'shadow-emerald-500/10',
    initials: 'GN',
    documents: ['Registry', 'TM', 'Mutation', 'Rent Agreement'],
  },
  {
    name: 'Noida Authority',
    fullName: 'New Okhla Industrial Development Authority',
    icon: Landmark,
    gradient: 'from-blue-500/20 to-blue-600/10',
    borderGlow: 'shadow-blue-500/10',
    initials: 'NA',
    documents: ['Registry', 'TM', 'Mutation', 'Rent Agreement'],
  },
  {
    name: 'YEIDA',
    fullName: 'Yamuna Expressway Industrial Development Authority',
    icon: ScrollText,
    gradient: 'from-violet-500/20 to-violet-600/10',
    borderGlow: 'shadow-violet-500/10',
    initials: 'YE',
    documents: ['Registry', 'TM', 'Mutation', 'Rent Agreement'],
  },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12 },
  },
}

const cardVariants = {
  hidden: { opacity: 0, y: 32 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut' as const },
  },
}

export default function Authorities() {
  return (
    <section className="w-full bg-background py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center sm:mb-16"
        >
          <span className="mb-3 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary">
            Trusted By
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-dark sm:text-4xl lg:text-5xl">
            Documents Accepted By
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base text-muted sm:text-lg">
            We prepare legal documents accepted by all major authorities in the
            NCR region.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 lg:gap-8"
        >
          {authorities.map((authority) => {
            const Icon = authority.icon
            return (
              <motion.div
                key={authority.name}
                variants={cardVariants}
                className="group relative overflow-hidden rounded-2xl border border-border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl sm:p-8"
              >
                {/* Gradient border overlay */}
                <div
                  className={`pointer-events-none absolute inset-0 rounded-2xl bg-gradient-to-b ${authority.gradient} opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
                />

                {/* Top section */}
                <div className="relative mb-6 flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-dark text-lg font-bold tracking-wide text-white shadow-md sm:h-16 sm:w-16 sm:text-xl">
                    {authority.initials}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-dark sm:text-xl">
                      {authority.name}
                    </h3>
                    <p className="mt-0.5 text-sm text-muted">
                      {authority.fullName}
                    </p>
                  </div>
                  <Icon className="h-6 w-6 text-muted-light transition-colors duration-300 group-hover:text-primary" />
                </div>

                {/* Divider */}
                <div className="relative mb-5 h-px bg-border" />

                {/* Documents list */}
                <ul className="relative space-y-2.5">
                  {authority.documents.map((doc) => (
                    <li
                      key={doc}
                      className="flex items-center gap-3 text-sm font-medium text-dark-light sm:text-base"
                    >
                      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-success/10 text-success">
                        <Check className="h-3 w-3" />
                      </span>
                      {doc}
                    </li>
                  ))}
                </ul>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
