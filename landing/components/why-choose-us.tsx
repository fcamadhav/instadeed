"use client";

import { motion } from "framer-motion";
import {
  Clock,
  IndianRupee,
  UserX,
  ShieldCheck,
  Building2,
  Bell,
} from "lucide-react";

const features = [
  {
    icon: Clock,
    title: "20 Minute Delivery",
    desc: "Get your legal document drafted and delivered within 20 minutes. No delays, no excuses.",
    color: "#2563EB",
  },
  {
    icon: IndianRupee,
    title: "Lowest Prices",
    desc: "Starting at just ₹150. No hidden fees, no surprise charges. Transparent pricing guaranteed.",
    color: "#16A34A",
  },
  {
    icon: UserX,
    title: "No Broker",
    desc: "Deal directly with legal professionals. No middlemen, no commission, no inflated costs.",
    color: "#8B5CF6",
  },
  {
    icon: ShieldCheck,
    title: "Legally Valid",
    desc: "Every document is vetted by expert legal professionals and compliant with applicable laws.",
    color: "#2563EB",
  },
  {
    icon: Building2,
    title: "Accepted Across Authorities",
    desc: "Our documents are accepted by registrars, banks, and government authorities across NCR.",
    color: "#16A34A",
  },
  {
    icon: Bell,
    title: "Renewal Reminder",
    desc: "Never miss a renewal. We send timely reminders so your documents stay valid and up-to-date.",
    color: "#F59E0B",
  },
];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring" as const, damping: 25, stiffness: 300 },
  },
};

export default function WhyChooseUs() {
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
            Why Us
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold tracking-tight text-dark sm:text-4xl"
          >
            Why Choose <span className="text-primary">INSTADEED</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mx-auto mt-4 max-w-2xl text-base text-muted sm:text-lg"
          >
            We make legal documentation fast, affordable, and hassle-free — so
            you can focus on what matters.
          </motion.p>
        </div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={cardVariants}
              className="group cursor-default rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-dark/5 sm:p-7"
            >
              <div
                className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-full transition-colors duration-300"
                style={{ backgroundColor: `${feature.color}10` }}
              >
                <feature.icon
                  className="h-5.5 w-5.5 transition-transform duration-300 group-hover:scale-110"
                  style={{ color: feature.color }}
                  strokeWidth={1.75}
                />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-dark">
                {feature.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted">
                {feature.desc}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
