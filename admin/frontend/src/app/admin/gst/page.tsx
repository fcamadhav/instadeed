'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, Building, CreditCard, Upload, Eye, Loader2 } from 'lucide-react';

interface GSTSettings {
  gstNumber: string;
  gstRate: number;
  sacCode: string;
  invoicePrefix: string;
  invoiceFooter: string;
  bankName: string;
  bankAccount: string;
  bankIfsc: string;
  bankBranch: string;
  invoiceLogo?: string;
  qrCode?: string;
}

export default function GSTPage() {
  const [settings, setSettings] = useState<GSTSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState<GSTSettings>({
    gstNumber: '', gstRate: 18, sacCode: '', invoicePrefix: 'INV-',
    invoiceFooter: '', bankName: '', bankAccount: '', bankIfsc: '',
    bankBranch: '',
  });

  useEffect(() => { fetchSettings(); }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { settings: GSTSettings } }>('/admin/gst');
      if (res.data?.settings) {
        setSettings(res.data.settings);
        setForm(res.data.settings);
      }
    } catch (err: any) { setError(err.message || 'Failed to load GST settings'); } finally { setLoading(false); }
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiPut('/admin/gst', form);
      toast.success('GST settings saved');
      fetchSettings();
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  if (loading) return <AdminLayout title="GST & Tax"><div className="card p-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div></AdminLayout>;

  return (
    <AdminLayout title="GST & Tax">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card p-6">
            <h3 className="section-title mb-4">GST Configuration</h3>
            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField label="GST Number" value={form.gstNumber} onChange={e => setForm({ ...form, gstNumber: e.target.value })} placeholder="22AAAAA0000A1Z5" />
                <FormField label="GST Rate (%)" type="number" value={form.gstRate} onChange={e => setForm({ ...form, gstRate: parseFloat(e.target.value) || 0 })} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField label="SAC Code" value={form.sacCode} onChange={e => setForm({ ...form, sacCode: e.target.value })} placeholder="e.g., 9983" />
                <FormField label="Invoice Prefix" value={form.invoicePrefix} onChange={e => setForm({ ...form, invoicePrefix: e.target.value })} placeholder="INV-" />
              </div>
              <FormField label="Invoice Footer" type="textarea" value={form.invoiceFooter} onChange={e => setForm({ ...form, invoiceFooter: e.target.value })} rows={3} placeholder="Terms & conditions..." />
            </form>
          </div>

          <div className="card p-6">
            <h3 className="section-title mb-4">Bank Details</h3>
            <form onSubmit={handleSave} className="space-y-4">
              <FormField label="Bank Name" value={form.bankName} onChange={e => setForm({ ...form, bankName: e.target.value })} placeholder="State Bank of India" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField label="Account Number" value={form.bankAccount} onChange={e => setForm({ ...form, bankAccount: e.target.value })} />
                <FormField label="IFSC Code" value={form.bankIfsc} onChange={e => setForm({ ...form, bankIfsc: e.target.value })} placeholder="SBIN0001234" />
              </div>
              <FormField label="Branch" value={form.bankBranch} onChange={e => setForm({ ...form, bankBranch: e.target.value })} />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label">Invoice Logo</label>
                  <div className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg p-4 text-center cursor-pointer hover:border-admin-400 transition-colors">
                    <Upload className="w-6 h-6 text-slate-400 mx-auto mb-1" />
                    <p className="text-xs text-slate-500">Click to upload logo</p>
                  </div>
                </div>
                <div>
                  <label className="label">QR Code</label>
                  <div className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg p-4 text-center cursor-pointer hover:border-admin-400 transition-colors">
                    <Upload className="w-6 h-6 text-slate-400 mx-auto mb-1" />
                    <p className="text-xs text-slate-500">Click to upload QR code</p>
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <button onClick={handleSave} disabled={saving} className="btn-primary">
                  <Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save All Settings'}
                </button>
              </div>
            </form>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="card p-6 sticky top-24">
            <h3 className="section-title mb-4 flex items-center gap-2"><Eye className="w-4 h-4" /> Preview</h3>
            <div className="border border-slate-200 dark:border-slate-700 rounded-lg p-4 space-y-2 text-sm">
              <p className="font-semibold text-slate-900 dark:text-white">TAX INVOICE</p>
              <p><span className="text-slate-500">GST:</span> {form.gstNumber || '—'}</p>
              <p><span className="text-slate-500">SAC:</span> {form.sacCode || '—'}</p>
              <p><span className="text-slate-500">Rate:</span> {form.gstRate}%</p>
              <p><span className="text-slate-500">Invoice:</span> {form.invoicePrefix}0001</p>
              <hr className="border-slate-200 dark:border-slate-700" />
              <p className="text-xs text-slate-400">{form.invoiceFooter || 'No footer set'}</p>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}
