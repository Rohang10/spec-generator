import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from "@/context/ThemeContext";

export const metadata: Metadata = {
  title:
    "AI Spec Generator - Transform Requirements into Technical Specifications",
  description:
    "Automatically convert messy requirements into clear technical specifications. Generate modules, features, user stories, API endpoints, and database schemas with AI-powered analysis.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="color-scheme" content="dark light" />

        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function () {
              try {
              const stored = localStorage.getItem("theme");
              const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

              const theme = stored || (prefersDark ? "dark" : "dark"); // FORCE DARK DEFAULT

              document.documentElement.classList.remove("light", "dark");
              document.documentElement.classList.add(theme);
              } catch (e) {
                document.documentElement.classList.add("dark");
            }
            })();
          `,
          }}
        />
      </head>

      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
