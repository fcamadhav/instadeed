'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, Settings as SettingsIcon, Palette, Key, Eye, EyeOff, Loader2 } from 'lucide-react';

interface GeneralSettings {
  siteName: string;
  logo: string;
  favicon: string;
  timezone: string;
  currency: string;
}

interface ThemeSettings {
  theme: 'light' | 'dark';
  customCss: string;
  customJs: string;
  maintenanceMode: boolean;
}

interface APIKeyEntry {
  _id?: string;
  provider: string;
  keyValue: string;
  hidden: boolean;
}

export default function SettingsPage() {
  const [tab, setTab] = useState<'general' | 'theme' | 'api'>('general');
  const [general, setGeneral] = useState<GeneralSettings>({ siteName: 'INSTADEED', logo: '', favicon: '', timezone: 'Asia/Kolkata', currency: 'INR' });
  const [theme, setTheme] = useState<ThemeSettings>({ theme: 'light', customCss: '', customJs: '', maintenanceMode: false });
  const [apiKeys, setApiKeys] = useState<APIKeyEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchSettings(); }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const [gRes, tRes, aRes] = await Promise.all([
        apiGet<{ data: GeneralSettings }>('/admin/settings/general').catch(() => null),
        apiGet<{ data: ThemeSettings }>('/admin/settings/theme').catch(() => null),
        apiGet<{ data: { keys: APIKeyEntry[] } }>('/admin/settings/api-keys').catch(() => null),
      ]);
      if (gRes?.data) setGeneral(gRes.data);
      if (tRes?.data) setTheme(tRes.data);
      if (aRes?.data?.keys) setApiKeys(aRes.data.keys);
    } catch {} finally { setLoading(false); }
  };

  const saveGeneral = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try { await apiPut('/admin/settings/general', general); toast.success('General settings saved'); } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const saveTheme = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try { await apiPut('/admin/settings/theme', theme); toast.success('Theme settings saved'); } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  if (loading) return <AdminLayout title="Settings"><div className="card p-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div></AdminLayout>;

  return (
    <AdminLayout title="Settings">
      <div className="flex gap-1 bg-slate-100 dark:bg-slate-700 rounded-lg p-1 mb-6 w-fit">
        {([
          { key: 'general' as const, label: 'General', icon: SettingsIcon },
          { key: 'theme' as const, label: 'Theme', icon: Palette },
          { key: 'api' as const, label: 'API Keys', icon: Key },
        ]).map(t => (
          <button key={t.key} onClick={() => setTab(t.key)} className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${tab === t.key ? 'bg-white dark:bg-slate-800 shadow-sm text-admin-600 dark:text-admin-400 font-medium' : 'text-slate-500'}`}>
            <t.icon className="w-3.5 h-3.5" /> {t.label}
          </button>
        ))}
      </div>

      {tab === 'general' && (
        <div className="card p-6 max-w-2xl">
          <form onSubmit={saveGeneral} className="space-y-4">
            <FormField label="Site Name" value={general.siteName} onChange={e => setGeneral({ ...general, siteName: e.target.value })} />
            <FormField label="Logo URL" value={general.logo} onChange={e => setGeneral({ ...general, logo: e.target.value })} />
            <FormField label="Favicon URL" value={general.favicon} onChange={e => setGeneral({ ...general, favicon: e.target.value })} />
            <div className="grid grid-cols-2 gap-4">
              <FormField type="select" label="Timezone" value={general.timezone} onChange={e => setGeneral({ ...general, timezone: e.target.value })} options={[
                { value: 'Asia/Kolkata', label: 'Asia/Kolkata (IST)' },
                { value: 'UTC', label: 'UTC' },
                { value: 'America/New_York', label: 'America/New_York' },
                { value: 'Europe/London', label: 'Europe/London' },
              ]} />
              <FormField type="select" label="Currency" value={general.currency} onChange={e => setGeneral({ ...general, currency: e.target.value })} options={[
                { value: 'INR', label: 'INR (₹)' },
                { value: 'USD', label: 'USD ($)' },
                { value: 'EUR', label: 'EUR (€)' },
                { value: 'GBP', label: 'GBP (£)' },
              ]} />
            </div>
            <button type="submit" disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save'}</button>
          </form>
        </div>
      )}

      {tab === 'theme' && (
        <div className="card p-6 max-w-2xl">
          <form onSubmit={saveTheme} className="space-y-4">
            <FormField type="select" label="Default Theme" value={theme.theme} onChange={e => setTheme({ ...theme, theme: e.target.value as any })} options={[{ value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }]} />
            <FormField label="Custom CSS" type="textarea" value={theme.customCss} onChange={e => setTheme({ ...theme, customCss: e.target.value })} rows={5} helperText="Add custom CSS styles" />
            <FormField label="Custom JavaScript" type="textarea" value={theme.customJs} onChange={e => setTheme({ ...theme, customJs: e.target.value })} rows={5} helperText="Add custom JavaScript" />
            <FormField label="Maintenance Mode" type="toggle" checked={theme.maintenanceMode} onChange={v => setTheme({ ...theme, maintenanceMode: v })} />
            <button type="submit" disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save'}</button>
          </form>
        </div>
      )}

      {tab === 'api' && (
        <div className="card p-6 max-w-2xl">
          <h3 className="section-title mb-4">API Keys</h3>
          <div className="space-y-3">
            {apiKeys.map((key, i) => (
              <div key={key._id || i} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">{key.provider}</p>
                  <p className="text-xs font-mono text-slate-500">{key.hidden ? '••••••••' + key.keyValue.slice(-4) : key.keyValue}</p>
                </div>
                <button onClick={() => {
                  const keys = [...apiKeys];
                  keys[i] = { ...keys[i], hidden: !keys[i].hidden };
                  setApiKeys(keys);
                }} className="text-slate-400 hover:text-slate-600">
                  {key.hidden ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                </button>
              </div>
            ))}
            {apiKeys.length === 0 && <p className="text-sm text-slate-400 text-center py-4">No API keys configured.</p>}
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
