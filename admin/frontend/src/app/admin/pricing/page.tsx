'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, History, Loader2 } from 'lucide-react';

interface Service {
  _id: string;
  name: string;
}

interface Pricing {
  _id: string;
  service: string;
  currentPrice: number;
  oldPrice: number;
  discountPercent: number;
  gstPercent: number;
  convenienceFee: number;
  processingFee: number;
  deliveryCharge: number;
  offerBadge: string;
  limitedTime: boolean;
  subscriptionPrice: number | null;
  emiEnabled: boolean;
}

interface PriceHistory {
  _id: string;
  service: { _id: string; name: string };
  currentPrice: number;
  oldPrice: number;
  changedAt: string;
}

export default function PricingPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState('');
  const [pricing, setPricing] = useState<Pricing | null>(null);
  const [history, setHistory] = useState<PriceHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    currentPrice: 0, oldPrice: 0, discountPercent: 0, gstPercent: 18,
    convenienceFee: 0, processingFee: 0, deliveryCharge: 0, offerBadge: '',
    limitedTime: false, subscriptionPrice: 0, emiEnabled: false,
  });

  useEffect(() => {
    apiGet<{ data: { services: Service[] } }>('/admin/services?limit=500')
      .then(res => setServices(res.data?.services || []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedService) return;
    fetchPricing();
    fetchHistory();
  }, [selectedService]);

  const fetchPricing = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { pricing: Pricing } }>(`/admin/pricing/${selectedService}`);
      if (res.data?.pricing) {
        const p = res.data.pricing;
        setPricing(p);
        setForm({
          currentPrice: p.currentPrice || 0,
          oldPrice: p.oldPrice || 0,
          discountPercent: p.discountPercent || 0,
          gstPercent: p.gstPercent || 18,
          convenienceFee: p.convenienceFee || 0,
          processingFee: p.processingFee || 0,
          deliveryCharge: p.deliveryCharge || 0,
          offerBadge: p.offerBadge || '',
          limitedTime: p.limitedTime || false,
          subscriptionPrice: p.subscriptionPrice || 0,
          emiEnabled: p.emiEnabled || false,
        });
      } else {
        setPricing(null);
        setForm({ currentPrice: 0, oldPrice: 0, discountPercent: 0, gstPercent: 18, convenienceFee: 0, processingFee: 0, deliveryCharge: 0, offerBadge: '', limitedTime: false, subscriptionPrice: 0, emiEnabled: false });
      }
    } catch { setPricing(null); } finally { setLoading(false); }
  };

  const fetchHistory = async () => {
    try {
      const res = await apiGet<{ data: { history: PriceHistory[] } }>(`/admin/pricing/${selectedService}/history`);
      setHistory(res.data?.history || []);
    } catch { setHistory([]); }
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiPut(`/admin/pricing/${selectedService}`, form);
      toast.success('Pricing updated');
      fetchHistory();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  const historyColumns: Column<PriceHistory>[] = [
    { key: 'service', label: 'Service', render: (h) => h.service?.name || 'N/A' },
    { key: 'oldPrice', label: 'Old Price', render: (h) => `₹${h.oldPrice?.toLocaleString('en-IN') || 0}` },
    { key: 'currentPrice', label: 'New Price', render: (h) => `₹${h.currentPrice?.toLocaleString('en-IN') || 0}` },
    { key: 'changedAt', label: 'Changed At', render: (h) => new Date(h.changedAt).toLocaleString('en-IN') },
  ];

  return (
    <AdminLayout title="Pricing">
      <div className="max-w-2xl mb-6">
        <FormField
          type="select" label="Select Service"
          value={selectedService}
          onChange={e => setSelectedService(e.target.value)}
          options={[{ value: '', label: 'Choose a service...' }, ...services.map(s => ({ value: s._id, label: s.name }))]}
        />
      </div>

      {loading ? (
        <div className="card p-8 text-center">
          <Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" />
        </div>
      ) : selectedService ? (
        <>
          <div className="card p-6 mb-6">
            <h3 className="section-title mb-4">Pricing Details</h3>
            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField label="Current Price (₹)" type="number" value={form.currentPrice} onChange={e => setForm({ ...form, currentPrice: parseFloat(e.target.value) || 0 })} />
                <FormField label="Old Price (₹)" type="number" value={form.oldPrice} onChange={e => setForm({ ...form, oldPrice: parseFloat(e.target.value) || 0 })} />
                <FormField label="Discount %" type="number" value={form.discountPercent} onChange={e => setForm({ ...form, discountPercent: parseFloat(e.target.value) || 0 })} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField label="GST %" type="number" value={form.gstPercent} onChange={e => setForm({ ...form, gstPercent: parseFloat(e.target.value) || 0 })} />
                <FormField label="Convenience Fee (₹)" type="number" value={form.convenienceFee} onChange={e => setForm({ ...form, convenienceFee: parseFloat(e.target.value) || 0 })} />
                <FormField label="Processing Fee (₹)" type="number" value={form.processingFee} onChange={e => setForm({ ...form, processingFee: parseFloat(e.target.value) || 0 })} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField label="Delivery Charge (₹)" type="number" value={form.deliveryCharge} onChange={e => setForm({ ...form, deliveryCharge: parseFloat(e.target.value) || 0 })} />
                <FormField label="Offer Badge" value={form.offerBadge} onChange={e => setForm({ ...form, offerBadge: e.target.value })} placeholder="e.g., 20% OFF" />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <FormField label="Limited Time Offer" type="toggle" checked={form.limitedTime} onChange={v => setForm({ ...form, limitedTime: v })} />
                <FormField label="EMI Available" type="toggle" checked={form.emiEnabled} onChange={v => setForm({ ...form, emiEnabled: v })} />
                <FormField label="Subscription Price (₹)" type="number" value={form.subscriptionPrice} onChange={e => setForm({ ...form, subscriptionPrice: parseFloat(e.target.value) || 0 })} helperText="Set 0 if not applicable" />
              </div>
              <div className="pt-2">
                <button type="submit" disabled={saving} className="btn-primary">
                  <Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save Pricing'}
                </button>
              </div>
            </form>
          </div>

          <div>
            <h3 className="section-title mb-3 flex items-center gap-2"><History className="w-4 h-4" /> Price History</h3>
            <DataTable columns={historyColumns} data={history} loading={false} keyExtractor={(h) => h._id} emptyMessage="No price history" emptyDescription="Price changes will be recorded here." />
          </div>
        </>
      ) : (
        <div className="card p-8 text-center text-sm text-slate-500 dark:text-slate-400">
          Select a service to manage its pricing.
        </div>
      )}
    </AdminLayout>
  );
}
