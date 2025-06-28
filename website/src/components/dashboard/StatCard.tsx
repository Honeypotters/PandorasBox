// components/dashboard/StatCard.tsx
import React from 'react';

interface StatCardProps {
  title: string;
  value: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value }) => {
  return (
    <div className="bg-white border border-black p-6 rounded-lg flex flex-col justify-center items-start">
      <h2 className="text-sm font-medium text-gray-600 uppercase tracking-wider">{title}</h2>
      <p className="text-4xl font-bold text-black mt-2">{value}</p>
    </div>
  );
};

export default StatCard;
