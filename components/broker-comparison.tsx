'use client'

import { motion } from 'framer-motion'
import { X, Check, Building2, Clock, IndianRuprise, AlertTriangle, BellOff, Smartphone, FileText, Zap, IndianRupee, Bell } from 'lucide-react'

const brokerCons = [
  { icon: Building2, label: 'Office Visit' },
  { icon: Clock, label: 'Waiting Days' },
  { icon: IndianRuprise, label: 'High Charges' },
  { icon: AlertTriangle, label: 'Typing Errors' },
  { icon: BellOff, label: 'No Reminder' },
]

const instadeedPros = [
  { icon: Smartphone, label: 'Online' },
  { icon: Zap, label: '5 Minute Draft' },
  { icon: Clock, label: '20 Minute Delivery' },
  { icon: IndianRupee, label: '₹150 Starting' },
  { icon: Bell, label: 'Renewal Reminder' },
]

const floatVariants = {
  animate: {
    y: [-6, 6, -6],
    transition: { duration: 3.5, repeat: Infinity, ease: 'easeInOut' },
  },
}

export default function BrokerComparison() {
  return (
    <section className="py-20 sm:py-24 bg-[#FFFFFF]">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.span
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-block px-4 py-1.5 text-xs font-semibold tracking-wider uppercase text-[#2563EB] bg-[#2563EB]/10 rounded-full mb-4"
          >
            Comparison
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl sm:text-4xl font-bold tracking-tight text-[#0F172A]"
          >
            Broker vs <span className="text-[#2563EB]">INSTADEED</span>
          </motion.h2>
        </div>

        <div className="relative grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] gap-y-8 md:gap-y-0 md:gap-x-8 items-center">
          {/* VS Badge */}
          <div className="absolute left-1/2 top-0 -translate-x-1/2 md:relative md:col-start-2 md:row-start-1 md:col-span-1 md:justify-self-center md:self-center z-10">
            <motion.div
              variants={floatVariants}
              animate="animate"
              className="flex items-center justify-center w-12 h-12 md:w-16 md:h-16 rounded-full bg-[#2563EB] text-white text-sm font-extrabold tracking-wide shadow-lg shadow-[#2563EB]/25"
            >
              VS
            </motion.div>
          </div>

          {/* Broker Column */}
          <div className="md:col-start-1 md:row-start-1 space-y-3">
            <div className="text-center md:text-right mb-6">
              <h3 className="text-2xl font-bold text-[#64748B]">Broker</h3>
              <p className="text-sm text-[#94A3B8] mt-1">Old way</p>
            </div>
            <div className="space-y-3">
              {brokerCons.map((item) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  className="flex items-center gap-3 p-4 bg-[#F1F5F9] rounded-lg border border-[#E5E7EB]"
                >
                  <div className="flex-shrink-0 flex items-center justify-center w-9 h-9 rounded-full bg-[#FEE2E2]">
                    <X className="w-4.5 h-4.5 text-[#EF4444]" strokeWidth={2.5} />
                  </div>
                  <item.icon className="w-4.5 h-4.5 text-[#94A3B8] flex-shrink-0" strokeWidth={1.5} />
                  <span className="text-sm font-medium text-[#64748B]">{item.label}</span>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Spacer on md+ */}
          <div className="hidden md:block md:col-start-2 md:row-start-1" />

          {/* INSTADEED Column */}
          <div className="md:col-start-3 md:row-start-1 space-y-3">
            <div className="text-center md:text-left mb-6">
              <h3 className="text-2xl font-bold text-[#2563EB]">INSTADEED</h3>
              <p className="text-sm text-[#94A3B8] mt-1">New way</p>
            </div>
            <div className="space-y-3">
              {instadeedPros.map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, x: 30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-center gap-3 p-4 bg-[#EFF6FF] rounded-lg border border-[#BFDBFE]"
                >
                  <div className="flex-shrink-0 flex items-center justify-center w-9 h-9 rounded-full bg-[#DCFCE7]">
                    <Check className="w-4.5 h-4.5 text-[#16A34A]" strokeWidth={2.5} />
                  </div>
                  <item.icon className="w-4.5 h-4.5 text-[#2563EB] flex-shrink-0" strokeWidth={1.5} />
                  <span className="text-sm font-semibold text-[#1E40AF]">{item.label}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
