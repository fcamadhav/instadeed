'use client'

import Navbar from "@/components/navbar";
import Hero from "@/components/hero";
import TrustStrip from "@/components/trust-strip";
import Authorities from "@/components/authorities";
import Services from "@/components/services";
import WhyChooseUs from "@/components/why-choose-us";
import BrokerComparison from "@/components/broker-comparison";
import HowItWorks from "@/components/how-it-works";
import Reviews from "@/components/reviews";
import Faq from "@/components/faq";
import FinalCta from "@/components/final-cta";
import Footer from "@/components/footer";

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <TrustStrip />
      <Authorities />
      <Services />
      <WhyChooseUs />
      <BrokerComparison />
      <HowItWorks />
      <Reviews />
      <Faq />
      <FinalCta />
      <Footer />
    </main>
  );
}
