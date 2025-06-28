// components/dashboard/DonutChart.tsx
"use client";

import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

interface ChartDataItem {
  name: string;
  value: number;
  color: string;
}

interface DonutChartProps {
  title: string;
  data: ChartDataItem[];
}

const DonutChart: React.FC<DonutChartProps> = ({ title, data }) => {
  return (
    <div className="bg-white border border-black p-6 rounded-lg h-full flex flex-col">
      <h2 className="text-lg font-bold text-black mb-4">{title}</h2>
      <div className="flex-grow">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip
              cursor={{ fill: "transparent" }}
              contentStyle={{
                backgroundColor: "rgba(255, 255, 255, 0.8)",
                border: "1px solid #000",
                borderRadius: "0.5rem",
              }}
            />
            <Legend iconType="circle" />
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default DonutChart;
