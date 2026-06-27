'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { CreditCard, Save, Loader2, Check, X } from 'lucide-react';

const gatewayMeta: Record<string, string> = {
  RAZORPAY: 'Razorpay',
  CASHFREE: 'Cashfree',
  PHONEPE: 'PhonePe',
  PAYU: 'PayU',
  STRIPE: 'Stripe',
  MANUAL_UPI: 'Manual UPI',
  BANK_TRANSFER: 'Bank Transfer',
};

interface Gateway {
  id: string;
  gateway: string;
  isEnabled: boolean;
  isTestMode: boolean;
  isDefault: boolean;
  apiKey: string | null;
  apiSecret: string | null;
  webhookSecret: string | null;
  successUrl: string | null;
  failureUrl: string | null;
  paymentTimeout: number;
}

export default function PaymentsPage() {
  const [gateways, setGateways] = useState<Gateway[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<Gateway | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({ apiKey: '', apiSecret: '', webhookSecret: '', successUrl: '', failureUrl: '', paymentTimeout: 300 });
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchGateways(); }, []);

  const fetchGateways = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiGet<{ data: Gateway[] }>('/admin/payment-gateways');
      setGateways(Array.isArray(res.data) ? res.data : []);
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const toggleEnabled = async (g: Gateway) => {
    try {
      await apiPut(`/admin/payment-gateways/${g.gateway}`, { isEnabled: !g.isEnabled });
      toast.success(`${gatewayMeta[g.gateway] || g.gateway} ${g.isEnabled ? 'disabled' : 'enabled'}`);
      fetchGateways();
    } catch (err: any) { toast.error(err.message); }
  };

  const toggleTestMode = async (g: Gateway) => {
    try {
      await apiPut(`/admin/payment-gateways/${g.gateway}`, { isTestMode: !g.isTestMode });
      toast.success(`Test mode ${g.isTestMode ? 'disabled' : 'enabled'}`);
      fetchGateways();
    } catch (err: any) { toast.error(err.message); }
  };

  const openEdit = (g: Gateway) => {
    setEditing(g);
    setForm({ apiKey: g.apiKey || '', apiSecret: '', webhookSecret: '', successUrl: g.successUrl || '', failureUrl: g.failureUrl || '', paymentTimeout: g.paymentTimeout || 300 });
    setModalOpen(true);
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    if (!editing) return;
    setSaving(true);
    try {
      await apiPut(`/admin/payment-gateways/${editing.gateway}`, form);
      toast.success('Gateway updated');
      setModalOpen(false);
      fetchGateways();
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  if (error) {
    return (
      <AdminLayout title="Payment Gateways">
        <div className="card p-8 text-center">
          <p className="text-sm text-red-500 mb-3">{error}</p>
          <button onClick={fetchGateways} className="btn-primary btn-sm">Retry</button>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout title="Payment Gateways">
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">Configure payment gateway integrations</p>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="card p-5"><div className="skeleton h-6 w-32 mb-3" /><div className="skeleton h-4 w-20 mb-2" /><div className="skeleton h-4 w-24" /></div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {gateways.map(g => {
            const label = gatewayMeta[g.gateway] || g.gateway;
            return (
              <div key={g.id} className="card p-5 hover:shadow-md transition-shadow cursor-pointer" onClick={() => openEdit(g)}>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-admin-50 dark:bg-admin-900/30 flex items-center justify-center">
                      <CreditCard className="w-5 h-5 text-admin-600 dark:text-admin-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-900 dark:text-white text-sm">{label}</h3>
                      {g.isDefault && <span className="badge-blue text-[10px]">Default</span>}
                    </div>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Enabled</span>
                    <button onClick={(e) => { e.stopPropagation(); toggleEnabled(g); }} className={`relative w-9 h-5 rounded-full transition-colors ${g.isEnabled ? 'bg-green-500' : 'bg-slate-300 dark:bg-slate-600'}`}>
                      <span className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${g.isEnabled ? 'translate-x-4' : ''}`} />
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Test Mode</span>
                    <button onClick={(e) => { e.stopPropagation(); toggleTestMode(g); }} className={`relative w-9 h-5 rounded-full transition-colors ${g.isTestMode ? 'bg-amber-500' : 'bg-slate-300 dark:bg-slate-600'}`}>
                      <span className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${g.isTestMode ? 'translate-x-4' : ''}`} />
                    </button>
                  </div>
                </div>

                <div className="mt-3 pt-3 border-t border-slate-100 dark:border-slate-700 text-xs text-slate-400">
                  {g.isEnabled ? 'Click to configure API keys' : 'Click to enable'}
                </div>
              </div>
            );
          })}
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={`Configure ${editing ? gatewayMeta[editing.gateway] || editing.gateway : ''}`} size="lg" footer={<><button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="API Key" value={form.apiKey} onChange={e => setForm({ ...form, apiKey: (e as any).target?.value || '' })} />
            <FormField label="API Secret" value={form.apiSecret} onChange={e => setForm({ ...form, apiSecret: (e as any).target?.value || '' })} />
          </div>
          <FormField label="Webhook Secret" value={form.webhookSecret} onChange={e => setForm({ ...form, webhookSecret: (e as any).target?.value || '' })} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Success URL" value={form.successUrl} onChange={e => setForm({ ...form, successUrl: (e as any).target?.value || '' })} />
            <FormField label="Failure URL" value={form.failureUrl} onChange={e => setForm({ ...form, failureUrl: (e as any).target?.value || '' })} />
          </div>
          <FormField label="Timeout (seconds)" type="number" value={String(form.paymentTimeout)} onChange={e => setForm({ ...form, paymentTimeout: parseInt((e as any).target?.value) || 300 })} />
        </form>
      </Modal>
    </AdminLayout>
  );
}
