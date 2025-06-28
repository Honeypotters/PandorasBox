// app/logs/page.tsx

import Header from '../components/Header';
import LogViewer from '../components/logs/LogViewer';

export default function LogsPage() {
  return (
    <div className="min-h-screen bg-gray-100 w-full">
      <Header />
      <main className="p-6 pt-28">
        <h1 className="text-3xl font-bold mb-6 text-black text-center">System Logs</h1>
        <LogViewer />
      </main>
    </div>
  );
}
