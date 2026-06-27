'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Phone, ArrowRight } from 'lucide-react'

const links = [
  { href: '#home', label: 'Home' },
  { href: '#services', label: 'Services' },
  { href: '#pricing', label: 'Pricing' },
  { href: '#how-it-works', label: 'How It Works' },
  { href: '#coverage', label: 'Coverage' },
  { href: '#about', label: 'About' },
  { href: '#contact', label: 'Contact' },
]

const menuVariants = {
  hidden: { x: '100%', opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { type: 'spring', damping: 28, stiffness: 300 },
  },
  exit: {
    x: '100%',
    opacity: 0,
    transition: { type: 'spring', damping: 28, stiffness: 300 },
  },
}

const linkItemVariants = {
  hidden: { opacity: 0, x: 20 },
  visible: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: { delay: 0.1 + i * 0.05, duration: 0.3 },
  }),
}

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    if (mobileOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [mobileOpen])

  const handleClose = () => setMobileOpen(false)

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#F8FAFC]/80 backdrop-blur-md shadow-[0_1px_3px_0_rgba(0,0,0,0.06)] border-b border-[#E5E7EB]'
          : 'bg-[#F8FAFC]/80 backdrop-blur-md'
      }`}
    >
      <div className="mx-auto max-w-7xl flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16 lg:h-20">
        {/* Logo */}
        <a href="#home" className="flex items-center gap-2 group">
          <span className="text-xl sm:text-2xl font-bold tracking-tight text-[#0F172A] transition-colors duration-200">
            INSTA<span className="text-[#2563EB]">DEED</span>
          </span>
        </a>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center gap-1">
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="relative px-3 py-2 text-sm font-medium text-slate-600 rounded-lg transition-colors duration-200 hover:text-[#2563EB] hover:bg-[#2563EB]/5"
            >
              {link.label}
            </a>
          ))}
        </nav>

        {/* Right side actions */}
        <div className="hidden lg:flex items-center gap-3">
          <a
            href="https://wa.me/1234567890"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-[#22C55E] rounded-full transition-all duration-200 hover:bg-[#16A34A] hover:shadow-lg hover:shadow-[#22C55E]/25 active:scale-95"
          >
            <Phone className="w-4 h-4" />
            WhatsApp
          </a>
          <a
            href="#draft-now"
            className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-[#2563EB] rounded-full transition-all duration-200 hover:bg-[#1D4ED8] hover:shadow-lg hover:shadow-[#2563EB]/25 active:scale-95"
          >
            Draft Now
            <ArrowRight className="w-4 h-4" />
          </a>
        </div>

        {/* Mobile hamburger */}
        <button
          onClick={() => setMobileOpen(true)}
          className="lg:hidden relative z-50 p-2 -mr-2 text-slate-700 rounded-lg transition-colors duration-200 hover:bg-slate-100"
          aria-label="Open menu"
        >
          <Menu className="w-6 h-6" />
        </button>
      </div>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
              onClick={handleClose}
              className="fixed inset-0 z-40 bg-[#0F172A]/40 backdrop-blur-sm"
            />

            {/* Drawer */}
            <motion.div
              variants={menuVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="fixed top-0 right-0 bottom-0 z-50 w-full max-w-sm bg-[#FFFFFF] shadow-2xl border-l border-[#E5E7EB] flex flex-col"
            >
              {/* Drawer header */}
              <div className="flex items-center justify-between px-5 h-16 border-b border-[#E5E7EB]">
                <span className="text-xl font-bold tracking-tight text-[#0F172A]">
                  INSTA<span className="text-[#2563EB]">DEED</span>
                </span>
                <button
                  onClick={handleClose}
                  className="p-2 -mr-2 text-slate-700 rounded-lg transition-colors duration-200 hover:bg-slate-100"
                  aria-label="Close menu"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Drawer links */}
              <nav className="flex-1 overflow-y-auto px-4 pt-4 pb-6 space-y-1">
                {links.map((link, i) => (
                  <motion.a
                    key={link.href}
                    href={link.href}
                    custom={i}
                    variants={linkItemVariants}
                    initial="hidden"
                    animate="visible"
                    onClick={handleClose}
                    className="block px-4 py-3 text-base font-medium text-slate-700 rounded-xl transition-colors duration-200 hover:text-[#2563EB] hover:bg-[#2563EB]/5"
                  >
                    {link.label}
                  </motion.a>
                ))}
              </nav>

              {/* Drawer CTA buttons */}
              <div className="border-t border-[#E5E7EB] px-5 py-5 space-y-3">
                <a
                  href="https://wa.me/1234567890"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 w-full px-4 py-3 text-sm font-semibold text-white bg-[#22C55E] rounded-full transition-all duration-200 hover:bg-[#16A34A] active:scale-[0.97]"
                >
                  <Phone className="w-4 h-4" />
                  WhatsApp
                </a>
                <a
                  href="#draft-now"
                  onClick={handleClose}
                  className="flex items-center justify-center gap-2 w-full px-4 py-3 text-sm font-semibold text-white bg-[#2563EB] rounded-full transition-all duration-200 hover:bg-[#1D4ED8] active:scale-[0.97]"
                >
                  Draft Now
                  <ArrowRight className="w-4 h-4" />
                </a>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </header>
  )
}
