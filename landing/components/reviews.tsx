"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";

const reviews = [
  {
    name: "Ravi Sharma",
    location: "Noida",
    initials: "RS",
    color: "#2563EB",
    rating: 5,
    text: "Got my rent agreement in 15 minutes flat. No broker, no hassle. The document was accepted by the society without any issues. Highly recommended!",
  },
  {
    name: "Priya Verma",
    location: "Greater Noida",
    initials: "PV",
    color: "#16A34A",
    rating: 5,
    text: "I was sceptical at first but the team delivered exactly what they promised. Sale deed was ready in 20 minutes and delivered to my home the next day.",
  },
  {
    name: "Amit Gupta",
    location: "Ghaziabad",
    initials: "AG",
    color: "#8B5CF6",
    rating: 5,
    text: "Best part is no middlemen. I saved ₹3000 compared to what a broker quoted. The draft was perfect and the registrar accepted it without any changes.",
  },
  {
    name: "Sunita Yadav",
    location: "Delhi",
    initials: "SY",
    color: "#F59E0B",
    rating: 4,
    text: "Really smooth experience. The renewal reminder is a lifesaver — I would have completely forgotten about my expiring rental agreement. Thank you!",
  },
  {
    name: "Vikram Singh",
    location: "Noida",
    initials: "VS",
    color: "#EC4899",
    rating: 5,
    text: "Three minutes to fill the form, five minutes for draft review, and the deed was ready. Unbelievable speed. This is the future of legal documentation.",
  },
  {
    name: "Neha Kapoor",
    location: "Ghaziabad",
    initials: "NK",
    color: "#14B8A6",
    rating: 5,
    text: "Affordable, professional, and incredibly fast. The WhatsApp support answered all my queries instantly. Will definitely use again for my renewal.",
  },
];

function Stars({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <Star
          key={i}
          className={`h-4 w-4 ${
            i < count
              ? "fill-amber-400 text-amber-400"
              : "text-border"
          }`}
          strokeWidth={1.5}
        />
      ))}
    </div>
  );
}

const cardVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring" as const, damping: 22, stiffness: 280 },
  },
};

export default function Reviews() {
  return (
    <section className="bg-background py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <motion.span
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-4 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary"
          >
            Testimonials
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold tracking-tight text-dark sm:text-4xl"
          >
            What Our Customers{" "}
            <span className="text-primary">Say</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mx-auto mt-4 max-w-xl text-base text-muted sm:text-lg"
          >
            Real reviews from real customers across Delhi-NCR.
          </motion.p>
        </div>

        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          transition={{ staggerChildren: 0.07 }}
          className="hidden gap-6 sm:grid sm:grid-cols-2"
        >
          {reviews.map((review) => (
            <motion.div
              key={review.name}
              variants={cardVariants}
              className="rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-md hover:shadow-dark/5"
            >
              <div className="flex items-start gap-4">
                <div
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-sm font-bold text-white"
                  style={{ backgroundColor: review.color }}
                >
                  {review.initials}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <h4 className="text-sm font-semibold text-dark">
                        {review.name}
                      </h4>
                      <p className="text-xs text-muted-light">
                        {review.location}
                      </p>
                    </div>
                    <Stars count={review.rating} />
                  </div>
                  <p className="mt-3 text-sm leading-relaxed text-muted">
                    &ldquo;{review.text}&rdquo;
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <div className="-mx-4 overflow-x-auto px-4 pb-4 sm:hidden">
          <div className="flex w-max gap-4">
            {reviews.map((review, i) => (
              <motion.div
                key={review.name}
                initial={{ opacity: 0, x: 40 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
                className="w-[85vw] max-w-sm shrink-0 rounded-xl border border-border bg-card p-5"
              >
                <div className="flex items-start gap-3">
                  <div
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white"
                    style={{ backgroundColor: review.color }}
                  >
                    {review.initials}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <h4 className="text-sm font-semibold text-dark">
                          {review.name}
                        </h4>
                        <p className="text-xs text-muted-light">
                          {review.location}
                        </p>
                      </div>
                      <Stars count={review.rating} />
                    </div>
                    <p className="mt-3 text-sm leading-relaxed text-muted">
                      &ldquo;{review.text}&rdquo;
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
