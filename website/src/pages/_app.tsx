import type { AppProps } from "next/app"; // Import AppProps type
import Layout from "../components/layout";
import Script from "next/script";
import "tailwindcss/tailwind.css";
import "../prism-theme.css";
import "../../globals.css";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}
