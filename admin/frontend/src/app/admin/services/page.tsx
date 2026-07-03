'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Star } from 'lucide-react';

interface Service {
  id: string;
  name: string;
  slug: string;
  category: { id: string; name: string } | null;
  pricing: { currentPrice: number; gstPercent: number; offerBadge: string | null; oldPrice: number | null } | null;
  status: string;
  isFeatured: boolean;
  showOnHomepage: boolean;
  sortOrder: number;
  shortDescription?: string;
  deliveryTime?: string;
  processingTime?: string;
  _count?: { orders: number };
}

interface Category {
  id: string;
  name: string;
}

interface FormData {
  name: string;
  slug: string;
  categoryId: string;
  shortDescription: string;
  longDescription: string;
  deliveryTime: string;
  processingTime: string;
  sortOrder: number;
  isFeatured: boolean;
  showOnHomepage: boolean;
  price: number;
  seoTitle: string;
  seoDescription: string;
}

const emptyForm: FormData = {
  name: '', slug: '', categoryId: '', shortDescription: '', longDescription: '',
  deliveryTime: '', processingTime: '', sortOrder: 0, isFeatured: false,
  showOnHomepage: true, price: 0, seoTitle: '', seoDescription: '',
};

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [saving, setSaving] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => { fetchData(); }, [page]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [sRes, cRes] = await Promise.all([
        apiGet<{ data: { services: Service[]; pagination: { totalPages: number } } }>(`/admin/services?page=${page}&limit=10`),
        apiGet<{ data: { categories: Category[] } }>('/admin/categories'),
      ]);
      if (sRes.data) {
        setServices(sRes.data.services || []);
        setTotalPages(sRes.data.pagination?.totalPages || 1);
      }
      if (cRes.data) setCategories(Array.isArray(cRes.data) ? cRes.data : cRes.data.categories || []);
    } catch {} finally { setLoading(false); }
  };

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setErrors({});
    setModalOpen(true);
  };

  const openEdit = async (service: Service) => {
    setEditing(service.id);
    setErrors({});
    setForm({
      name: service.name || '',
      slug: service.slug || '',
      categoryId: service.category?.id || '',
      shortDescription: service.shortDescription || '',
      longDescription: '',
      deliveryTime: service.deliveryTime || '',
      processingTime: service.processingTime || '',
      sortOrder: service.sortOrder || 0,
      isFeatured: service.isFeatured || false,
      showOnHomepage: service.showOnHomepage !== false,
      price: service.pricing?.currentPrice || 0,
      seoTitle: '',
      seoDescription: '',
    });
    setModalOpen(true);
  };

  const validate = () => {
    const errs: Record<string, string> = {};
    if (!form.name.trim()) errs.name = 'Required';
    if (!form.slug.trim()) errs.slug = 'Required';
    if (!form.categoryId) errs.categoryId = 'Required';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    try {
      if (editing) {
        await apiPut(`/admin/services/${editing}`, form);
        toast.success('Updated');
      } else {
        await apiPost('/admin/services', form);
        toast.success('Created');
      }
      setModalOpen(false);
      fetchData();
    } catch (err: any) {
      toast.error(err.message || 'Failed');
    } finally { setSaving(false); }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiDelete(`/admin/services/${id}`);
      toast.success('Deleted');
      setDeleteConfirm(null);
      fetchData();
    } catch (err: any) { toast.error(err.message || 'Failed'); }
  };

  const toggleStatus = async (service: Service) => {
    try {
      await apiPut(`/admin/services/${service.id}/status`, {});
      toast.success(service.status === 'ACTIVE' ? 'Disabled' : 'Enabled');
      fetchData();
    } catch (err: any) { toast.error(err.message || 'Failed'); }
  };

  const columns: Column<Service>[] = [
    {
      key: 'name', label: 'Service',
      render: (s) => (
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-900 dark:text-white">{s.name}</span>
          {s.isFeatured && <Star className="w-3 h-3 text-amber-500 fill-amber-500" />}
        </div>
      ),
    },
    { key: 'category', label: 'Category', render: (s) => s.category?.name || '—' },
    { key: 'pricing', label: 'Price', render: (s) => s.pricing ? `₹${(s.pricing.currentPrice || 0).toLocaleString('en-IN')}` : '—' },
    {
      key: 'status', label: 'Status',
      render: (s) => (
        <button onClick={(e) => { e.stopPropagation(); toggleStatus(s); }}
          className={`relative w-9 h-5 rounded-full transition-colors ${s.status === 'ACTIVE' ? 'bg-green-500' : 'bg-slate-300 dark:bg-slate-600'}`}>
          <span className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${s.status === 'ACTIVE' ? 'translate-x-4' : ''}`} />
        </button>
      ),
    },
    { key: 'sortOrder', label: 'Order', render: (s) => s.sortOrder },
    {
      key: 'actions', label: '',
      render: (s) => (
        <div className="flex items-center gap-1">
          <button onClick={(e) => { e.stopPropagation(); openEdit(s); }} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button>
          <button onClick={(e) => { e.stopPropagation(); setDeleteConfirm(s.id); }} className="btn-ghost btn-sm p-1.5 text-red-500 hover:text-red-700"><Trash2 className="w-3.5 h-3.5" /></button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout title="Services">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500 dark:text-slate-400">Manage legal services — changes appear instantly on the website</p>
        <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4" /> Add Service</button>
      </div>
      <DataTable columns={columns} data={services} loading={loading} page={page} totalPages={totalPages} onPageChange={setPage}
        keyExtractor={(s) => s.id} onRowClick={openEdit}
        emptyMessage="No services yet" emptyDescription="Create your first legal service to get started." />
      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Service' : 'Add Service'} size="xl"
        footer={<>
          <button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button>
          <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save'}</button>
        </>}>
        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} error={errors.name} />
            <FormField label="Slug" value={form.slug} onChange={e => setForm({...form, slug: e.target.value})} error={errors.slug} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <FormField type="select" label="Category" value={form.categoryId} error={errors.categoryId}
              onChange={e => setForm({...form, categoryId: e.target.value})}
              options={[{value:'',label:'Select...'}, ...categories.map(c => ({value:c.id, label:c.name}))]} />
            <FormField label="Price (₹)" type="number" value={form.price} onChange={e => setForm({...form, price: parseFloat(e.target.value)||0})} />
          </div>
          <FormField label="Short Description" type="textarea" value={form.shortDescription} onChange={e => setForm({...form, shortDescription: e.target.value})} />
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Delivery Time" value={form.deliveryTime} onChange={e => setForm({...form, deliveryTime: e.target.value})} />
            <FormField label="Processing Time" value={form.processingTime} onChange={e => setForm({...form, processingTime: e.target.value})} />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <FormField label="Sort Order" type="number" value={form.sortOrder} onChange={e => setForm({...form, sortOrder: parseInt(e.target.value)||0})} />
            <FormField label="Featured" type="toggle" checked={form.isFeatured} onChange={v => setForm({...form, isFeatured: v})} />
            <FormField label="Show on Homepage" type="toggle" checked={form.showOnHomepage} onChange={v => setForm({...form, showOnHomepage: v})} />
          </div>
        </form>
      </Modal>
      <Modal open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)} title="Delete Service" size="sm"
        footer={<>
          <button onClick={() => setDeleteConfirm(null)} className="btn-secondary">Cancel</button>
          <button onClick={() => deleteConfirm && handleDelete(deleteConfirm)} className="btn-danger">Delete</button>
        </>}>
        <p className="text-sm text-slate-600">Are you sure you want to delete this service? This cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
