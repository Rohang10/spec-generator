import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from "@/context/ThemeContext";

export const metadata: Metadata = {
  title: "AI Spec Generator - Transform Requirements into Technical Specifications",
  description: "Automatically convert messy requirements into clear technical specifications. Generate modules, features, user stories, API endpoints, and database schemas with AI-powered analysis.",
  keywords: [
    "AI spec generator",
    "requirements analysis",
    "technical specifications",
    "API design",
    "database schema",
    "user stories",
    "software requirements",
    "specification automation",
    "LLM specification generator",
    "project documentation",
    "software architecture",
    "requirement engineering"
  ],
  authors: [{ name: "AI Spec Generator " }],
  
  // Open Graph
  openGraph: {
    type: "website",
    locale: "en_US",
    title: "AI Spec Generator - Convert Requirements to Technical Specs",
    description: "Transform messy requirements into clear modules, features, user stories, API endpoints, and database schemas automatically with AI",
    siteName: "AI Spec Generator",
  },
  
  // Twitter Card
  twitter: {
    card: "summary_large_image",
    title: "AI Spec Generator",
    description: "AI-powered tool to transform requirements into technical specifications, API designs, and database schemas",
  },
  
  // Robots
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  
  // Additional metadata
  category: "Technology",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta name="theme-color" content="#020617" />
        
        {/* Structured Data for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              "name": "AI Spec Generator",
              "applicationCategory": "DeveloperApplication",
              "description": "AI-powered specification generator that transforms requirements into technical specifications, user stories, API endpoints, and database schemas",
              "operatingSystem": "Web Browser",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              },
              "featureList": [
                "Requirements analysis",
                "Module and feature extraction",
                "User story generation",
                "API endpoint suggestions",
                "Database schema design",
                "Iterative refinement"
              ],
              "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "ratingCount": "150"
              }
            }),
          }}
        />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}