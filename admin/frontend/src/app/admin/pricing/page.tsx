'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, History, Loader2 } from 'lucide-react';

interface Service { id: string; name: string; }
interface PricingData { id: string; currentPrice: number; oldPrice: number | null; discountPercent: number | null; gstPercent: number; convenienceFee: number; processingFee: number; deliveryCharge: number; offerBadge: string | null; isLimitedOffer: boolean; subscriptionPrice: number | null; emiAvailable: boolean; }

export default function PricingPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState('');
  const [pricing, setPricing] = useState<PricingData | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ currentPrice: 0, oldPrice: 0, gstPercent: 18, convenienceFee: 0, processingFee: 0, deliveryCharge: 0, offerBadge: '', isLimitedOffer: false, subscriptionPrice: 0, emiAvailable: false });

  useEffect(() => {
    apiGet<{ data: { services: Service[] } }>('/admin/services?limit=500')
      .then(res => setServices(res.data?.services || [])).catch((err: any) => toast.error(err.message || 'Failed to load services'));
  }, []);

  useEffect(() => { if (!selectedService) return; fetchPricing(); fetchHistory(); }, [selectedService]);

  const fetchPricing = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: PricingData }>(`/admin/pricing/${selectedService}`);
      if (res.data) {
        const p = res.data; setPricing(p);
        setForm({ currentPrice: p.currentPrice||0, oldPrice: p.oldPrice||0, gstPercent: p.gstPercent||18, convenienceFee: p.convenienceFee||0, processingFee: p.processingFee||0, deliveryCharge: p.deliveryCharge||0, offerBadge: p.offerBadge||'', isLimitedOffer: p.isLimitedOffer||false, subscriptionPrice: p.subscriptionPrice||0, emiAvailable: p.emiAvailable||false });
      }
    } catch { toast.error('Failed to load pricing'); setPricing(null); } finally { setLoading(false); }
  };

  const fetchHistory = async () => {
    try {
      const res = await apiGet<{ data: any[] }>(`/admin/pricing/${selectedService}/history`);
      setHistory(res.data || []);
    } catch { toast.error('Failed to load pricing history'); setHistory([]); }
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault(); setSaving(true);
    try { await apiPut(`/admin/pricing/${selectedService}`, form); toast.success('Pricing updated'); fetchHistory(); }
    catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  return (
    <AdminLayout title="Pricing">
      <div className="max-w-2xl mb-6">
        <FormField type="select" label="Select Service" value={selectedService} onChange={e => setSelectedService(e.target.value)}
          options={[{value:'',label:'Choose a service...'}, ...services.map(s => ({value:s.id, label:s.name}))]} />
      </div>
      {loading ? <div className="card p-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto"/></div>
      : selectedService ? <>
        <div className="card p-6 mb-6">
          <h3 className="section-title mb-4">Pricing Details</h3>
          <form onSubmit={handleSave} className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <FormField label="Current Price (₹)" type="number" value={form.currentPrice} onChange={e => setForm({...form, currentPrice: parseFloat(e.target.value)||0})}/>
              <FormField label="Old Price (₹)" type="number" value={form.oldPrice} onChange={e => setForm({...form, oldPrice: parseFloat(e.target.value)||0})}/>
              <FormField label="GST %" type="number" value={form.gstPercent} onChange={e => setForm({...form, gstPercent: parseFloat(e.target.value)||0})}/>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <FormField label="Convenience Fee (₹)" type="number" value={form.convenienceFee} onChange={e => setForm({...form, convenienceFee: parseFloat(e.target.value)||0})}/>
              <FormField label="Processing Fee (₹)" type="number" value={form.processingFee} onChange={e => setForm({...form, processingFee: parseFloat(e.target.value)||0})}/>
              <FormField label="Delivery Charge (₹)" type="number" value={form.deliveryCharge} onChange={e => setForm({...form, deliveryCharge: parseFloat(e.target.value)||0})}/>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <FormField label="Offer Badge" value={form.offerBadge} onChange={e => setForm({...form, offerBadge: e.target.value})} placeholder="e.g., 20% OFF"/>
              <FormField label="Subscription Price (₹)" type="number" value={form.subscriptionPrice} onChange={e => setForm({...form, subscriptionPrice: parseFloat(e.target.value)||0})} helperText="0 = not applicable"/>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <FormField label="Limited Time Offer" type="toggle" checked={form.isLimitedOffer} onChange={v => setForm({...form, isLimitedOffer: v})}/>
              <FormField label="EMI Available" type="toggle" checked={form.emiAvailable} onChange={v => setForm({...form, emiAvailable: v})}/>
            </div>
            <div className="pt-2"><button type="submit" disabled={saving} className="btn-primary"><Save className="w-4 h-4"/> {saving?'Saving...':'Save Pricing'}</button></div>
          </form>
        </div>
        <div><h3 className="section-title mb-3"><History className="w-4 h-4 inline mr-1"/>Price History</h3>
          <DataTable columns={[{key:'oldPrice',label:'Old Price',render:(h:any)=>`₹${(h.oldPrice||0).toLocaleString('en-IN')}`},{key:'currentPrice',label:'New Price',render:(h:any)=>`₹${(h.currentPrice||0).toLocaleString('en-IN')}`},{key:'gstPercent',label:'GST %'},{key:'createdAt',label:'Date',render:(h:any)=>new Date(h.createdAt).toLocaleString('en-IN')}]} data={history} loading={false} keyExtractor={h=>h.id} emptyMessage="No price history"/>
        </div>
      </> : <div className="card p-8 text-center text-sm text-slate-500">Select a service to manage pricing.</div>}
    </AdminLayout>
  );
}
