"use client"

import { motion } from "framer-motion"
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
} from "lucide-react"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0.1, 0.25, 1] } },
}

const leftVariants = {
  hidden: { opacity: 0, x: -40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.7, ease: [0.25, 0.1, 0.25, 1] } },
}

const rightVariants = {
  hidden: { opacity: 0, x: 40 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.7, ease: [0.25, 0.1, 0.25, 1] } },
}

const floatAnimation = {
  y: [0, -8, 0],
  transition: { duration: 3, repeat: Infinity, ease: "easeInOut" },
}

const floatAnimation2 = {
  y: [0, -6, 0],
  transition: { duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 0.5 },
}

const floatAnimation3 = {
  y: [0, -10, 0],
  transition: { duration: 4, repeat: Infinity, ease: "easeInOut", delay: 1 },
}

const trustItems = [
  { label: "Physical Delivery", icon: Truck },
  { label: "Lowest Price", icon: IndianRupee },
  { label: "Renewal Reminder", icon: Clock },
  { label: "Accepted Documents", icon: Shield },
  { label: "Error Free", icon: Check },
]

const floatingCards = [
  {
    label: "20 Minutes",
    sublabel: "Delivery",
    icon: Clock,
    color: "text-blue-600",
    bg: "bg-blue-50",
    className: "top-[8%] -right-[2%]",
    anim: floatAnimation,
  },
  {
    label: "₹150",
    sublabel: "Starting",
    icon: IndianRupee,
    color: "text-green-600",
    bg: "bg-green-50",
    className: "top-[38%] -left-[4%]",
    anim: floatAnimation2,
  },
  {
    label: "Accepted",
    sublabel: "GNIDA & YEIDA",
    icon: Shield,
    color: "text-primary",
    bg: "bg-primary/10",
    className: "bottom-[22%] -right-[4%]",
    anim: floatAnimation3,
  },
  {
    label: "Physical",
    sublabel: "Delivery",
    icon: Truck,
    color: "text-amber-600",
    bg: "bg-amber-50",
    className: "bottom-[6%] left-[8%]",
    anim: floatAnimation2,
  },
]

const floatingCardVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: (i: number) => ({
    opacity: 1,
    scale: 1,
    transition: { delay: 0.6 + i * 0.15, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] },
  }),
}

export default function Hero() {
  return (
    <section className="relative min-h-[90vh] overflow-hidden bg-background">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
        <motion.div
          className="flex flex-col lg:flex-row items-center gap-12 lg:gap-16"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* LEFT COLUMN - 55% */}
          <motion.div className="w-full lg:w-[55%]" variants={leftVariants}>
            {/* Badge */}
            <motion.div variants={itemVariants} className="mb-6">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.12em] text-primary">
                <MapPin className="h-3.5 w-3.5" />
                Gautam Buddha Nagar&apos;s Most Trusted Document Platform
              </span>
            </motion.div>

            {/* Headline */}
            <motion.h1
              variants={itemVariants}
              className="text-5xl sm:text-6xl lg:text-7xl font-bold leading-[1.08] tracking-tight text-dark"
            >
              One Platform.
              <br />
              <span className="text-primary">All Property Documents.</span>
              <br />
              Delivered Within{" "}
              <span className="relative whitespace-nowrap">
                <span className="relative z-10">20 Minutes</span>
                <span className="absolute bottom-1 left-0 -z-0 h-3 w-full rounded-full bg-primary/15" />
              </span>
              .
            </motion.h1>

            {/* Subheading */}
            <motion.p
              variants={itemVariants}
              className="mt-6 max-w-xl text-lg leading-relaxed text-muted sm:text-xl"
            >
              Prepare legally valid property documents accepted across GNIDA, Noida Authority &amp;
              YEIDA. No Broker. No Middleman. Physical Delivery. Lowest Price Guaranteed.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div variants={itemVariants} className="mt-8 flex flex-wrap gap-4">
              <motion.a
                href="#"
                className="inline-flex items-center gap-2 rounded-xl bg-primary px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-primary/25 transition-shadow hover:shadow-xl hover:shadow-primary/30"
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
              >
                <FileText className="h-4 w-4" />
                Draft Document
              </motion.a>
              <motion.a
                href="#"
                className="inline-flex items-center gap-2 rounded-xl border-2 border-border bg-card px-7 py-3.5 text-sm font-semibold text-dark transition-colors hover:border-primary/30 hover:bg-primary/5"
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
              >
                <IndianRupee className="h-4 w-4" />
                View Pricing
              </motion.a>
            </motion.div>

            {/* Trust Icons Row */}
            <motion.div variants={itemVariants} className="mt-10">
              <p className="mb-4 text-xs font-medium uppercase tracking-[0.08em] text-muted-light">
                Why customers trust us
              </p>
              <div className="flex flex-wrap gap-x-6 gap-y-3">
                {trustItems.map((item) => (
                  <div key={item.label} className="flex items-center gap-1.5 text-sm text-dark">
                    <span className="flex h-5 w-5 items-center justify-center rounded-full bg-success/10">
                      <item.icon className="h-3 w-3 text-success" />
                    </span>
                    <span className="font-medium">{item.label}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          </motion.div>

          {/* RIGHT COLUMN - 45% */}
          <motion.div
            className="relative w-full lg:w-[45%]"
            variants={rightVariants}
          >
            <div className="relative mx-auto aspect-[4/3] w-full max-w-lg">
              {/* Gradient background */}
              <div className="absolute inset-0 rounded-[2rem] bg-gradient-to-br from-primary/5 via-primary/5 to-primary/[0.02]" />
              <div className="absolute inset-4 rounded-[1.5rem] border border-primary/10 bg-card/50 backdrop-blur-sm" />

              {/* City Skyline Silhouette */}
              <svg
                className="absolute bottom-[18%] left-0 w-full"
                viewBox="0 0 400 120"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <motion.path
                  d="M0 120V90L20 85V75L35 70V55L50 50V65L70 60V75L90 70V55L105 50V65L120 60V80L140 75V90L160 85V70L175 65V80L195 75V60L210 55V70L225 65V80L245 75V90L260 85V100L280 95V110L300 105V90L315 85V100L330 95V110L350 105V90L370 85V100L390 95V110L400 105V120H0Z"
                  fill="url(#skylineGrad)"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.35 }}
                  transition={{ duration: 1.5, delay: 0.8, ease: "easeInOut" }}
                />
                {/* Windows */}
                {[
                  { x: 28, w: 4 },
                  { x: 92, w: 6 },
                  { x: 128, w: 4 },
                  { x: 168, w: 4 },
                  { x: 210, w: 4 },
                  { x: 268, w: 6 },
                  { x: 340, w: 4 },
                ].map((win, i) => (
                  <motion.rect
                    key={i}
                    x={win.x}
                    y={62 + (i % 3) * 8}
                    width={win.w}
                    height={5}
                    rx={1}
                    fill="#2563EB"
                    opacity={0.5}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.5 }}
                    transition={{ delay: 1.5 + i * 0.1, duration: 0.3 }}
                  />
                ))}
                <defs>
                  <linearGradient id="skylineGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#2563EB" stopOpacity="0.5" />
                    <stop offset="100%" stopColor="#2563EB" stopOpacity="0.15" />
                  </linearGradient>
                </defs>
              </svg>

              {/* Document Icon */}
              <motion.div
                className="absolute left-1/2 top-[22%] -translate-x-1/2"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9, duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <div className="flex h-20 w-16 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-dark shadow-lg shadow-primary/20">
                  <FileText className="h-8 w-8 text-white" />
                </div>
              </motion.div>

              {/* Delivery Icon */}
              <motion.div
                className="absolute bottom-[30%] left-[30%]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.1, duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-green-500 to-green-600 shadow-lg shadow-green-500/20">
                  <Truck className="h-7 w-7 text-white" />
                </div>
              </motion.div>

              {/* Phone Mockup */}
              <motion.div
                className="absolute bottom-[32%] right-[28%]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.3, duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-500 to-amber-600 shadow-lg shadow-amber-500/20">
                  <Smartphone className="h-6 w-6 text-white" />
                </div>
              </motion.div>

              {/* Building Icon */}
              <motion.div
                className="absolute bottom-[28%] left-[8%]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.5, duration: 0.6, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-slate-600 to-slate-700 shadow-lg">
                  <Building className="h-5 w-5 text-white" />
                </div>
              </motion.div>

              {/* Dotted connection lines */}
              <svg
                className="absolute inset-0 h-full w-full"
                viewBox="0 0 500 400"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <motion.path
                  d="M250 88L180 180"
                  stroke="#2563EB"
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  strokeLinecap="round"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.25 }}
                  transition={{ delay: 1.8, duration: 0.8, ease: "easeInOut" }}
                />
                <motion.path
                  d="M250 88L340 175"
                  stroke="#2563EB"
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  strokeLinecap="round"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.25 }}
                  transition={{ delay: 2, duration: 0.8, ease: "easeInOut" }}
                />
                <motion.path
                  d="M180 180L340 175"
                  stroke="#2563EB"
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  strokeLinecap="round"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.15 }}
                  transition={{ delay: 2.2, duration: 0.8, ease: "easeInOut" }}
                />
              </svg>

              {/* Floating Cards */}
              {floatingCards.map((card, i) => (
                <motion.div
                  key={card.label}
                  className={`absolute ${card.className}`}
                  custom={i}
                  variants={floatingCardVariants}
                  initial="hidden"
                  animate="visible"
                >
                  <motion.div
                    className="flex items-center gap-2.5 rounded-xl border border-border/60 bg-card px-3.5 py-2.5 shadow-xl shadow-black/[0.03] backdrop-blur-sm"
                    animate={card.anim}
                    whileHover={{
                      scale: 1.05,
                      boxShadow: "0 20px 40px rgba(0,0,0,0.08)",
                      transition: { duration: 0.2 },
                    }}
                  >
                    <span
                      className={`flex h-9 w-9 items-center justify-center rounded-lg ${card.bg}`}
                    >
                      <card.icon className={`h-4.5 w-4.5 ${card.color}`} />
                    </span>
                    <div>
                      <p className="text-sm font-bold leading-tight text-dark">{card.label}</p>
                      <p className="text-[11px] font-medium leading-tight text-muted-light">
                        {card.sublabel}
                      </p>
                    </div>
                  </motion.div>
                </motion.div>
              ))}

              {/* Bottom decorative glow */}
              <div className="absolute -bottom-8 left-1/2 h-32 w-3/4 -translate-x-1/2 rounded-full bg-primary/10 blur-[60px]" />
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Subtle gradient overlay at bottom */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent pointer-events-none" />
    </section>
  )
}
