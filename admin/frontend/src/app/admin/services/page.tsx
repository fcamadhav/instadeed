'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete, apiUpload } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Eye, EyeOff, Star } from 'lucide-react';

interface Service {
  _id: string;
  name: string;
  slug: string;
  category: { _id: string; name: string } | null;
  price: number;
  status: boolean;
  featured: boolean;
  sortOrder: number;
  shortDescription?: string;
  deliveryTime?: string;
  processingTime?: string;
}

interface Category {
  _id: string;
  name: string;
}

interface FormData {
  name: string;
  slug: string;
  category: string;
  shortDescription: string;
  longDescription: string;
  deliveryTime: string;
  processingTime: string;
  sortOrder: number;
  featured: boolean;
  showOnHomepage: boolean;
  price: number;
  metaTitle: string;
  metaDescription: string;
  metaKeywords: string;
}

const emptyForm: FormData = {
  name: '', slug: '', category: '', shortDescription: '', longDescription: '',
  deliveryTime: '', processingTime: '', sortOrder: 0, featured: false,
  showOnHomepage: false, price: 0, metaTitle: '', metaDescription: '', metaKeywords: '',
};

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [saving, setSaving] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [iconFile, setIconFile] = useState<File | null>(null);
  const [bannerFile, setBannerFile] = useState<File | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => { fetchData(); }, [page]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sRes, cRes] = await Promise.all([
        apiGet<{ data: { services: Service[]; page: number; totalPages: number; total: number } }>(`/admin/services?page=${page}&limit=10`),
        apiGet<{ data: { categories: Category[] } }>('/admin/categories?limit=100'),
      ]);
      if (sRes.data) {
        setServices(sRes.data.services || []);
        setTotalPages(sRes.data.totalPages || 1);
        setTotal(sRes.data.total || 0);
      }
      if (cRes.data) setCategories(cRes.data.categories || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setIconFile(null);
    setBannerFile(null);
    setErrors({});
    setModalOpen(true);
  };

  const openEdit = async (service: Service) => {
    setEditing(service._id);
    setErrors({});
    setIconFile(null);
    setBannerFile(null);
    try {
      const res = await apiGet<{ data: { service: any } }>(`/admin/services/${service._id}`);
      const s = res.data.service;
      setForm({
        name: s.name || '',
        slug: s.slug || '',
        category: s.category?._id || '',
        shortDescription: s.shortDescription || '',
        longDescription: s.longDescription || '',
        deliveryTime: s.deliveryTime || '',
        processingTime: s.processingTime || '',
        sortOrder: s.sortOrder || 0,
        featured: s.featured || false,
        showOnHomepage: s.showOnHomepage || false,
        price: s.price || 0,
        metaTitle: s.metaTitle || '',
        metaDescription: s.metaDescription || '',
        metaKeywords: s.metaKeywords || '',
      });
    } catch (err: any) {
      toast.error('Failed to load service details');
    }
    setModalOpen(true);
  };

  const validate = () => {
    const errs: Record<string, string> = {};
    if (!form.name.trim()) errs.name = 'Name is required';
    if (!form.slug.trim()) errs.slug = 'Slug is required';
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
        toast.success('Service updated');
      } else {
        await apiPost('/admin/services', form);
        toast.success('Service created');
      }
      setModalOpen(false);
      fetchData();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiDelete(`/admin/services/${id}`);
      toast.success('Service deleted');
      setDeleteConfirm(null);
      fetchData();
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  const toggleStatus = async (service: Service) => {
    try {
      await apiPut(`/admin/services/${service._id}`, { status: !service.status });
      toast.success(`Service ${service.status ? 'deactivated' : 'activated'}`);
      fetchData();
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  const columns: Column<Service>[] = [
    {
      key: 'name', label: 'Service', sortable: true,
      render: (s) => (
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-900 dark:text-white">{s.name}</span>
          {s.featured && <Star className="w-3 h-3 text-amber-500 fill-amber-500" />}
        </div>
      ),
    },
    {
      key: 'category', label: 'Category',
      render: (s) => s.category?.name || '—',
    },
    {
      key: 'price', label: 'Price', sortable: true,
      render: (s) => `₹${(s.price || 0).toLocaleString('en-IN')}`,
    },
    {
      key: 'status', label: 'Status',
      render: (s) => (
        <button
          onClick={(e) => { e.stopPropagation(); toggleStatus(s); }}
          className={`relative w-9 h-5 rounded-full transition-colors ${
            s.status ? 'bg-green-500' : 'bg-slate-300 dark:bg-slate-600'
          }`}
        >
          <span className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${
            s.status ? 'translate-x-4' : ''
          }`} />
        </button>
      ),
    },
    {
      key: 'sortOrder', label: 'Order', sortable: true,
      render: (s) => s.sortOrder,
    },
    {
      key: 'actions', label: '',
      render: (s) => (
        <div className="flex items-center gap-1">
          <button onClick={(e) => { e.stopPropagation(); openEdit(s); }} className="btn-ghost btn-sm p-1.5">
            <Edit2 className="w-3.5 h-3.5" />
          </button>
          <button onClick={(e) => { e.stopPropagation(); setDeleteConfirm(s._id); }} className="btn-ghost btn-sm p-1.5 text-red-500 hover:text-red-700">
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout title="Services">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500 dark:text-slate-400">Manage legal services</p>
        <button onClick={openCreate} className="btn-primary btn-sm">
          <Plus className="w-4 h-4" /> Add Service
        </button>
      </div>

      <DataTable
        columns={columns}
        data={services}
        loading={loading}
        error={error}
        onRetry={fetchData}
        page={page}
        totalPages={totalPages}
        total={total}
        onPageChange={setPage}
        keyExtractor={(s) => s._id}
        emptyMessage="No services yet"
        emptyDescription="Create your first legal service to get started."
      />

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? 'Edit Service' : 'Add Service'}
        size="xl"
        footer={
          <>
            <button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button>
            <button onClick={handleSave} disabled={saving} className="btn-primary">
              {saving ? 'Saving...' : editing ? 'Update Service' : 'Create Service'}
            </button>
          </>
        }
      >
        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Service Name" required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} error={errors.name} />
            <FormField label="Slug" required value={form.slug} onChange={e => setForm({ ...form, slug: e.target.value })} error={errors.slug} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="select" label="Category"
              value={form.category}
              onChange={e => setForm({ ...form, category: e.target.value })}
              options={[
                { value: '', label: 'Select category' },
                ...categories.map(c => ({ value: c._id, label: c.name })),
              ]}
            />
            <FormField label="Price (₹)" type="number" value={form.price} onChange={e => setForm({ ...form, price: parseFloat(e.target.value) || 0 })} />
          </div>
          <FormField label="Short Description" type="textarea" value={form.shortDescription} onChange={e => setForm({ ...form, shortDescription: e.target.value })} />
          <FormField label="Long Description" type="textarea" value={form.longDescription} onChange={e => setForm({ ...form, longDescription: e.target.value })} rows={5} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Delivery Time" value={form.deliveryTime} onChange={e => setForm({ ...form, deliveryTime: e.target.value })} placeholder="e.g., 24 hours" />
            <FormField label="Processing Time" value={form.processingTime} onChange={e => setForm({ ...form, processingTime: e.target.value })} placeholder="e.g., 2-3 business days" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormField label="Sort Order" type="number" value={form.sortOrder} onChange={e => setForm({ ...form, sortOrder: parseInt(e.target.value) || 0 })} />
            <FormField label="Featured" type="toggle" checked={form.featured} onChange={v => setForm({ ...form, featured: v })} />
            <FormField label="Show on Homepage" type="toggle" checked={form.showOnHomepage} onChange={v => setForm({ ...form, showOnHomepage: v })} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Icon" type="file" onChange={e => setIconFile((e.target as HTMLInputElement).files?.[0] || null)} helperText="Upload icon image" />
            <FormField label="Banner" type="file" onChange={e => setBannerFile((e.target as HTMLInputElement).files?.[0] || null)} helperText="Upload banner image" />
          </div>
          <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
            <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">SEO Settings</h4>
            <div className="space-y-3">
              <FormField label="Meta Title" value={form.metaTitle} onChange={e => setForm({ ...form, metaTitle: e.target.value })} />
              <FormField label="Meta Description" type="textarea" value={form.metaDescription} onChange={e => setForm({ ...form, metaDescription: e.target.value })} />
              <FormField label="Meta Keywords" value={form.metaKeywords} onChange={e => setForm({ ...form, metaKeywords: e.target.value })} placeholder="keyword1, keyword2" />
            </div>
          </div>
        </form>
      </Modal>

      <Modal
        open={!!deleteConfirm}
        onClose={() => setDeleteConfirm(null)}
        title="Delete Service"
        size="sm"
        footer={
          <>
            <button onClick={() => setDeleteConfirm(null)} className="btn-secondary">Cancel</button>
            <button onClick={() => deleteConfirm && handleDelete(deleteConfirm)} className="btn-danger">Delete</button>
          </>
        }
      >
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Are you sure you want to delete this service? This action cannot be undone.
        </p>
      </Modal>
    </AdminLayout>
  );
}
