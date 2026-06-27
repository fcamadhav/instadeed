import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-plus-jakarta",
});

export const metadata: Metadata = {
  title: "INSTADEED — One Platform. All Property Documents. Delivered Within 20 Minutes.",
  description:
    "Prepare legally valid property documents accepted across GNIDA, Noida Authority & YEIDA. No Broker. No Middleman. Physical Delivery. Lowest Price Guaranteed.",
  keywords: [
    "property documents",
    "rent agreement",
    "registry",
    "mutation",
    "GNIDA",
    "Noida Authority",
    "YEIDA",
    "transfer memorandum",
    "legal documents",
    "Gautam Buddha Nagar",
  ],
  openGraph: {
    title: "INSTADEED — Property Documents in 20 Minutes",
    description:
      "Legally valid property documents accepted across GNIDA, Noida Authority & YEIDA.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={plusJakartaSans.variable}>
      <body>{children}</body>
    </html>
  );
}
