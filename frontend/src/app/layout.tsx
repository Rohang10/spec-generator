import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from "@/context/ThemeContext";

export const metadata: Metadata = {
  title: "AI Spec Generator - Transform Requirements into Technical Specifications",
  description:
    "Automatically convert messy requirements into clear technical specifications.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className="dark"              // 🔥 FORCE DARK AT SSR LEVEL
      suppressHydrationWarning
    >
      <head>
        <meta name="color-scheme" content="dark light" />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
