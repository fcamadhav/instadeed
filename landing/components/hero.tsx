"use client";

import { motion } from "framer-motion";
import {
  Check,
  Clock,
  IndianRupee,
  MapPin,
  Shield,
  Truck,
  Building,
  FileText,
  Smartphone,
  Star,
} from "lucide-react";
import { setActiveDoc } from "@/lib/documentState";

const trusts = [
  "Physical Delivery",
  "Lowest Price",
  "Renewal Reminder",
  "Accepted Documents",
  "Error Free",
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
    <section id="home" className="relative min-h-screen overflow-hidden bg-gradient-to-b from-background to-white pt-24 sm:pt-28 lg:pt-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid items-center gap-12 lg:grid-cols-12 lg:gap-16">
          <motion.div
            variants={container}
            initial={false}
            animate="visible"
            className="lg:col-span-6"
          >
            <motion.div variants={itemLeft} className="mb-6">
              <span className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary">
                <Star className="h-3.5 w-3.5 fill-primary/20" />
                Gautam Buddha Nagar&apos;s Most Trusted Document Platform
              </span>
            </motion.div>

            <motion.h1
              variants={itemLeft}
              className="text-4xl font-bold leading-tight tracking-tight text-dark sm:text-5xl lg:text-6xl"
            >
              One Platform.
              <br />
              <span className="text-primary">All Property Documents.</span>
              <br />
              Delivered Within{" "}
              <span className="text-primary">20 Minutes.</span>
            </motion.h1>

            <motion.p
              variants={itemLeft}
              className="mt-6 max-w-xl text-base leading-relaxed text-muted sm:text-lg"
            >
              Prepare legally valid property documents accepted across GNIDA,
              Noida Authority &amp; YEIDA. No Broker. No Middleman. Physical
              Delivery. Lowest Price Guaranteed.
            </motion.p>

            <motion.div
              variants={itemLeft}
              className="mt-8 flex flex-col gap-4 sm:flex-row"
            >
              <button
                onClick={() => setActiveDoc('rent-agreement')}
                className="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-primary/25 transition-all duration-200 hover:bg-primary-dark hover:shadow-xl active:scale-95"
              >
                Draft Document
                <FileText className="h-5 w-5" />
              </button>
              <a
                href="#services"
                className="inline-flex items-center justify-center gap-2 rounded-full border-2 border-border bg-white px-8 py-3.5 text-base font-semibold text-dark transition-all duration-200 hover:border-primary/30 hover:bg-primary/5 active:scale-95"
              >
                View Pricing
                <IndianRupee className="h-5 w-5" />
              </a>
            </motion.div>

            <motion.div
              variants={itemLeft}
              className="mt-10 flex flex-wrap gap-x-6 gap-y-3"
            >
              {trusts.map((item) => (
                <span
                  key={item}
                  className="inline-flex items-center gap-2 text-sm font-medium text-muted"
                >
                  <span className="flex h-5 w-5 items-center justify-center rounded-full bg-success/10 text-success">
                    <Check className="h-3 w-3" strokeWidth={3} />
                  </span>
                  {item}
                </span>
              ))}
            </motion.div>
          </motion.div>

          <motion.div
            variants={itemRight}
            initial={false}
            animate="visible"
            className="relative lg:col-span-6"
          >
            <div className="relative mx-auto aspect-[4/3] w-full max-w-lg">
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-primary/5 via-primary/5 to-primary/10" />

              <svg
                viewBox="0 0 400 300"
                className="h-full w-full"
                fill="none"
              >
                <rect width="400" height="300" rx="24" className="fill-white/50" />

                {/* Skyline */}
                {[
                  { x: 40, w: 48, h: 100, color: "#E2E8F0" },
                  { x: 96, w: 36, h: 140, color: "#CBD5E1" },
                  { x: 140, w: 56, h: 80, color: "#E2E8F0" },
                  { x: 204, w: 40, h: 160, color: "#CBD5E1" },
                  { x: 252, w: 52, h: 110, color: "#E2E8F0" },
                  { x: 312, w: 44, h: 130, color: "#CBD5E1" },
                ].map((b, i) => (
                  <rect
                    key={i}
                    x={b.x}
                    y={300 - b.h - 40}
                    width={b.w}
                    height={b.h}
                    rx={4}
                    className="fill-current"
                    style={{ color: b.color }}
                  />
                ))}

                {/* Windows on buildings */}
                {[
                  { x: 48, y: 175, color: "#2563EB" },
                  { x: 64, y: 175, color: "#2563EB" },
                  { x: 48, y: 190, color: "#93C5FD" },
                  { x: 64, y: 190, color: "#2563EB" },
                  { x: 104, y: 135, color: "#93C5FD" },
                  { x: 116, y: 135, color: "#2563EB" },
                  { x: 104, y: 150, color: "#2563EB" },
                  { x: 116, y: 150, color: "#93C5FD" },
                  { x: 212, y: 115, color: "#2563EB" },
                  { x: 228, y: 115, color: "#93C5FD" },
                  { x: 212, y: 130, color: "#93C5FD" },
                  { x: 228, y: 130, color: "#2563EB" },
                  { x: 320, y: 145, color: "#2563EB" },
                  { x: 340, y: 145, color: "#93C5FD" },
                  { x: 320, y: 160, color: "#93C5FD" },
                  { x: 340, y: 160, color: "#2563EB" },
                ].map((w, i) => (
                  <rect
                    key={i}
                    x={w.x}
                    y={w.y}
                    width={6}
                    height={8}
                    rx={1}
                    className="fill-current"
                    style={{ color: w.color }}
                    opacity={0.8}
                  />
                ))}

                {/* Document icon */}
                <g transform="translate(160, 80)">
                  <rect x={0} y={0} width={80} height={100} rx={8} className="fill-white stroke-primary/30" strokeWidth={1.5} />
                  <line x1={16} y1={28} x2={64} y2={28} className="stroke-primary/40" strokeWidth={2} strokeLinecap="round" />
                  <line x1={16} y1={42} x2={52} y2={42} className="stroke-primary/30" strokeWidth={2} strokeLinecap="round" />
                  <line x1={16} y1={56} x2={58} y2={56} className="stroke-primary/30" strokeWidth={2} strokeLinecap="round" />
                  <line x1={16} y1={70} x2={44} y2={70} className="stroke-primary/30" strokeWidth={2} strokeLinecap="round" />
                  <rect x={26} y={78} width={28} height={14} rx={4} className="fill-primary/10 stroke-primary/40" strokeWidth={1} />
                  <text x={40} y={88} textAnchor="middle" className="fill-primary text-[8px] font-bold">₹150</text>
                </g>

                {/* Delivery truck */}
                <g transform="translate(280, 180)">
                  <rect x={0} y={12} width={60} height={28} rx={4} className="fill-primary/10 stroke-primary/30" strokeWidth={1.5} />
                  <rect x={20} y={0} width={40} height={20} rx={3} className="fill-primary/5 stroke-primary/20" strokeWidth={1} />
                  <circle cx={14} cy={44} r={10} className="fill-white stroke-primary/30" strokeWidth={1.5} />
                  <circle cx={48} cy={44} r={10} className="fill-white stroke-primary/30" strokeWidth={1.5} />
                  <text x={14} y={48} textAnchor="middle" className="fill-primary text-[10px]">⚡</text>
                </g>

                {/* Phone mockup */}
                <g transform="translate(60, 160)">
                  <rect x={0} y={0} width={36} height={60} rx={6} className="fill-dark stroke-dark/50" strokeWidth={1.5} />
                  <rect x={6} y={8} width={24} height={40} rx={2} className="fill-primary/5" />
                  <line x1={10} y1={14} x2={26} y2={14} className="stroke-primary/40" strokeWidth={1.5} strokeLinecap="round" />
                  <line x1={10} y1={22} x2={22} y2={22} className="stroke-primary/30" strokeWidth={1} strokeLinecap="round" />
                  <rect x={10} y={32} width={16} height={10} rx={3} className="fill-primary/10" />
                  <text x={18} y={39} textAnchor="middle" className="fill-primary text-[6px] font-bold">OK</text>
                  <circle cx={18} cy={56} r={2} className="fill-white" />
                </g>

                {/* Map pin */}
                <g transform="translate(320, 100)">
                  <MapPin className="h-8 w-8 text-primary/40" />
                </g>

                {/* Dotted connection lines */}
                <line x1={200} y1={180} x2={280} y2={200} stroke="#2563EB" strokeWidth={1} strokeDasharray="4 4" opacity={0.2} />
                <line x1={200} y1={180} x2={96} y2={200} stroke="#2563EB" strokeWidth={1} strokeDasharray="4 4" opacity={0.2} />
              </svg>

              {/* Floating cards */}
              <motion.div
                animate={floatAnimation}
                className="absolute -left-4 top-8 rounded-xl border border-border bg-white px-3.5 py-2.5 shadow-lg"
              >
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-primary" />
                  <span className="text-sm font-bold text-dark">20 Minutes</span>
                </div>
              </motion.div>

              <motion.div
                animate={{
                  y: [0, 8, 0],
                  transition: { duration: 3.5, repeat: Infinity, ease: "easeInOut" as const, delay: 0.5 },
                }}
                className="absolute -right-2 top-20 rounded-xl border border-border bg-white px-3.5 py-2.5 shadow-lg"
              >
                <div className="flex items-center gap-2">
                  <IndianRupee className="h-4 w-4 text-success" />
                  <span className="text-sm font-bold text-dark">₹150 Starting</span>
                </div>
              </motion.div>

              <motion.div
                animate={{
                  y: [0, -6, 0],
                  transition: { duration: 3, repeat: Infinity, ease: "easeInOut" as const, delay: 1 },
                }}
                className="absolute -left-6 bottom-16 rounded-xl border border-border bg-white px-3.5 py-2.5 shadow-lg"
              >
                <div className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-success" />
                  <span className="text-sm font-bold text-dark">Accepted</span>
                </div>
              </motion.div>

              <motion.div
                animate={{
                  y: [0, -12, 0],
                  transition: { duration: 4.5, repeat: Infinity, ease: "easeInOut" as const, delay: 0.8 },
                }}
                className="absolute -right-4 bottom-24 rounded-xl border border-border bg-white px-3.5 py-2.5 shadow-lg"
              >
                <div className="flex items-center gap-2">
                  <Truck className="h-4 w-4 text-primary" />
                  <span className="text-sm font-bold text-dark">Physical Delivery</span>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent pointer-events-none" />
    </section>
  );
}
