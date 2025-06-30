// components/dashboard/ActivityList.tsx
import React from "react";

interface ActivityListProps {
  title: string;
  items: string[];
}

const ActivityList: React.FC<ActivityListProps> = ({ title, items }) => {
  return (
    <div className="bg-white border border-black p-6 rounded-lg overflow-x-scroll">
      <h2 className="text-lg font-bold text-black mb-4">{title}</h2>
      <ul className="space-y-3">
        {items.map((item, index) => (
          <li
            key={index}
            className="text-xs text-gray-800 border-b border-gray-200 pb-2 font-mono truncate"
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ActivityList;
