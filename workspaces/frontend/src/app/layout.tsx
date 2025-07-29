import type { Metadata } from "next";
import "./globals.css";
import { MSALWrapper } from '@/components/MSALWrapper';

export const metadata: Metadata = {
  title: "Noumena",
  description: "AI Characters Living in a Narrative World",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <MSALWrapper>
          {children}
        </MSALWrapper>
      </body>
    </html>
  );
}
