'use client'

import { motion } from 'framer-motion'
import { CheckCircle2, X, Check, Star } from 'lucide-react'

const features = [
  '20 Minute Delivery',
  'Lowest Prices Starting at ₹150',
  'No Broker, No Hidden Charges',
  'Legally Valid & Error Free',
  'Accepted Across All Authorities',
  'Renewal Reminders on Time',
]

const comparison = [
  { broker: 'Office Visit', instadeed: 'Online, From Anywhere' },
  { broker: 'Waiting for Days', instadeed: '5 Min Draft' },
  { broker: 'High Charges', instadeed: '20 Min Delivery' },
  { broker: 'Typing Errors', instadeed: '₹150 Starting' },
  { broker: 'No Reminder', instadeed: 'Renewal Reminder' },
]

export default function WhyChooseUs() {
  return (
    <section className="w-full bg-[#F8FAFC] py-16 sm:py-20 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-3">
          
          {/* Column 1: Why Choose */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="flex flex-col rounded-3xl bg-white p-8 shadow-sm border border-border/50 relative overflow-hidden"
          >
            <h3 className="mb-8 text-xl font-extrabold text-dark tracking-tight">
              Why Choose <span className="text-primary">INSTADEED</span>?
            </h3>
            <ul className="flex flex-col gap-5 z-10">
              {features.map((feature, i) => (
                <li key={i} className="flex items-center gap-3">
                  <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-emerald-500">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>
                  <span className="text-sm font-semibold text-dark">{feature}</span>
                </li>
              ))}
            </ul>
            <div className="absolute -bottom-6 -right-6 h-32 w-32 rounded-full bg-primary/10 flex items-center justify-center">
               <div className="h-16 w-16 bg-primary rounded-xl rotate-12 flex items-center justify-center text-white shadow-lg">
                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
               </div>
            </div>
          </motion.div>

          {/* Column 2: Broker vs INSTADEED */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="flex flex-col rounded-3xl bg-white p-8 shadow-sm border border-border/50"
          >
            <h3 className="mb-8 text-xl font-extrabold text-dark text-center tracking-tight">
              Broker <span className="text-muted text-sm font-medium mx-1">vs</span> <span className="text-primary">INSTADEED</span>
            </h3>
            
            <div className="flex justify-between mb-4 px-2">
              <span className="text-xs font-bold text-rose-500 uppercase tracking-wide">Broker <span className="text-muted">(Old Way)</span></span>
              <span className="text-xs font-bold text-emerald-500 uppercase tracking-wide">INSTADEED <span className="text-muted">(New Way)</span></span>
            </div>

            <div className="flex flex-col gap-4 relative">
              {/* VS badge in middle */}
              <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-8 w-8 rounded-full bg-primary text-white text-[10px] font-bold flex items-center justify-center shadow-md z-10 ring-4 ring-white">
                VS
              </div>
              
              {comparison.map((row, i) => (
                <div key={i} className="flex justify-between items-center rounded-lg bg-gray-50/50 p-3 text-sm">
                  <div className="flex items-center gap-2 w-[45%] text-muted font-medium">
                    <X className="h-4 w-4 text-rose-400 shrink-0" strokeWidth={3} />
                    <span className="truncate text-xs">{row.broker}</span>
                  </div>
                  <div className="flex items-center gap-2 w-[45%] text-dark font-semibold justify-end text-right">
                    <span className="truncate text-xs">{row.instadeed}</span>
                    <Check className="h-4 w-4 text-emerald-500 shrink-0" strokeWidth={3} />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Column 3: What Customers Say */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col rounded-3xl bg-white p-8 shadow-sm border border-border/50 text-center items-center justify-center"
          >
            <h3 className="mb-6 text-xl font-extrabold text-dark tracking-tight w-full text-left">
              What Customers Say
            </h3>
            
            <div className="flex items-end gap-3 mb-2">
              <span className="text-4xl font-black text-dark">4.9/5</span>
              <div className="flex gap-1 pb-1">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Star key={s} className="h-5 w-5 fill-amber-400 text-amber-400" />
                ))}
              </div>
            </div>
            <p className="text-xs font-semibold text-muted mb-8 w-full text-left">
              Based on 10,000+ reviews
            </p>

            <blockquote className="text-sm font-semibold text-dark/80 italic mb-4">
              "Got my rent agreement in 15 minutes. Super fast and hassle free!"
            </blockquote>
            <p className="text-xs font-bold text-muted text-right w-full mb-8">
              – Ravi Sharma, Noida
            </p>

            <div className="flex items-center gap-3 w-full border-t border-border/50 pt-6">
              <div className="flex -space-x-3">
                <img src="https://i.pravatar.cc/100?img=11" alt="User" className="h-8 w-8 rounded-full border-2 border-white" />
                <img src="https://i.pravatar.cc/100?img=32" alt="User" className="h-8 w-8 rounded-full border-2 border-white" />
                <img src="https://i.pravatar.cc/100?img=47" alt="User" className="h-8 w-8 rounded-full border-2 border-white" />
              </div>
              <span className="text-xs font-bold text-dark">10K+ Happy Customers</span>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  )
}
