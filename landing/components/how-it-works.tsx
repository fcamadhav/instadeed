"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import {
  Search,
  Edit3,
  FileCheck,
  CreditCard,
  Truck,
  Bell,
} from "lucide-react";

const steps = [
  {
    icon: Search,
    title: "Choose Service",
    desc: "Select the legal document you need — rent agreement, sale deed, mutation, and more.",
  },
  {
    icon: Edit3,
    title: "Fill Details",
    desc: "Answer a few simple questions in our easy online form. Takes just 2 minutes.",
  },
  {
    icon: FileCheck,
    title: "Review Draft",
    desc: "Our expert team drafts your document. You get a preview to verify before finalising.",
  },
  {
    icon: CreditCard,
    title: "Pay",
    desc: "Secure online payment with zero hidden charges. Starting at just ₹150.",
  },
  {
    icon: Truck,
    title: "Physical Delivery",
    desc: "Get the final signed document delivered to your doorstep anywhere in India.",
  },
  {
    icon: Bell,
    title: "Renewal Reminder",
    desc: "We keep track of expiry dates and notify you before renewal is due.",
  },
];

function StepCard({
  step,
  index,
}: {
  step: (typeof steps)[number];
  index: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <div ref={ref} className="group relative flex items-start gap-5 sm:gap-8">
      <div className="flex flex-col items-center">
        <motion.div
          initial={false}
          animate={isInView ? { scale: 1 } : {}}
          transition={{
            type: "spring" as const,
            damping: 18,
            stiffness: 250,
            delay: 0.1,
          }}
          className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-bold text-white shadow-md shadow-primary/20 sm:h-13 sm:w-13 sm:text-base"
        >
          {index + 1}
        </motion.div>
        {index < steps.length - 1 && (
          <motion.div
            initial={false}
            animate={isInView ? { scaleY: 1 } : {}}
            transition={{ duration: 0.6, delay: 0.25 }}
            className="w-0.5 flex-1 origin-top bg-gradient-to-b from-primary to-blue-200"
            style={{ minHeight: 40 }}
          />
        )}
      </div>

      <motion.div
        initial={false}
        animate={isInView ? { opacity: 1, x: 0 } : {}}
        transition={{
          type: "spring" as const,
          damping: 22,
          stiffness: 280,
          delay: 0.15,
        }}
        className="flex-1 pb-10 sm:pb-14"
        style={{ paddingBottom: index < steps.length - 1 ? undefined : 0 }}
      >
        <div className="rounded-xl border border-border bg-card p-5 transition-shadow duration-300 hover:shadow-md sm:p-6">
          <div className="mb-2 flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10">
              <step.icon
                className="h-4.5 w-4.5 text-primary"
                strokeWidth={1.75}
              />
            </div>
            <h3 className="text-base font-semibold text-dark sm:text-lg">
              {step.title}
            </h3>
          </div>
          <p className="ml-0 text-sm leading-relaxed text-muted sm:ml-12">
            {step.desc}
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="bg-card py-20 sm:py-24">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="mb-16 text-center">
          <motion.span
            initial={false}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-4 inline-block rounded-full bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary"
          >
            Process
          </motion.span>
          <motion.h2
            initial={false}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl font-bold tracking-tight text-dark sm:text-4xl"
          >
            How It <span className="text-primary">Works</span>
          </motion.h2>
          <motion.p
            initial={false}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mx-auto mt-4 max-w-xl text-base text-muted sm:text-lg"
          >
            From selection to doorstep delivery in six simple steps.
          </motion.p>
        </div>

        <div className="relative">
          {steps.map((step, i) => (
            <StepCard key={step.title} step={step} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
