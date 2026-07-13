"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";

const reviews = [
  {
    name: "Ravi Sharma",
    location: "Noida",
    initials: "RS",
    color: "#2563EB",
    rating: 5,
    text: "Got my rent agreement in 15 minutes flat. No broker, no hassle. The document was accepted by the society without any issues. Highly recommended!",
  },
  {
    name: "Priya Verma",
    location: "Greater Noida",
    initials: "PV",
    color: "#16A34A",
    rating: 5,
    text: "I was sceptical at first but the team delivered exactly what they promised. Sale deed was ready in 20 minutes and delivered to my home the next day.",
  },
  {
    name: "Amit Gupta",
    location: "Ghaziabad",
    initials: "AG",
    color: "#8B5CF6",
    rating: 5,
    text: "Best part is no middlemen. I saved ₹3000 compared to what a broker quoted. The draft was perfect and the registrar accepted it without any changes.",
  },
  {
    name: "Sunita Yadav",
    location: "Delhi",
    initials: "SY",
    color: "#F59E0B",
    rating: 4,
    text: "Really smooth experience. The renewal reminder is a lifesaver — I would have completely forgotten about my expiring rental agreement. Thank you!",
  },
  {
    name: "Vikram Singh",
    location: "Noida",
    initials: "VS",
    color: "#EC4899",
    rating: 5,
    text: "Three minutes to fill the form, five minutes for draft review, and the deed was ready. Unbelievable speed. This is the future of legal documentation.",
  },
  {
    name: "Neha Kapoor",
    location: "Ghaziabad",
    initials: "NK",
    color: "#14B8A6",
    rating: 5,
    text: "Affordable, professional, and incredibly fast. The WhatsApp support answered all my queries instantly. Will definitely use again for my renewal.",
  },
];

function Stars({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <Star
          key={i}
          className={`h-4 w-4 ${
            i < count
              ? "fill-amber-400 text-amber-400"
              : "text-border"
          }`}
          strokeWidth={1.5}
        />
      ))}
    </div>
  );
}

const cardVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring" as const, damping: 22, stiffness: 280 },
  },
};

export default function Reviews() {
  return null;
}
