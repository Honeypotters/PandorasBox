import type { AppProps } from "next/app"; // Import AppProps type
import Layout from "../components/layout";
import "tailwindcss/tailwind.css";
import "../../globals.css";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}
