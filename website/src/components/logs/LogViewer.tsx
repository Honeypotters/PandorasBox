// components/logs/LogViewer.tsx
"use client";

import { useState, useEffect } from "react";

const API_BASE_URL = "http://localhost:8080/";

const LogViewer = () => {
  const [logContent, setLogContent] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLogs = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(API_BASE_URL + "logfile");

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.text();
        setLogContent(data);

      } catch (err) {
        if (err instanceof Error) {
          setError(`Failed to load logs: ${err.message}`);
        } else {
          setError("An unknown error occurred.");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchLogs();
  }, []);

  return (
    <div className="bg-white border border-gray-700 rounded-lg shadow-2xl h-[60vh] flex flex-col">
      <div className="p-4 text-sm font-mono flex-grow overflow-y-auto">
        {isLoading ? (
          <p className="text-yellow-400">Fetching logs...</p>
        ) : error ? (
          <p className="text-red-500">Error: {error}</p>
        ) : (
          <pre className="text-black whitespace-pre-wrap">{logContent}</pre>
        )}
      </div>
    </div>
  );
};

export default LogViewer;
