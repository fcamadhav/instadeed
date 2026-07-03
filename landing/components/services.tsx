'use client'

import { motion } from 'framer-motion'
import { setActiveDoc } from '@/lib/documentState'
import { useState, useEffect } from 'react'
import { FileText, ArrowRight, Star } from 'lucide-react'

interface ApiService {
  id: string; name: string; slug: string; shortDescription: string | null;
  icon: string | null; docKey: string | null; isFeatured: boolean;
  pricing: { currentPrice: number; offerBadge: string | null; oldPrice: number | null } | null;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.45, ease: 'easeOut' as const } },
}

export default function Services() {
  const [services, setServices] = useState<ApiService[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/services?limit=50')
      .then(r => r.json())
      .then(d => setServices(d.data?.services || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

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
            <h2 className="text-3xl font-extrabold tracking-tight text-dark sm:text-4xl">Popular Services</h2>
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-60px' }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
          {loading ? (
            <div className="col-span-full text-center py-10 text-slate-400 text-sm">Loading services...</div>
          ) : services.length === 0 ? (
            <div className="col-span-full text-center py-10 text-slate-400 text-sm">No services available at the moment.</div>
          ) : (
            services.map((service) => (
              <motion.div
                key={service.id}
                variants={cardVariants}
                className="group relative flex flex-col overflow-hidden rounded-3xl border border-border/50 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl sm:p-7"
              >
                {service.isFeatured && (
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
                      ₹{(service.pricing?.currentPrice || 0).toLocaleString('en-IN')}
                    </span>
                    {service.pricing?.oldPrice && service.pricing.oldPrice > (service.pricing?.currentPrice || 0) && (
                      <span className="text-xs text-muted line-through">₹{service.pricing.oldPrice.toLocaleString('en-IN')}</span>
                    )}
                  </div>
                  {service.pricing?.offerBadge && (
                    <span className="mt-1 text-xs font-semibold text-green-600">{service.pricing.offerBadge}</span>
                  )}
                </div>
                <p className="mb-6 text-sm leading-relaxed text-muted font-medium flex-grow">
                  {service.shortDescription || 'Professional legal document drafting service.'}
                </p>
                <button
                  onClick={(e) => { e.stopPropagation(); setActiveDoc(service.slug || service.name.toLowerCase().replace(/\s+/g, '-')); }}
                  className="mt-auto inline-flex items-center gap-1.5 text-sm font-bold text-primary transition-all duration-200 hover:gap-2.5 cursor-pointer"
                >
                  <span>Get Drafted</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </motion.div>
            ))
          )}
        </motion.div>
      </div>
    </section>
  )
}
