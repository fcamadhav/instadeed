'use client'

import { motion } from 'framer-motion'
import { setActiveDoc } from '@/lib/documentState'
import { FileText, ArrowRight, Star } from 'lucide-react'

interface DraftService {
  name: string; slug: string; description: string;
  price: string; badge: string | null; featured: boolean;
}

const DRAFT_SERVICES: DraftService[] = [
  { name: 'Rent Agreement', slug: 'rent-agreement', description: 'Draft a legally valid rent agreement in minutes.', price: '300', badge: null, featured: true },
  { name: 'Agreement to Sell / ATS', slug: 'ats', description: 'Prepare an Agreement to Sell for property transactions.', price: '300', badge: null, featured: false },
  { name: 'Registered Rent Agreement', slug: 'reg_rent', description: 'Get a registered rental agreement with stamp duty.', price: '5,000', badge: null, featured: true },
  { name: 'Transfer Memorandum / TM', slug: 'tm48', description: 'Draft TM-48 document for leasehold property transfers.', price: '500', badge: null, featured: false },
  { name: 'Mutation Form', slug: 'mutation', description: 'Apply for property mutation with the authority.', price: '4,000', badge: null, featured: false },
  { name: 'GNIDA Flat Registry Deed', slug: 'gnida_registry', description: 'Registry deed for GNIDA flats and apartments.', price: '10,000', badge: null, featured: true },
  { name: 'Permission to Mortgage / PTM', slug: 'gnida_ptm', description: 'Get permission to mortgage your GNIDA property.', price: '7,500', badge: null, featured: false },
  { name: 'GNIDA 5-in-1 Package', slug: 'gnida_package', description: 'Complete GNIDA documentation package.', price: '40,000', badge: 'Best Value', featured: true },
  { name: 'Know Your Allottee / KYA', slug: 'kya', description: 'KYA verification document for property allottees.', price: 'FREE', badge: 'Free', featured: false },
  { name: 'Transfer Memo Application', slug: 'tm_app', description: 'Transfer memo application for authority approval.', price: '2,000', badge: null, featured: false },
  { name: 'Noida Transfer Application', slug: 'noida_transfer', description: 'Noida Authority property transfer application.', price: '2,000', badge: null, featured: false },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.45, ease: 'easeOut' as const } },
}

export default function Services() {
  return (
    <section id="services" className="w-full bg-[#F8FAFC] py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-12 flex flex-col sm:flex-row sm:items-end justify-between gap-6"
        >
          <div>
            <span className="mb-2 inline-block text-xs font-bold uppercase tracking-widest text-primary">WHAT WE OFFER</span>
            <h2 className="text-3xl font-extrabold tracking-tight text-dark sm:text-4xl">All Drafting Services</h2>
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
          {DRAFT_SERVICES.map((service) => (
            <motion.div
              key={service.slug}
              variants={cardVariants}
              className="group relative flex flex-col overflow-hidden rounded-3xl border border-border/50 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl sm:p-7"
            >
              {service.featured && (
                <div className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full bg-rose-100 text-rose-500">
                  <Star className="h-4 w-4 fill-rose-500" />
                </div>
              )}
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-500">
                <FileText className="h-6 w-6" />
              </div>
              <h3 className="mb-1 text-lg font-bold text-dark leading-tight min-h-[50px]">{service.name}</h3>
              <div className="mb-4 flex flex-col">
                <span className="text-xs font-medium text-muted uppercase tracking-wider">Starts at</span>
                <div className="flex items-baseline gap-2">
                  <span className="text-xl font-extrabold text-dark">
                    {service.price === 'FREE' ? 'FREE' : `₹${service.price}`}
                  </span>
                </div>
                {service.badge && (
                  <span className="mt-1 text-xs font-semibold text-green-600">{service.badge}</span>
                )}
              </div>
              <p className="mb-6 text-sm leading-relaxed text-muted font-medium flex-grow">
                {service.description}
              </p>
              <button
                onClick={(e) => { e.stopPropagation(); setActiveDoc(service.slug); }}
                className="mt-auto inline-flex items-center gap-1.5 text-sm font-bold text-primary transition-all duration-200 hover:gap-2.5 cursor-pointer"
              >
                <span>Get Drafted</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
