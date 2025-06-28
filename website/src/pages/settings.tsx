// app/settings/page.tsx

import Header from '@/components/Header';
import SettingsSection from '@/components/settings/SettingsSection';

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="p-6 pt-28 max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-black">Settings</h1>

        <SettingsSection
          title="General Settings"
          description="Configure general application settings and preferences."
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label htmlFor="dark-mode" className="text-sm font-medium text-gray-700">
                Enable Dark Mode
              </label>
              <button
                type="button"
                className="bg-gray-200 relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2"
                role="switch"
                aria-checked="false"
              >
                <span className="translate-x-0 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
              </button>
            </div>
          </div>
        </SettingsSection>

        <SettingsSection
          title="API Configuration"
          description="Manage API keys and data retention policies for your honeypot."
        >
          <div className="space-y-4">
            <div>
              <label htmlFor="api-key" className="block text-sm font-medium text-gray-700">
                API Key
              </label>
              <input
                type="password"
                name="api-key"
                id="api-key"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm"
                defaultValue="••••••••••••••••"
              />
            </div>
            <div>
              <label htmlFor="retention-policy" className="block text-sm font-medium text-gray-700">
                Data Retention Policy
              </label>
              <select
                id="retention-policy"
                name="retention-policy"
                className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-black focus:outline-none focus:ring-black sm:text-sm"
                defaultValue="30"
              >
                <option value="7">7 Days</option>
                <option value="30">30 Days</option>
                <option value="90">90 Days</option>
                <option value="forever">Indefinitely</option>
              </select>
            </div>
          </div>
        </SettingsSection>

        <SettingsSection
          title="Notifications"
          description="Choose how you want to be notified of activity."
        >
          <div className="space-y-4">
            <div>
              <label htmlFor="alert-email" className="block text-sm font-medium text-gray-700">
                Alert Email Address
              </label>
              <input
                type="email"
                name="alert-email"
                id="alert-email"
                placeholder="you@example.com"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-black focus:ring-black sm:text-sm"
              />
            </div>
            <fieldset>
              <legend className="text-sm font-medium text-gray-700">Notify me on...</legend>
              <div className="mt-2 space-y-2">
                <div className="relative flex items-start">
                  <div className="flex h-5 items-center">
                    <input id="high-threat" name="high-threat" type="checkbox" className="h-4 w-4 rounded border-gray-300 text-black focus:ring-black" />
                  </div>
                  <div className="ml-3 text-sm">
                    <label htmlFor="high-threat" className="text-gray-700">High-Threat Prompt</label>
                  </div>
                </div>
                <div className="relative flex items-start">
                  <div className="flex h-5 items-center">
                    <input id="system-error" name="system-error" type="checkbox" className="h-4 w-4 rounded border-gray-300 text-black focus:ring-black" />
                  </div>
                  <div className="ml-3 text-sm">
                    <label htmlFor="system-error" className="text-gray-700">System Error or Failure</label>
                  </div>
                </div>
              </div>
            </fieldset>
          </div>
        </SettingsSection>
        
      </main>
    </div>
  );
}
