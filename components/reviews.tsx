'use client'

import { motion } from 'framer-motion'
import { Star } from 'lucide-react'

const reviews = [
  {
    name: 'Ravi Sharma',
    location: 'Noida',
    initials: 'RS',
    color: '#2563EB',
    rating: 5,
    text: 'Got my rent agreement in 15 minutes flat. No broker, no hassle. The document was accepted by the society without any issues. Highly recommended!',
  },
  {
    name: 'Priya Verma',
    location: 'Greater Noida',
    initials: 'PV',
    color: '#16A34A',
    rating: 5,
    text: 'I was sceptical at first but the team delivered exactly what they promised. Sale deed was ready in 20 minutes and delivered to my home the next day.',
  },
  {
    name: 'Amit Gupta',
    location: 'Ghaziabad',
    initials: 'AG',
    color: '#8B5CF6',
    rating: 5,
    text: 'Best part is no middlemen. I saved ₹3000 compared to what a broker quoted. The draft was perfect and the registrar accepted it without any changes.',
  },
  {
    name: 'Sunita Yadav',
    location: 'Delhi',
    initials: 'SY',
    color: '#F59E0B',
    rating: 4,
    text: 'Really smooth experience. The renewal reminder is a lifesaver — I would have completely forgotten about my expiring rental agreement. Thank you!',
  },
  {
    name: 'Vikram Singh',
    location: 'Noida',
    initials: 'VS',
    color: '#EC4899',
    rating: 5,
    text: 'Three minutes to fill the form, five minutes for draft review, and the deed was ready. Unbelievable speed. This is the future of legal documentation.',
  },
  {
    name: 'Neha Kapoor',
    location: 'Ghaziabad',
    initials: 'NK',
    color: '#14B8A6',
    rating: 5,
    text: 'Affordable, professional, and incredibly fast. The WhatsApp support answered all my queries instantly. Will definitely use again for my renewal.',
  },
]

function Stars({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <Star
          key={i}
          className={`w-4 h-4 ${i < count ? 'text-[#F59E0B] fill-[#F59E0B]' : 'text-[#E5E7EB]'}`}
          strokeWidth={1.5}
        />
      ))}
    </div>
  )
}

const cardVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: 'spring', damping: 22, stiffness: 280 },
  },
}

export default function Reviews() {
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
            Testimonials
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl sm:text-4xl font-bold tracking-tight text-[#0F172A]"
          >
            What Our Customers <span className="text-[#2563EB]">Say</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-[#64748B] max-w-xl mx-auto"
          >
            Real reviews from real customers across Delhi-NCR.
          </motion.p>
        </div>

        {/* Desktop grid */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-50px' }}
          transition={{ staggerChildren: 0.07 }}
          className="hidden sm:grid sm:grid-cols-2 gap-6"
        >
          {reviews.map((review) => (
            <motion.div
              key={review.name}
              variants={cardVariants}
              className="bg-[#FFFFFF] border border-[#E5E7EB] rounded-xl p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-md hover:shadow-[#0F172A]/5"
            >
              <div className="flex items-start gap-4">
                <div
                  className="flex-shrink-0 flex items-center justify-center w-11 h-11 rounded-full text-white text-sm font-bold"
                  style={{ backgroundColor: review.color }}
                >
                  {review.initials}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <div>
                      <h4 className="text-sm font-semibold text-[#0F172A]">{review.name}</h4>
                      <p className="text-xs text-[#94A3B8]">{review.location}</p>
                    </div>
                    <Stars count={review.rating} />
                  </div>
                  <p className="mt-3 text-sm leading-relaxed text-[#64748B]">&ldquo;{review.text}&rdquo;</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Mobile horizontal scroll */}
        <div className="sm:hidden overflow-x-auto -mx-4 px-4 pb-4 scrollbar-none snap-x snap-mandatory scroll-smooth">
          <div className="flex gap-4 w-max">
            {reviews.map((review, i) => (
              <motion.div
                key={review.name}
                initial={{ opacity: 0, x: 40 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
                className="snap-start w-[85vw] max-w-sm flex-shrink-0 bg-[#FFFFFF] border border-[#E5E7EB] rounded-xl p-5"
              >
                <div className="flex items-start gap-3">
                  <div
                    className="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-full text-white text-xs font-bold"
                    style={{ backgroundColor: review.color }}
                  >
                    {review.initials}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <div>
                        <h4 className="text-sm font-semibold text-[#0F172A]">{review.name}</h4>
                        <p className="text-xs text-[#94A3B8]">{review.location}</p>
                      </div>
                      <Stars count={review.rating} />
                    </div>
                    <p className="mt-3 text-sm leading-relaxed text-[#64748B]">&ldquo;{review.text}&rdquo;</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
