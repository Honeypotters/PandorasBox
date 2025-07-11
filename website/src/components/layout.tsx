// src/app/layout.tsx
import Head from "next/head";
import { ReactNode } from "react";

import Header from "./Header";

interface LayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: LayoutProps) {
  return (
    <div className="flex flex-col h-screen w-full">
      <Head>
        <meta httpEquiv="content-language" content="en-us"></meta>
        <meta name="author" content="The Honeypotters"></meta>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link
          rel="icon"
          type="image/png"
          href="/favicon/favicon-96x96.png"
          sizes="96x96"
        />
        <link rel="icon" type="image/svg+xml" href="/favicon/favicon.svg" />
        <link rel="shortcut icon" href="/favicon/favicon.ico" />
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/favicon/apple-touch-icon.png"
        />
        <meta name="apple-mobile-web-app-title" content="Pandora's Box" />
        <link rel="manifest" href="/favicon/site.webmanifest" />
      </Head>
      <Header />

      <div className="flex flex-grow overflow-y-hidden">
        <main className="w-full pt-16 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
