// components/settings/SettingsSection.tsx

import React from 'react';

interface SettingsSectionProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

const SettingsSection: React.FC<SettingsSectionProps> = ({ title, description, children }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm mb-10">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        <p className="mt-1 text-sm text-gray-600">{description}</p>
      </div>
      
      <div className="p-6">
        {children}
      </div>

      <div className="bg-gray-50 p-4 text-right rounded-b-lg">
        <button
          type="button"
          className="bg-black text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
};

export default SettingsSection;
