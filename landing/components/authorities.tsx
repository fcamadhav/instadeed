'use client'

import { motion } from 'framer-motion'

const authorities = [
  {
    name: 'GNIDA',
    fullName: 'Greater Noida Industrial\nDevelopment Authority',
    initials: 'GN',
    bgColor: 'bg-green-500',
    documents: ['Registry', 'TM', 'Mutation', 'Rent Agreement'],
  },
  {
    name: 'Noida Authority',
    fullName: 'New Okhla Industrial\nDevelopment Authority',
    initials: 'NA',
    bgColor: 'bg-blue-500',
    documents: ['Registry', 'TM', 'Mutation', 'Rent Agreement'],
  },
  {
    name: 'YEIDA',
    fullName: 'Yamuna Expressway Industrial\nDevelopment Authority',
    initials: 'YE',
    bgColor: 'bg-purple-500',
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
    <section id="coverage" className="w-full bg-white py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center sm:mb-16"
        >
          <div className="flex items-center justify-center gap-4 mb-4">
            <div className="hidden sm:block h-px w-12 bg-primary/20 relative">
               <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rotate-45 border-t border-r border-primary/40"></div>
            </div>
            <h2 className="text-3xl font-extrabold tracking-tight text-dark sm:text-4xl">
              Documents Accepted By
            </h2>
            <div className="hidden sm:block h-px w-12 bg-primary/20 relative">
               <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-1.5 -rotate-135 border-t border-r border-primary/40"></div>
            </div>
          </div>
          <p className="mx-auto max-w-2xl text-sm font-medium text-muted sm:text-base">
            We prepare legal documents accepted by all major authorities in the NCR region.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 lg:gap-8"
        >
          {authorities.map((authority) => (
            <motion.div
              key={authority.name}
              variants={cardVariants}
              className="flex flex-col overflow-hidden rounded-2xl border border-border/60 bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-lg sm:p-8"
            >
              <div className="flex items-start gap-4 mb-6">
                <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-lg font-bold text-white shadow-sm ${authority.bgColor}`}>
                  {authority.initials}
                </div>
                <div className="flex flex-col">
                  <h3 className="text-lg font-bold text-dark">{authority.name}</h3>
                  <p className="text-xs font-medium text-muted leading-tight whitespace-pre-line mt-1">
                    {authority.fullName}
                  </p>
                </div>
              </div>

              <div className="mt-auto flex flex-wrap gap-2">
                {authority.documents.map((doc) => (
                  <span
                    key={doc}
                    className="inline-flex items-center rounded-md bg-gray-50 px-2.5 py-1 text-[10px] font-semibold text-muted border border-border/50 uppercase tracking-wider"
                  >
                    {doc}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
