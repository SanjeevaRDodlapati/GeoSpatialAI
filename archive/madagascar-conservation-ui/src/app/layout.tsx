import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Madagascar Conservation AI | Protecting Biodiversity with Technology",
  description: "Advanced AI-powered conservation platform for protecting Madagascar's unique ecosystems and endemic species through real-time monitoring, predictive analytics, and stakeholder decision support.",
  keywords: "Madagascar, conservation, biodiversity, AI, machine learning, species protection, environmental monitoring",
  authors: [{ name: "Madagascar Conservation Team" }],
  openGraph: {
    title: "Madagascar Conservation AI",
    description: "Protecting Madagascar's biodiversity with advanced AI technology",
    type: "website",
    locale: "en_US",
  },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.variable} font-sans antialiased`}>
        <div id="root" className="min-h-screen bg-gradient-to-br from-[#FFF3E0] via-white to-[#E8F5E8]">
          {children}
        </div>
      </body>
    </html>
  );
}
