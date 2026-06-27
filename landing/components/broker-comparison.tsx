"use client";

import { motion } from "framer-motion";
import {
  X,
  Check,
  Building2,
  Clock,
  IndianRupee,
  AlertTriangle,
  BellOff,
  Smartphone,
  Zap,
  Bell,
} from "lucide-react";

const brokerCons = [
  { icon: Building2, label: "Office Visit" },
  { icon: Clock, label: "Waiting Days" },
  { icon: IndianRupee, label: "High Charges" },
  { icon: AlertTriangle, label: "Typing Errors" },
  { icon: BellOff, label: "No Reminder" },
];

const instadeedPros = [
  { icon: Smartphone, label: "Online" },
  { icon: Zap, label: "5 Minute Draft" },
  { icon: Clock, label: "20 Minute Delivery" },
  { icon: IndianRupee, label: "₹150 Starting" },
  { icon: Bell, label: "Renewal Reminder" },
];

const floatVariants = {
  animate: {
    y: [-6, 6, -6],
    transition: { duration: 3.5, repeat: Infinity, ease: "easeInOut" as const },
  },
};

export default function BrokerComparison() {
  return (
    <section id="pricing" className="bg-card py-20 sm:py-24">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <motion.span
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-4 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary"
          >
            Comparison
          </motion.span>
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold tracking-tight text-dark sm:text-4xl"
          >
            Broker vs <span className="text-primary">INSTADEED</span>
          </motion.h2>
        </div>

        <div className="relative grid grid-cols-1 items-center gap-y-8 md:grid-cols-[1fr_auto_1fr] md:gap-x-8 md:gap-y-0">
          <div className="absolute left-1/2 top-0 z-10 -translate-x-1/2 md:relative md:col-span-1 md:col-start-2 md:row-start-1 md:justify-self-center md:self-center">
            <motion.div
              variants={floatVariants}
              animate="animate"
              className="flex h-12 w-12 items-center justify-center rounded-full bg-primary text-sm font-extrabold tracking-wide text-white shadow-lg shadow-primary/25 md:h-16 md:w-16"
            >
              VS
            </motion.div>
          </div>

          <div className="space-y-3 md:col-start-1 md:row-start-1">
            <div className="mb-6 text-center md:text-right">
              <h3 className="text-2xl font-bold text-muted">Broker</h3>
              <p className="mt-1 text-sm text-muted-light">Old way</p>
            </div>
            <div className="space-y-3">
              {brokerCons.map((item) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  className="flex items-center gap-3 rounded-lg border border-border bg-slate-50 p-4"
                >
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-50">
                    <X className="h-4.5 w-4.5 text-red-500" strokeWidth={2.5} />
                  </div>
                  <item.icon className="h-4.5 w-4.5 shrink-0 text-muted-light" strokeWidth={1.5} />
                  <span className="text-sm font-medium text-muted">
                    {item.label}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="hidden md:col-start-2 md:row-start-1 md:block" />

          <div className="space-y-3 md:col-start-3 md:row-start-1">
            <div className="mb-6 text-center md:text-left">
              <h3 className="text-2xl font-bold text-primary">INSTADEED</h3>
              <p className="mt-1 text-sm text-muted-light">New way</p>
            </div>
            <div className="space-y-3">
              {instadeedPros.map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, x: 30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-center gap-3 rounded-lg border border-blue-200 bg-blue-50 p-4"
                >
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-green-50">
                    <Check className="h-4.5 w-4.5 text-success" strokeWidth={2.5} />
                  </div>
                  <item.icon className="h-4.5 w-4.5 shrink-0 text-primary" strokeWidth={1.5} />
                  <span className="text-sm font-semibold text-primary-dark">
                    {item.label}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
