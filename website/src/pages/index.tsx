// app/dashboard/page.tsx
import Head from 'next/head';
import Header from '@/components/Header';
import StatCard from '@/components/dashboard/StatCard';
import RequestMap from '@/components/dashboard/RequestMap';
import ActivityList from '@/components/dashboard/ActivityList';

import DonutChart from '@/components/dashboard/DonutChart';
import BarChart from '@/components/dashboard/BarChart';

// --- MOCK DATA ---
const last10Requests = [
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
];

const last10Responses = [
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
  '', 
];

const requestCategoryData = [
  { name: 'Prompt Injection', value: 452, color: '#1f2937' },
  { name: 'Data Exfiltration', value: 310, color: '#4b5563' },
  { name: 'Jailbreaking', value: 281, color: '#6b7280' },
  { name: 'Reconnaissance', value: 159, color: '#9ca3af' },
  { name: 'Other', value: 226, color: '#d1d5db' },
];

// --- END MOCK DATA ---


export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-100 text-black w-full">
    <Head>
        <title>Dashboard - Pandora's Box</title>
    </Head>
      <Header />
      <main className="p-6 pt-18">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <StatCard title="Requests Received" value="1,428" />
          <StatCard title="Average Response Time" value="1.2s" />
          <StatCard title="Uptime" value="1337hrs" />

          <div className="md:col-span-2">
            <RequestMap />
          </div>

          <div className="space-y-6">
            <ActivityList title="Last 10 Requests" items={last10Requests} />
            <ActivityList title="Last 10 Responses" items={last10Responses} />
          </div>

          <div className="md:col-span-1">
             <DonutChart title="Request Categories" data={requestCategoryData} />
          </div>
          <div className="md:col-span-2">
            <BarChart title="Request Volume by Category" data={requestCategoryData} />
          </div>

        </div>
      </main>
    </div>
  );
}
