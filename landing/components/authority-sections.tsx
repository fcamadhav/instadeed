"use client";

import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2, FileText, Home, MapPin } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const authorities = [
  {
    id: "gnida",
    name: "GNIDA",
    fullName: "Greater Noida Industrial Development Authority",
    description:
      "Comprehensive legal drafting and documentation services for properties and plots located in Greater Noida.",
    color: "emerald",
    bgColor: "bg-emerald-50",
    textColor: "text-emerald-700",
    buttonColor: "bg-emerald-600 hover:bg-emerald-700",
    services: ["Property Registry", "Transfer Memorandum (TM)", "Property Mutation", "Rent Agreements", "Lease Deeds"],
    icon: MapPin,
    logoUrl: "/logos/gnida.png", // Add your GNIDA logo to public/logos/gnida.png
  },
  {
    id: "noida",
    name: "Noida Authority",
    fullName: "New Okhla Industrial Development Authority",
    description:
      "Expert documentation services for residential, commercial, and industrial properties under Noida Authority.",
    color: "blue",
    bgColor: "bg-blue-50",
    textColor: "text-blue-700",
    buttonColor: "bg-blue-600 hover:bg-blue-700",
    services: ["Sale Deeds", "Transfer of Property", "Mutation Services", "Rent & Lease Agreements", "Mortgage Deeds"],
    icon: Home,
    logoUrl: "/logos/noida.png", // Add your Noida Authority logo to public/logos/noida.png
  },
  {
    id: "yeida",
    name: "YEIDA",
    fullName: "Yamuna Expressway Industrial Development Authority",
    description:
      "Streamlined legal drafting for plots, flats, and land parcels situated along the Yamuna Expressway.",
    color: "purple",
    bgColor: "bg-purple-50",
    textColor: "text-purple-700",
    buttonColor: "bg-purple-600 hover:bg-purple-700",
    services: ["Plot Registry", "TM Processing", "Mutation Updates", "Builder Buyer Agreements", "Sub-Lease Deeds"],
    icon: FileText,
    logoUrl: "/logos/yeida.png", // Add your YEIDA logo to public/logos/yeida.png
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15 },
  },
};

const sectionVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const },
  },
};

export default function AuthoritySections() {
  return (
    <section id="authorities" className="w-full bg-slate-50 py-20 lg:py-28">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-16 text-center"
        >
          <h2 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl md:text-5xl mb-4">
            Specialized Authority Services
          </h2>
          <p className="mx-auto max-w-2xl text-base font-medium text-slate-500 sm:text-lg">
            We provide dedicated legal drafting and documentation services tailored specifically for the major authorities in the NCR region.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="space-y-12 lg:space-y-16"
        >
          {authorities.map((auth, index) => (
            <motion.div
              key={auth.id}
              variants={sectionVariants}
              className={`flex flex-col lg:flex-row overflow-hidden rounded-3xl border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 bg-white ${
                index % 2 === 1 ? "lg:flex-row-reverse" : ""
              }`}
            >
              {/* Left/Right Banner Area */}
              <div
                className={`w-full lg:w-2/5 p-8 lg:p-12 flex flex-col items-center justify-center text-center ${auth.bgColor} relative overflow-hidden`}
              >
                {/* Logo Area */}
                <div className="relative z-10 w-32 h-32 md:w-40 md:h-40 mb-6 bg-white rounded-full shadow-md flex items-center justify-center p-4 border-4 border-white">
                  <div className="w-full h-full relative flex items-center justify-center">
                    {/* Fallback Icon if logo fails, otherwise Logo text */}
                    <auth.icon className={`w-16 h-16 ${auth.textColor} opacity-20 absolute`} />
                    <div className="w-full h-full relative z-10 flex items-center justify-center">
                       <span className={`text-2xl font-black tracking-tight ${auth.textColor}`}>{auth.name}</span>
                    </div>
                  </div>
                </div>

                <h3 className={`text-3xl font-black tracking-tight ${auth.textColor} relative z-10`}>
                  {auth.name}
                </h3>
                <p className={`mt-3 text-sm font-bold uppercase tracking-widest ${auth.textColor} opacity-80 relative z-10`}>
                  {auth.fullName}
                </p>
              </div>

              {/* Content Area */}
              <div className="w-full lg:w-3/5 p-8 lg:p-12 flex flex-col justify-center bg-white relative z-10">
                <p className="text-lg text-slate-600 mb-8 leading-relaxed">
                  {auth.description}
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-4 gap-x-6 mb-10">
                  {auth.services.map((service, idx) => (
                    <div key={idx} className="flex items-center gap-3">
                      <CheckCircle2 className={`w-5 h-5 ${auth.textColor} shrink-0`} />
                      <span className="font-semibold text-slate-700">{service}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                  <p className="text-sm text-slate-500 font-medium">Select to begin drafting process</p>
                  <Link
                    href={`/draft?type=rent`}
                    className={`inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-white font-bold shadow-sm transition-all ${auth.buttonColor}`}
                  >
                    Start {auth.name} Draft
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
