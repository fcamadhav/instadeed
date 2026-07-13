"use client";

import { motion } from "framer-motion";
import {
  Clock,
  IndianRupee,
  Shield,
  Truck,
  FileText,
  Star,
  Users,
} from "lucide-react";
import { setActiveDoc } from "@/lib/documentState";

const trusts = [
  { text: "20 Min Delivery", icon: Clock },
  { text: "Lowest Price", icon: IndianRupee },
  { text: "No Broker", icon: Users },
  { text: "Physical Delivery", icon: Truck },
  { text: "Renewal Reminder", icon: Clock },
  { text: "100% Legal", icon: Shield },
];

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 },
  },
};

const itemLeft = {
  hidden: { opacity: 0, x: -40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6, ease: "easeOut" as const } },
};

const itemRight = {
  hidden: { opacity: 0, x: 40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6, ease: "easeOut" as const } },
};

const floatAnimation = {
  y: [0, -10, 0],
  transition: { duration: 4, repeat: Infinity, ease: "easeInOut" as const },
};

export default function Hero() {
  return (
    <section id="home" className="relative min-h-screen overflow-hidden bg-gradient-to-b from-[#EFF6FF] to-white pt-24 sm:pt-28 lg:pt-32">
      <div className="absolute top-0 right-0 -z-10 h-full w-full opacity-30" style={{ backgroundImage: 'radial-gradient(#93C5FD 1px, transparent 1px)', backgroundSize: '24px 24px' }}></div>
      
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid items-center gap-12 lg:grid-cols-12 lg:gap-8">
          <motion.div
            variants={container}
            initial="hidden"
            animate="visible"
            className="lg:col-span-6 z-10"
          >
            <motion.div variants={itemLeft} className="mb-6">
              <span className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-white px-4 py-1.5 text-xs font-semibold tracking-wider text-primary shadow-sm">
                Gautam Buddha Nagar&apos;s Most Trusted Platform
              </span>
            </motion.div>

            <motion.h1
              variants={itemLeft}
              className="text-5xl font-extrabold leading-tight tracking-tight text-dark sm:text-6xl lg:text-7xl"
            >
              GNIDA, YEIDA &<br />
              Noida Authority<br />
              Documentation in <span className="text-primary">20 Mins</span>.
            </motion.h1>

            <motion.p
              variants={itemLeft}
              className="mt-6 max-w-lg text-base leading-relaxed text-muted font-medium sm:text-lg"
            >
              Legally valid documents accepted by GNIDA, Noida Authority &amp; YEIDA.<br />
              No Broker. No Middleman. Physical Delivery.<br />
              Lowest Price Guaranteed.
            </motion.p>

            <motion.div
              variants={itemLeft}
              className="mt-8 flex flex-col gap-4 sm:flex-row"
            >
              <button
                onClick={() => setActiveDoc('rent-agreement')}
                className="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-8 py-3.5 text-base font-bold text-white shadow-lg shadow-primary/30 transition-all duration-200 hover:bg-primary-dark hover:shadow-xl active:scale-95"
              >
                Draft Your Document Now
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
              </button>
              <a
                href="#pricing"
                className="inline-flex items-center justify-center gap-2 rounded-full border-2 border-primary/20 bg-white px-8 py-3.5 text-base font-bold text-primary transition-all duration-200 hover:border-primary/40 hover:bg-primary/5 active:scale-95"
              >
                View Pricing
              </a>
            </motion.div>

            <motion.div
              variants={itemLeft}
              className="mt-12 grid grid-cols-3 gap-y-6 sm:flex sm:flex-wrap sm:gap-6"
            >
              {trusts.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <div key={idx} className="flex flex-col items-center gap-2 text-center sm:flex-col sm:items-center">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary">
                      <Icon className="h-5 w-5" />
                    </div>
                    <span className="text-xs font-semibold text-dark">{item.text}</span>
                  </div>
                );
              })}
            </motion.div>
          </motion.div>

          <motion.div
            variants={itemRight}
            initial="hidden"
            animate="visible"
            className="relative lg:col-span-6 flex justify-center lg:justify-end mt-12 lg:mt-0"
          >
            <div className="relative w-full max-w-[600px]">
              <img src="/landing/hero_3d.webp" alt="3D Hero Graphic" fetchPriority="high" loading="eager" className="w-full h-auto object-contain z-0 relative" />
              
              {/* Floating Badges */}
              <motion.div
                animate={floatAnimation}
                className="absolute -right-4 top-10 z-10 flex flex-col items-center justify-center rounded-2xl bg-white p-4 shadow-xl shadow-primary/10 sm:right-4 border border-border/50"
              >
                <span className="text-xs font-bold text-muted uppercase">Starting at</span>
                <span className="text-3xl font-black text-dark tracking-tight"><span className="text-primary">₹</span>150</span>
                <span className="text-xs font-bold text-muted">Only</span>
              </motion.div>

              <motion.div
                animate={floatAnimation}
                style={{ animationDelay: "1s" }}
                className="absolute bottom-10 left-0 sm:-left-10 z-10 flex items-center gap-4 rounded-full bg-white px-6 py-3 shadow-xl shadow-primary/10 border border-border/50"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <Clock className="h-5 w-5" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs font-bold text-muted uppercase">Delivered Within</span>
                  <span className="text-lg font-black text-dark">20 MINUTES</span>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
