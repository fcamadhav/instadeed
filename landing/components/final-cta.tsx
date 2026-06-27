import { ArrowRight } from 'lucide-react'

export default function FinalCta() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary to-primary-dark py-20 sm:py-28">
      {/* Decorative circles */}
      <div className="pointer-events-none absolute -left-32 -top-32 h-72 w-72 rounded-full border border-white/10" />
      <div className="pointer-events-none absolute -bottom-40 -right-40 h-96 w-96 rounded-full border border-white/10" />
      <div className="pointer-events-none absolute left-1/3 top-1/4 h-4 w-4 rounded-full bg-white/20" />
      <div className="pointer-events-none absolute right-1/4 top-1/3 h-6 w-6 rounded-full bg-white/10" />
      <div className="pointer-events-none absolute bottom-1/4 left-1/4 h-3 w-3 rounded-full bg-white/15" />

      {/* Dot pattern */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            'radial-gradient(circle, white 1px, transparent 1px)',
          backgroundSize: '24px 24px',
        }}
      />

      <div className="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-white/10 bg-white/[0.03] px-6 py-16 text-center backdrop-blur-sm sm:px-12 sm:py-20">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-5xl">
            Ready to Draft Your Documents?
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-blue-100 sm:text-lg">
            Get your legally valid property documents delivered within 20 minutes.
            No broker, no middleman.
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <a
              href="#draft-now"
              className="inline-flex items-center gap-2 rounded-full bg-white px-8 py-3.5 text-base font-semibold text-primary shadow-lg transition-all duration-200 hover:bg-blue-50 hover:shadow-xl active:scale-95"
            >
              Start Now
              <ArrowRight className="h-5 w-5" />
            </a>
            <a
              href="#how-it-works"
              className="inline-flex items-center gap-2 rounded-full border border-white/30 px-8 py-3.5 text-base font-semibold text-white transition-all duration-200 hover:bg-white/10 active:scale-95"
            >
              See How It Works
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
