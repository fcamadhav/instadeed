'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Copy } from 'lucide-react';

interface Coupon {
  id: string;
  code: string;
  type: 'percentage' | 'fixed';
  value: number;
  minOrder: number;
  maxUses: number;
  usedCount: number;
  expiryDate: string;
  status: boolean;
  applicableServices: string[];
  applicableCategories: string[];
}

interface Service { id: string; name: string }
interface Category { id: string; name: string }

const emptyForm: { code: string; type: 'percentage' | 'fixed'; value: number; minOrder: number; maxUses: number; expiryDate: string; status: boolean; applicableServices: string[]; applicableCategories: string[] } = { code: '', type: 'percentage', value: 0, minOrder: 0, maxUses: 0, expiryDate: '', status: true, applicableServices: [], applicableCategories: [] };

export default function CouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  useEffect(() => { fetchData(); }, [page]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [cpRes, svRes, ctRes] = await Promise.all([
        apiGet<{ data: { coupons: Coupon[]; page: number; totalPages: number; total: number } }>(`/admin/coupons?page=${page}&limit=10`),
        apiGet<{ data: { services: Service[] } }>('/admin/services?limit=500'),
        apiGet<{ data: { categories: Category[] } }>('/admin/categories?limit=500'),
      ]);
      if (cpRes.data) { setCoupons(cpRes.data.coupons || []); setTotalPages(cpRes.data.totalPages || 1); setTotal(cpRes.data.total || 0); }
      if (svRes.data) setServices(svRes.data.services || []);
      if (ctRes.data) setCategories(ctRes.data.categories || []);
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const openCreate = () => { setEditing(null); setForm(emptyForm); setErrors({}); setModalOpen(true); };
  const openEdit = (c: Coupon) => { setEditing(c.id); setForm({ code: c.code, type: c.type, value: c.value, minOrder: c.minOrder, maxUses: c.maxUses, expiryDate: c.expiryDate ? new Date(c.expiryDate).toISOString().split('T')[0] : '', status: c.status, applicableServices: c.applicableServices || [], applicableCategories: c.applicableCategories || [] }); setErrors({}); setModalOpen(true); };

  const validate = () => {
    const errs: Record<string, string> = {};
    if (!form.code.trim()) errs.code = 'Code is required';
    if (!form.value || form.value <= 0) errs.value = 'Value must be positive';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    try {
      if (editing) { await apiPut(`/admin/coupons/${editing}`, form); toast.success('Coupon updated'); }
      else { await apiPost('/admin/coupons', form); toast.success('Coupon created'); }
      setModalOpen(false);
      fetchData();
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const handleDelete = async (id: string) => {
    try { await apiDelete(`/admin/coupons/${id}`); toast.success('Coupon deleted'); setDeleteConfirm(null); fetchData(); } catch (err: any) { toast.error(err.message); }
  };

  const generateCode = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 8; i++) code += chars.charAt(Math.floor(Math.random() * chars.length));
    setForm({ ...form, code });
  };

  const columns: Column<Coupon>[] = [
    { key: 'code', label: 'Code', sortable: true, render: (c) => <span className="font-mono font-bold text-sm text-admin-600 dark:text-admin-400">{c.code}</span> },
    { key: 'type', label: 'Type', render: (c) => <span className="badge-blue">{c.type}</span> },
    { key: 'value', label: 'Value', sortable: true, render: (c) => c.type === 'percentage' ? `${c.value}%` : `₹${c.value}` },
    { key: 'minOrder', label: 'Min Order', render: (c) => `₹${(c.minOrder || 0).toLocaleString('en-IN')}` },
    { key: 'maxUses', label: 'Max Uses', render: (c) => c.maxUses || '∞' },
    { key: 'usedCount', label: 'Used', render: (c) => c.usedCount || 0 },
    { key: 'expiryDate', label: 'Expiry', render: (c) => c.expiryDate ? new Date(c.expiryDate).toLocaleDateString('en-IN') : '—' },
    { key: 'status', label: 'Status', render: (c) => c.status ? <span className="badge-green">Active</span> : <span className="badge-red">Inactive</span> },
    { key: 'actions', label: '', render: (c) => (
      <div className="flex items-center gap-1">
        <button onClick={(e) => { e.stopPropagation(); navigator.clipboard.writeText(c.code); toast.success('Copied!'); }} className="btn-ghost btn-sm p-1.5"><Copy className="w-3.5 h-3.5" /></button>
        <button onClick={(e) => { e.stopPropagation(); openEdit(c); }} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button>
        <button onClick={(e) => { e.stopPropagation(); setDeleteConfirm(c.id); }} className="btn-ghost btn-sm p-1.5 text-red-500"><Trash2 className="w-3.5 h-3.5" /></button>
      </div>
    )},
  ];

  return (
    <AdminLayout title="Coupons">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500 dark:text-slate-400">Manage discount coupons</p>
        <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4" /> Add Coupon</button>
      </div>

      <DataTable columns={columns} data={coupons} loading={loading} error={error} onRetry={fetchData} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(c) => c.id} emptyMessage="No coupons yet" emptyDescription="Create coupons to offer discounts." />

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Coupon' : 'Add Coupon'} size="lg" footer={<><button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <div className="flex items-end gap-2">
            <div className="flex-1">
              <FormField label="Coupon Code" required value={form.code} onChange={e => setForm({ ...form, code: e.target.value.toUpperCase() })} error={errors.code} />
            </div>
            <button type="button" onClick={generateCode} className="btn-secondary btn-sm mb-1"><Copy className="w-3.5 h-3.5" /> Generate</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormField type="select" label="Type" value={form.type} onChange={e => setForm({ ...form, type: e.target.value as any })} options={[{ value: 'percentage', label: 'Percentage' }, { value: 'fixed', label: 'Fixed Amount' }]} />
            <FormField label="Value" type="number" required value={form.value} onChange={e => setForm({ ...form, value: parseFloat(e.target.value) || 0 })} error={errors.value} helperText={form.type === 'percentage' ? 'Discount percentage' : 'Discount amount in ₹'} />
            <FormField label="Min Order (₹)" type="number" value={form.minOrder} onChange={e => setForm({ ...form, minOrder: parseFloat(e.target.value) || 0 })} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormField label="Max Uses" type="number" value={form.maxUses} onChange={e => setForm({ ...form, maxUses: parseInt(e.target.value) || 0 })} helperText="0 for unlimited" />
            <FormField label="Expiry Date" type="date" value={form.expiryDate} onChange={e => setForm({ ...form, expiryDate: e.target.value })} />
            <FormField label="Active" type="toggle" checked={form.status} onChange={v => setForm({ ...form, status: v })} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">Applicable Services</label>
              <div className="max-h-32 overflow-y-auto border border-slate-200 dark:border-slate-700 rounded-lg p-2 space-y-1">
                {services.map(s => (
                  <label key={s.id} className="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300 cursor-pointer">
                    <input type="checkbox" checked={form.applicableServices.includes(s.id)} onChange={() => setForm({ ...form, applicableServices: form.applicableServices.includes(s.id) ? form.applicableServices.filter(id => id !== s.id) : [...form.applicableServices, s.id] })} className="rounded" />
                    {s.name}
                  </label>
                ))}
                {services.length === 0 && <p className="text-xs text-slate-400">No services</p>}
              </div>
            </div>
            <div>
              <label className="label">Applicable Categories</label>
              <div className="max-h-32 overflow-y-auto border border-slate-200 dark:border-slate-700 rounded-lg p-2 space-y-1">
                {categories.map(c => (
                  <label key={c.id} className="flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300 cursor-pointer">
                    <input type="checkbox" checked={form.applicableCategories.includes(c.id)} onChange={() => setForm({ ...form, applicableCategories: form.applicableCategories.includes(c.id) ? form.applicableCategories.filter(id => id !== c.id) : [...form.applicableCategories, c.id] })} className="rounded" />
                    {c.name}
                  </label>
                ))}
                {categories.length === 0 && <p className="text-xs text-slate-400">No categories</p>}
              </div>
            </div>
          </div>
        </form>
      </Modal>

      <Modal open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)} title="Delete Coupon" size="sm" footer={<><button onClick={() => setDeleteConfirm(null)} className="btn-secondary">Cancel</button><button onClick={() => deleteConfirm && handleDelete(deleteConfirm)} className="btn-danger">Delete</button></>}>
        <p className="text-sm text-slate-600 dark:text-slate-400">Are you sure? This cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
