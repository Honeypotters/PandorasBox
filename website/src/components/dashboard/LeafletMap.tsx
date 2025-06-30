// components/dashboard/LeafletMap.tsx
"use client";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";

import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import MarkerClusterGroup from "react-leaflet-markercluster";

const blackDotIcon = L.divIcon({
  className: "custom-dot-marker",
  iconSize: [12, 12],
});

const createClusterCustomIcon = function (cluster: L.MarkerCluster) {
  return L.divIcon({
    html: `<span>${cluster.getChildCount()}</span>`,
    className: "custom-cluster-icon",
    iconSize: L.point(40, 40, true),
  });
};

interface Location {
  position: [number, number];
  name: string;
}

interface LeafletMapProps {
  locations: Location[];
}

const DynamicMarkers = ({ locations }: LeafletMapProps) => {
  return (
    <MarkerClusterGroup
      iconCreateFunction={createClusterCustomIcon}
      polygonOptions={{
        fillColor: "#000000",
        color: "#000000",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.5,
      }}
    >
           {" "}
      {locations.map((location, index) => (
        <Marker
          key={`${location.name}-${location.position[0]}-${location.position[1]}-${index}`}
          position={location.position as L.LatLngExpression}
          icon={blackDotIcon}
        >
                   {" "}
          <Popup>
                        Request from <br /> {location.name}           {" "}
          </Popup>
                   {" "}
        </Marker>
      ))}
         {" "}
    </MarkerClusterGroup>
  );
};

const LeafletMap = ({ locations }: LeafletMapProps) => {
  return (
    <MapContainer
      center={[25, 0]}
      zoom={2}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%" }}
    >
           {" "}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
            <DynamicMarkers locations={locations} />   {" "}
    </MapContainer>
  );
};

export default LeafletMap;
