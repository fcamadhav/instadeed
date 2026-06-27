'use client'

import { motion } from 'framer-motion'
import { Clock, IndianRupee, UserX, ShieldCheck, Building2, Bell } from 'lucide-react'

const features = [
  {
    icon: Clock,
    title: '20 Minute Delivery',
    desc: 'Get your legal deed drafted and delivered within 20 minutes. No delays, no excuses.',
    color: '#2563EB',
    bg: '#2563EB10',
  },
  {
    icon: IndianRupee,
    title: 'Lowest Prices',
    desc: 'Starting at just ₹150. No hidden fees, no surprise charges. Transparent pricing guaranteed.',
    color: '#16A34A',
    bg: '#16A34A10',
  },
  {
    icon: UserX,
    title: 'No Broker',
    desc: 'Deal directly with legal professionals. No middlemen, no commission, no inflated costs.',
    color: '#8B5CF6',
    bg: '#8B5CF610',
  },
  {
    icon: ShieldCheck,
    title: 'Legally Valid',
    desc: 'Every deed is vetted by expert legal professionals and compliant with applicable laws.',
    color: '#2563EB',
    bg: '#2563EB10',
  },
  {
    icon: Building2,
    title: 'Accepted Across Authorities',
    desc: 'Our documents are accepted by registrars, banks, and government authorities pan-India.',
    color: '#16A34A',
    bg: '#16A34A10',
  },
  {
    icon: Bell,
    title: 'Renewal Reminder',
    desc: 'Never miss a renewal. We send timely reminders so your deeds stay valid and up-to-date.',
    color: '#F59E0B',
    bg: '#F59E0B10',
  },
]

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1 },
  },
}

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: 'spring', damping: 25, stiffness: 300 },
  },
}

export default function WhyChooseUs() {
  return (
    <section className="py-20 sm:py-24 bg-[#F8FAFC]">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.span
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-block px-4 py-1.5 text-xs font-semibold tracking-wider uppercase text-[#2563EB] bg-[#2563EB]/10 rounded-full mb-4"
          >
            Why Us
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl sm:text-4xl font-bold tracking-tight text-[#0F172A]"
          >
            Why Choose <span className="text-[#2563EB]">INSTADEED</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-[#64748B] max-w-2xl mx-auto"
          >
            We make legal documentation fast, affordable, and hassle-free — so you can focus on what matters.
          </motion.p>
        </div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-50px' }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={cardVariants}
              className="group relative bg-[#FFFFFF] border border-[#E5E7EB] rounded-xl p-6 sm:p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-[#0F172A]/5 cursor-default"
            >
              <div
                className="inline-flex items-center justify-center w-12 h-12 rounded-full mb-4 transition-colors duration-300"
                style={{ backgroundColor: feature.bg }}
              >
                <feature.icon
                  className="w-5.5 h-5.5 transition-transform duration-300 group-hover:scale-110"
                  style={{ color: feature.color }}
                  strokeWidth={1.75}
                />
              </div>
              <h3 className="text-lg font-semibold text-[#0F172A] mb-2">
                {feature.title}
              </h3>
              <p className="text-sm leading-relaxed text-[#64748B]">
                {feature.desc}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
