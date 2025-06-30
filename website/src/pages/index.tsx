// app/dashboard/page.tsx

"use client";

import { useState, useEffect } from "react";
import Head from "next/head";
import Header from "@/components/Header";
import StatCard from "@/components/dashboard/StatCard";
import RequestMap from "@/components/dashboard/RequestMap";
import ActivityList from "@/components/dashboard/ActivityList";
import DonutChart from "@/components/dashboard/DonutChart";
import BarChart from "@/components/dashboard/BarChart";

interface Location {
  position: [number, number];
  name: string;
}

interface ChartData {
  name: string;
  value: number;
  color: string;
}

const API_BASE_URL = "http://localhost:8080";

const CATEGORY_COLORS: { [key: string]: string } = {
  "Reconnaissance & Scanning": "#9ca3af",
  "Exploitation Attempt": "#ef4444",
  "Internet Noise": "#d1d5db",
  "Manual Investigation": "#f97316",
  "Uncategorized or Novel": "#6b7280",
};

export default function DashboardPage() {
  const [requestsReceived, setRequestsReceived] = useState(0);
  const [avgResponseTime, setAvgResponseTime] = useState(0);
  const [uptime, setUptime] = useState(0);
  const [requestLocations, setRequestLocations] = useState<Location[]>([]);
  const [last10Requests, setLast10Requests] = useState<string[]>([]);
  const [last10Responses, setLast10Responses] = useState<string[]>([]);
  const [requestCategoryData, setRequestCategoryData] = useState<ChartData[]>(
    [],
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          uptimeRes,
          avgTimeRes,
          requestsCountRes,
          locationsRes,
          lastRequestsRes,
          lastResponsesRes,
          categoryCountsRes,
        ] = await Promise.all([
          fetch(`${API_BASE_URL}/uptime`),
          fetch(`${API_BASE_URL}/average-response-time`),
          fetch(`${API_BASE_URL}/request-count`),
          fetch(`${API_BASE_URL}/locations`),
          fetch(`${API_BASE_URL}/last-ten-requests`),
          fetch(`${API_BASE_URL}/last-ten-responses`),
          fetch(`${API_BASE_URL}/categorised-counts`),
        ]);

        const uptimeData = await uptimeRes.json();
        const avgTimeData = await avgTimeRes.json();
        const requestsCountData = await requestsCountRes.json();
        const locationsData = await locationsRes.json();
        const lastRequestsData = await lastRequestsRes.json();
        const lastResponsesData = await lastResponsesRes.json();
        const categoryCountsData = await categoryCountsRes.json();

        setUptime(uptimeData.uptime_minutes || 0);
        setAvgResponseTime(avgTimeData.average_response_time || 0);
        setRequestsReceived(requestsCountData.count || 0);
        setRequestLocations(locationsData.locations || []);

        if (
          !lastRequestsData.last_10_requests ||
          lastRequestsData.last_10_requests.length === 0
        ) {
          setLast10Requests(["", "", "", "", "", "", "", "", "", "", ""]);
        }
        if (
          !lastResponsesData.last_10_responses ||
          lastResponsesData.last_10_responses.length === 0
        ) {
          setLast10Responses(["", "", "", "", "", "", "", "", "", "", ""]);
        }

        if (categoryCountsData.counts) {
          const chartData = Object.entries(categoryCountsData.counts).map(
            ([name, value]) => ({
              name,
              value: value as number,
              color: CATEGORY_COLORS[name] || "#d1d5db",
            }),
          );
          setRequestCategoryData(chartData);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      }
    };

    fetchData();

    const intervalId = setInterval(fetchData, 5000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 text-black w-full">
      <Head>
        <title>Dashboard - Pandora's Box</title>
      </Head>
      <Header />
      <main className="p-6 pt-18">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard
            title="Requests Received"
            value={requestsReceived.toLocaleString()}
          />
          <StatCard
            title="Average Response Time"
            value={`${(avgResponseTime / 1000).toFixed(1)}s`}
          />
          <StatCard title="Uptime" value={`${Math.floor(uptime / 60)}hrs`} />

          <div className="md:col-span-2">
            <RequestMap locations={requestLocations} />
          </div>

          <div className="space-y-6">
            <ActivityList title="Last 10 Requests" items={last10Requests} />
            <ActivityList title="Last 10 Responses" items={last10Responses} />
          </div>

          <div className="md:col-span-1">
            <DonutChart title="Request Categories" data={requestCategoryData} />
          </div>
          <div className="md:col-span-2">
            <BarChart
              title="Request Volume by Category"
              data={requestCategoryData}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
