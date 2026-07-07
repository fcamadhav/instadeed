import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import ClientLayout from "@/components/ClientLayout";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "INSTADEED — One Platform. All Property Documents. Delivered in 20 Minutes.",
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
    <html lang="en" className={inter.variable}>
      <body className="bg-white min-h-screen relative font-sans">
        <div className="fixed inset-0 -z-50 h-full w-full bg-white opacity-25" style={{ backgroundImage: 'radial-gradient(#2563EB 1px, transparent 1px)', backgroundSize: '24px 24px' }}></div>
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}
