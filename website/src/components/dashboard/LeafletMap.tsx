// components/dashboard/LeafletMap.tsx
"use client";

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

const locations = [
  { position: [51.505, -0.09], name: "London, UK" },
  { position: [48.8566, 2.3522], name: "Paris, France" },
  { position: [52.52, 13.405], name: "Berlin, Germany" },
  { position: [41.9028, 12.4964], name: "Rome, Italy" },
  { position: [40.7128, -74.006], name: "New York, USA" },
  { position: [34.0522, -118.2437], name: "Los Angeles, USA" },
  { position: [41.8781, -87.6298], name: "Chicago, USA" },
  { position: [35.6895, 139.6917], name: "Tokyo, Japan" },
];

const LeafletMap = () => {
  return (
    <MapContainer
      center={[25, 0]}
      zoom={2}
      scrollWheelZoom={false}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />

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
        {locations.map((location, index) => (
          <Marker
            key={index}
            position={location.position as L.LatLngExpression}
            icon={blackDotIcon}
          >
            <Popup>
              Request from <br /> {location.name}
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
};

export default LeafletMap;
