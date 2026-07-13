'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { setActiveDoc } from '@/lib/documentState'
import { FileText, ArrowRight, Star, Clock } from 'lucide-react'

interface DraftService {
  name: string; slug: string; description: string;
  price: string; badge: string | null; featured: boolean;
}

const GNIDA_SERVICES: DraftService[] = [
  { name: 'Transfer Memorandum / TM', slug: 'tm48', description: 'Draft TM-48 document for leasehold property transfers.', price: '500', badge: null, featured: false },
  { name: 'Mutation Form', slug: 'mutation', description: 'Apply for property mutation with the authority.', price: '4,000', badge: null, featured: false },
  { name: 'GNIDA Flat Registry Deed', slug: 'gnida_registry', description: 'Registry deed for GNIDA flats and apartments.', price: '10,000', badge: null, featured: true },
  { name: 'Permission to Mortgage / PTM', slug: 'gnida_ptm', description: 'Get permission to mortgage your GNIDA property.', price: '7,500', badge: null, featured: false },
  { name: 'GNIDA 5-in-1 Package', slug: 'gnida_package', description: 'Complete GNIDA documentation package.', price: '40,000', badge: 'Best Value', featured: true },
  { name: 'Know Your Allottee / KYA', slug: 'kya', description: 'KYA verification document for property allottees.', price: 'FREE', badge: 'Free', featured: false },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: 'easeOut' as const } },
}

export default function Services() {
  const [activeTab, setActiveTab] = useState<'gnida' | 'noida' | 'yeida'>('gnida')

  return (
    <section id="services" className="w-full bg-[#F8FAFC] py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-10 text-center"
        >
          <span className="mb-2 inline-block text-xs font-bold uppercase tracking-widest text-primary">WHAT WE OFFER</span>
          <h2 className="text-3xl font-extrabold tracking-tight text-dark sm:text-4xl">All Drafting Services</h2>
        </motion.div>

        {/* Tabs */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex flex-wrap justify-center gap-2 bg-white rounded-full p-1.5 shadow-sm border border-gray-200">
            <button
              onClick={() => setActiveTab('gnida')}
              className={`px-6 py-2.5 rounded-full text-sm font-bold transition-all ${
                activeTab === 'gnida' ? 'bg-emerald-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              GNIDA
            </button>
            <button
              onClick={() => setActiveTab('yeida')}
              className={`px-6 py-2.5 rounded-full text-sm font-bold transition-all ${
                activeTab === 'yeida' ? 'bg-purple-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              YEIDA
            </button>
            <button
              onClick={() => setActiveTab('noida')}
              className={`px-6 py-2.5 rounded-full text-sm font-bold transition-all ${
                activeTab === 'noida' ? 'bg-blue-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Noida Authority
            </button>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'gnida' && (
            <motion.div
              key="gnida"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              exit="hidden"
              className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3"
            >
              {GNIDA_SERVICES.map((service) => (
                <motion.div
                  key={service.slug}
                  variants={cardVariants}
                  className="group relative flex flex-col overflow-hidden rounded-3xl border border-border/50 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl sm:p-7 hover:border-emerald-200"
                >
                  {service.featured && (
                    <div className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                      <Star className="h-4 w-4 fill-emerald-500" />
                    </div>
                  )}
                  <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
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
                      <span className="mt-1 text-xs font-semibold text-emerald-600">{service.badge}</span>
                    )}
                  </div>
                  <p className="mb-6 text-sm leading-relaxed text-muted font-medium flex-grow">
                    {service.description}
                  </p>
                  <button
                    onClick={(e) => { e.stopPropagation(); setActiveDoc(service.slug); }}
                    className="mt-auto inline-flex items-center gap-1.5 text-sm font-bold text-emerald-600 transition-all duration-200 hover:gap-2.5 cursor-pointer"
                  >
                    <span>Get Drafted</span>
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </motion.div>
              ))}
            </motion.div>
          )}

          {(activeTab === 'noida' || activeTab === 'yeida') && (
            <motion.div
              key="coming-soon"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
              className="flex flex-col items-center justify-center py-20 px-4 text-center bg-white rounded-3xl border border-dashed border-gray-300"
            >
              <div className="h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center mb-6">
                <Clock className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Coming Soon</h3>
              <p className="text-gray-500 max-w-md mx-auto">
                We are currently integrating specialized drafting services for {activeTab === 'noida' ? 'Noida Authority' : 'YEIDA'}. Check back soon!
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  )
}
