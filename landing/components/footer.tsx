import { Mail, Phone, MapPin } from 'lucide-react'

const quickLinks = [
  { href: '#home', label: 'Home' },
  { href: '#services', label: 'Services' },
  { href: '#pricing', label: 'Pricing' },
  { href: '#how-it-works', label: 'How It Works' },
  { href: '#coverage', label: 'Coverage' },
]

const services = [
  { href: '#services', label: 'Rent Agreement' },
  { href: '#services', label: 'Registry' },
  { href: '#services', label: 'Mutation' },
  { href: '#services', label: 'Transfer Memorandum (TM)' },
  { href: '#services', label: 'Partial TM (PTM)' },
]

export default function Footer() {
  return (
    <footer className="bg-dark">
      <div className="mx-auto max-w-7xl px-4 pb-8 pt-16 sm:px-6 lg:px-8">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          {/* Column 1: Brand */}
          <div>
            <span className="text-xl font-bold tracking-tight text-white">
              INSTA<span className="text-primary-light">DEED</span>
            </span>
            <p className="mt-4 text-sm leading-relaxed text-muted-light">
              One platform for all your property document needs. Fast, legal, and
              accepted by all major authorities in Gautam Buddha Nagar.
            </p>
            <div className="mt-6 flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-xs text-muted-light transition-colors duration-200 hover:border-primary/40 hover:text-primary-light">
                FB
              </span>
              <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-xs text-muted-light transition-colors duration-200 hover:border-primary/40 hover:text-primary-light">
                X
              </span>
              <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-xs text-muted-light transition-colors duration-200 hover:border-primary/40 hover:text-primary-light">
                IG
              </span>
              <span className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-xs text-muted-light transition-colors duration-200 hover:border-primary/40 hover:text-primary-light">
                LI
              </span>
            </div>
          </div>

          {/* Column 2: Quick Links */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              Quick Links
            </h3>
            <ul className="mt-5 space-y-3">
              {quickLinks.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="text-sm text-muted-light transition-colors duration-200 hover:text-white"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Services */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              Services
            </h3>
            <ul className="mt-5 space-y-3">
              {services.map((service) => (
                <li key={service.label}>
                  <a
                    href={service.href}
                    className="text-sm text-muted-light transition-colors duration-200 hover:text-white"
                  >
                    {service.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 4: Contact */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
              Contact
            </h3>
            <ul className="mt-5 space-y-4">
              <li>
                <a
                  href="mailto:info@instadeed.io"
                  className="flex items-center gap-3 text-sm text-muted-light transition-colors duration-200 hover:text-white"
                >
                  <Mail className="h-4 w-4 shrink-0 text-primary-light" />
                  info@instadeed.io
                </a>
              </li>
              <li>
                <span className="flex items-center gap-3 text-sm text-muted-light">
                  <Phone className="h-4 w-4 shrink-0 text-primary-light" />
                  +91 98765 43210
                </span>
              </li>
              <li>
                <span className="flex items-start gap-3 text-sm text-muted-light">
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-primary-light" />
                  <span>
                    Sector 62, Noida,
                    <br />
                    Gautam Buddha Nagar,
                    <br />
                    Uttar Pradesh 201309
                  </span>
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-14 border-t border-white/10 pt-8 text-center">
          <p className="text-sm text-muted-light">
            &copy; 2026 INSTADEED. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
