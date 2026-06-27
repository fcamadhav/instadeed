'use client'

import { motion } from 'framer-motion'
import {
  FileText,
  Stamp,
  FileSignature,
  Landmark,
  Building,
  ScrollText,
  Map,
} from 'lucide-react'

const services = [
  {
    name: 'Rent Agreement',
    price: 150,
    description:
      'Unregistered rental agreement for residential or commercial use. Fast & affordable.',
    icon: FileText,
    featured: true,
    href: '/app/?doc=rent-agreement',
  },
  {
    name: 'Registered Rent Agreement',
    price: 2000,
    description:
      'Notarized and registered rental agreement with full legal validity.',
    icon: Stamp,
    featured: false,
    href: '/app/?doc=registered-rent',
  },
  {
    name: 'Agreement to Sell / ATS',
    price: 150,
    description:
      'Legally enforceable promise to sell a property between buyer and seller.',
    icon: FileSignature,
    featured: false,
    href: '/app/?doc=ats',
  },
  {
    name: 'Transfer Memorandum / TM',
    price: 2000,
    description:
      'Official document recording the transfer of property ownership rights.',
    icon: Landmark,
    featured: false,
    href: '/app/?doc=tm48',
  },
  {
    name: 'Registry',
    price: 5000,
    description:
      'Full property sale deed registration with the sub-registrar office.',
    icon: Building,
    featured: false,
    href: '/app/?doc=registry',
  },
  {
    name: 'Permission to Mortgage / PTM',
    price: 9000,
    description:
      'Authority permission document for mortgaging a property against a loan.',
    icon: ScrollText,
    featured: false,
    href: '/app/?doc=ptm',
  },
  {
    name: 'Mutation',
    price: 3500,
    description:
      'Updating property title records with the local municipal authority.',
    icon: Map,
    featured: false,
    href: '/app/?doc=mutation',
  },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
}

const cardVariants = {
  hidden: { opacity: 0, y: 28 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.45, ease: 'easeOut' as const },
  },
}

export default function Services() {
  return (
    <section className="w-full bg-slate-50 py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-12 text-center sm:mb-16"
        >
          <span className="mb-3 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary">
            What We Offer
          </span>
          <h2 className="text-3xl font-bold tracking-tight text-dark sm:text-4xl lg:text-5xl">
            Popular Services
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base text-muted sm:text-lg">
            Affordable legal document drafting services with fast turnaround and
            100% accuracy.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
          {services.map((service) => {
            const Icon = service.icon
            const isFeatured = service.featured

            return (
              <motion.div
                key={service.name}
                variants={cardVariants}
                className={`group relative overflow-hidden rounded-2xl border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:shadow-lg sm:p-7 ${
                  isFeatured
                    ? 'border-primary shadow-primary/5 ring-1 ring-primary/20'
                    : 'border-border'
                }`}
              >
                {isFeatured && (
                  <>
                    <div className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/[0.04] to-transparent" />
                    </div>
                    <span className="absolute right-3 top-3 rounded-full bg-primary/10 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-primary sm:right-4 sm:top-4">
                      Popular
                    </span>
                  </>
                )}

                <div className="relative mb-4 flex items-center gap-3">
                  <div
                    className={`flex h-11 w-11 items-center justify-center rounded-xl sm:h-12 sm:w-12 ${
                      isFeatured
                        ? 'bg-primary text-white shadow-md shadow-primary/20'
                        : 'bg-primary/10 text-primary'
                    }`}
                  >
                    <Icon className="h-5 w-5 sm:h-5.5 sm:w-5.5" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-dark sm:text-lg">
                      {service.name}
                    </h3>
                    <span className="text-sm font-semibold text-primary">
                      ₹{service.price.toLocaleString('en-IN')}
                    </span>
                  </div>
                </div>

                <p className="relative text-sm leading-relaxed text-muted">
                  {service.description}
                </p>

                <a
                  href={service.href}
                  className="relative mt-5 flex items-center gap-1 text-sm font-medium text-primary transition-all duration-200 hover:gap-2"
                >
                  <span>Get Drafted</span>
                  <svg
                    className="h-4 w-4 transition-transform duration-200 hover:translate-x-0.5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3"
                    />
                  </svg>
                </a>
              </motion.div>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
