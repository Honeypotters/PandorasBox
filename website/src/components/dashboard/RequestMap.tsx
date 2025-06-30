// components/dashboard/RequestMap.tsx

import React from "react";
import dynamic from "next/dynamic";

// --- Type Definitions ---
interface Location {
  position: [number, number];
  name: string;
}

interface RequestMapProps {
  locations: Location[];
}

const LeafletMap = dynamic(() => import("./LeafletMap"), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full bg-gray-200 animate-pulse flex items-center justify-center">
      <p className="text-gray-500">Loading Map...</p>
    </div>
  ),
});

const RequestMap = ({ locations }: RequestMapProps) => {
  return (
    <div className="bg-white border border-black p-6 rounded-lg h-full flex flex-col">
      <h2 className="text-lg font-bold text-black mb-4">Request Origins</h2>
      <div className="flex-grow rounded-md overflow-hidden">
        <LeafletMap locations={locations} />
      </div>
    </div>
  );
};

export default RequestMap;
