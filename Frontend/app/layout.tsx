import React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "../src/styles/globals.css";


const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Document Intelligence Assistant",
  description: "Upload documents and ask intelligent questions about their content",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
