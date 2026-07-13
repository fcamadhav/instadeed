import { Facebook, Twitter, Instagram, Linkedin, Mail, Phone, MapPin } from 'lucide-react'

const footerLinks = {
  quick: [
    { label: 'Home', href: '/#home' },
    { label: 'Services', href: '/#services' },
    { label: 'Pricing', href: '/#pricing' },
    { label: 'How It Works', href: '/#how-it-works' },
    { label: 'Coverage', href: '/#coverage' },
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
  ],
  services: [
    { label: 'Rent Agreement', href: '/services/rent-agreement' },
    { label: 'Registry', href: '/services/registry' },
    { label: 'Mutation', href: '/services/mutation' },
    { label: 'Transfer Memorandum (TM)', href: '/services/tm' },
    { label: 'Permission to Mortgage (PTM)', href: '/services/ptm' },
    { label: 'GNIDA 5-in-1 Package', href: '/services/gnida' },
  ],
  legal: [
    { label: 'Privacy Policy', href: '/privacy' },
    { label: 'Terms of Service', href: '/terms' },
    { label: 'Refund & Cancellation', href: '/refund' },
  ],
}

export default function Footer() {
  return (
    <footer className="w-full bg-white border-t border-border/50">
      <div className="mx-auto max-w-7xl px-4 pb-8 pt-16 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          {/* Brand */}
          <div className="flex flex-col">
            <a href="/" className="flex items-center gap-2 mb-6">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-white"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              </div>
              <span className="text-xl font-bold tracking-tight text-dark">
                INSTADEED
              </span>
            </a>
            <p className="mb-8 max-w-xs text-sm leading-relaxed text-muted font-medium">
              One platform for all your property document needs. Fast, legal, and
              accepted by all major authorities in Gautam Buddha Nagar.
            </p>
            {/* <div className="flex gap-4">
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-50 text-muted transition-colors hover:bg-primary hover:text-white border border-border">
                <Facebook className="h-4 w-4" />
              </a>
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-50 text-muted transition-colors hover:bg-primary hover:text-white border border-border">
                <Twitter className="h-4 w-4" />
              </a>
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-50 text-muted transition-colors hover:bg-primary hover:text-white border border-border">
                <Instagram className="h-4 w-4" />
              </a>
              <a href="#" className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-50 text-muted transition-colors hover:bg-primary hover:text-white border border-border">
                <Linkedin className="h-4 w-4" />
              </a>
            </div> */}
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="mb-6 text-sm font-bold text-dark">Quick Links</h3>
            <ul className="flex flex-col gap-3">
              {footerLinks.quick.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="text-sm font-medium text-muted transition-colors hover:text-primary"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Popular Services */}
          <div>
            <h3 className="mb-6 text-sm font-bold text-dark">Popular Services</h3>
            <ul className="flex flex-col gap-3">
              {footerLinks.services.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="text-sm font-medium text-muted transition-colors hover:text-primary"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="mb-6 text-sm font-bold text-dark">Contact Us</h3>
            <ul className="flex flex-col gap-4">
              <li className="flex items-start gap-3">
                <Mail className="mt-0.5 h-4 w-4 shrink-0 text-muted" />
                <span className="text-sm font-medium text-muted">info@instadeed.in</span>
              </li>
              <li className="flex items-start gap-3">
                <Phone className="mt-0.5 h-4 w-4 shrink-0 text-muted" />
                <span className="text-sm font-medium text-muted">+91 88999 99321</span>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-muted" />
                <span className="text-sm font-medium leading-relaxed text-muted max-w-[200px]">
                  Sector 62, Noida,<br />Gautam Buddha Nagar,<br />Uttar Pradesh 201309
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-16 flex flex-col items-center justify-between gap-4 border-t border-border pt-8 sm:flex-row">
          <p className="text-xs font-medium text-muted text-center sm:text-left">
            © 2026 INSTADEED. All rights reserved.
          </p>
          <ul className="flex flex-wrap items-center justify-center gap-6 sm:justify-end">
            {footerLinks.legal.map((link) => (
              <li key={link.label}>
                <a
                  href={link.href}
                  className="text-xs font-medium text-muted transition-colors hover:text-primary"
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  )
}
