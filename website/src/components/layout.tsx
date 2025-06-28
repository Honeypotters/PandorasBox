// src/app/layout.tsx
import Sidebar from './Sidebar';
import Head from 'next/head';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: LayoutProps) {
  return (
    <div className="flex h-screen">
      <Head>
        <meta httpEquiv="content-language" content="en-us"></meta>
        <meta name="author" content="Samuel Paynter "></meta>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/png" href="/favicon/favicon-96x96.png" sizes="96x96" />
        <link rel="icon" type="image/svg+xml" href="/favicon/favicon.svg" />
        <link rel="shortcut icon" href="/favicon/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png" />
        <meta name="apple-mobile-web-app-title" content="Pandora's Box" />
        <link rel="manifest" href="/favicon/site.webmanifest" />
      </Head>

      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
