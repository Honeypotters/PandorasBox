// components/dashboard/BarChart.tsx
"use client";

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, LabelList, Cell } from 'recharts';

interface ChartDataItem {
  name: string;
  value: number;
  color: string;
}

interface BarChartProps {
  title: string;
  data: ChartDataItem[];
}

const BarChartComponent: React.FC<BarChartProps> = ({ title, data }) => {
  return (
    <div className="bg-white border border-black p-6 rounded-lg h-full">
      <h2 className="text-lg font-bold text-black mb-4">{title}</h2>
      <div className="w-full h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
          >
            <XAxis type="number" hide />
            <YAxis
              type="category"
              dataKey="name"
              axisLine={false}
              tickLine={false}
              width={120}
              tick={{ fill: '#374151', fontSize: 14 }}
            />
            <Tooltip
              cursor={{ fill: 'rgba(243, 244, 246, 0.5)' }}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                border: '1px solid #000',
                borderRadius: '0.5rem'
              }}
            />
            <Bar dataKey="value" barSize={25} radius={[0, 4, 4, 0]}>
              <LabelList dataKey="value" position="right" style={{ fill: '#1f2937', fontSize: 12 }} />
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BarChartComponent;
