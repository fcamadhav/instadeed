'use client'

import { ArrowRight, CheckCircle2 } from 'lucide-react'
import { setActiveDoc } from '@/lib/documentState'
import { motion } from 'framer-motion'

export default function FinalCta() {
  return (
    <section className="w-full bg-[#F8FAFC] py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-[2.5rem] bg-gradient-to-r from-primary-dark via-primary to-primary-light px-8 py-12 sm:px-16 sm:py-16 shadow-2xl">
          
          {/* Decorative background paper airplane */}
          <div className="absolute right-0 top-0 opacity-10 transform translate-x-1/3 -translate-y-1/4">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" className="w-96 h-96 text-white"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"></path></svg>
          </div>

          <div className="relative z-10 flex flex-col items-center justify-between gap-12 lg:flex-row">
            
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex-1 w-full flex items-center lg:items-start"
            >
              <img src="/landing/cta_3d.png" alt="Document Ready" className="h-64 w-auto object-contain hidden lg:block mr-8" />
              
              <div className="flex flex-col flex-1">
                <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
                  Ready to Draft Your Documents?
                </h2>
                <p className="mt-4 max-w-xl text-base leading-relaxed text-blue-100/90 font-medium sm:text-lg">
                  Get your legally valid property documents delivered within 20 minutes. No broker, no middleman.
                </p>
                
                <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3">
                  {[
                    '20 Min Delivery',
                    'Lowest Price Guarantee',
                    '100% Legal',
                    'Physical Delivery',
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                      <span className="text-sm font-semibold text-white/90">{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex shrink-0 flex-col sm:flex-row gap-4"
            >
              <button
                onClick={() => setActiveDoc('rent-agreement')}
                className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-8 py-3.5 text-base font-bold text-primary shadow-lg transition-all duration-200 hover:bg-gray-50 hover:shadow-xl active:scale-95"
              >
                Draft Now
                <ArrowRight className="h-5 w-5" />
              </button>
              <a
                href="https://wa.me/918899999321"
                target="_blank"
                className="inline-flex items-center justify-center gap-2 rounded-full border-2 border-white/30 bg-transparent px-8 py-3.5 text-base font-bold text-white transition-all duration-200 hover:bg-white/10 active:scale-95"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                Chat on WhatsApp
              </a>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}
