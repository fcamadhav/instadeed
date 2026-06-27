'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Eye, EyeOff } from 'lucide-react';

interface Category {
  _id: string;
  name: string;
  slug: string;
  icon: string;
  displayOrder: number;
  showOnHomepage: boolean;
  status: boolean;
}

const emptyForm = { name: '', slug: '', icon: '', displayOrder: 0, showOnHomepage: false, status: true };

export default function CategoriesPage() {
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
      const res = await apiGet<{ data: { categories: Category[]; page: number; totalPages: number; total: number } }>(`/admin/categories?page=${page}&limit=10`);
      if (res.data) {
        setCategories(res.data.categories || []);
        setTotalPages(res.data.totalPages || 1);
        setTotal(res.data.total || 0);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setErrors({});
    setModalOpen(true);
  };

  const openEdit = (cat: Category) => {
    setEditing(cat._id);
    setForm({ name: cat.name, slug: cat.slug, icon: cat.icon, displayOrder: cat.displayOrder, showOnHomepage: cat.showOnHomepage, status: cat.status });
    setErrors({});
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
        await apiPut(`/admin/categories/${editing}`, form);
        toast.success('Category updated');
      } else {
        await apiPost('/admin/categories', form);
        toast.success('Category created');
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
      await apiDelete(`/admin/categories/${id}`);
      toast.success('Category deleted');
      setDeleteConfirm(null);
      fetchData();
    } catch (err: any) {
      toast.error(err.message);
    }
  };

  const columns: Column<Category>[] = [
    { key: 'name', label: 'Name', sortable: true, render: (c) => <span className="font-medium text-slate-900 dark:text-white">{c.name}</span> },
    { key: 'slug', label: 'Slug', render: (c) => <code className="text-xs text-slate-500 dark:text-slate-400">{c.slug}</code> },
    { key: 'icon', label: 'Icon', render: (c) => c.icon || '—' },
    { key: 'displayOrder', label: 'Display Order', sortable: true },
    {
      key: 'showOnHomepage', label: 'Homepage',
      render: (c) => c.showOnHomepage ? <span className="badge-green">Visible</span> : <span className="badge-slate">Hidden</span>,
    },
    {
      key: 'status', label: 'Status',
      render: (c) => c.status ? <span className="badge-green">Active</span> : <span className="badge-red">Inactive</span>,
    },
    {
      key: 'actions', label: '',
      render: (c) => (
        <div className="flex items-center gap-1">
          <button onClick={(e) => { e.stopPropagation(); openEdit(c); }} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button>
          <button onClick={(e) => { e.stopPropagation(); setDeleteConfirm(c._id); }} className="btn-ghost btn-sm p-1.5 text-red-500 hover:text-red-700"><Trash2 className="w-3.5 h-3.5" /></button>
        </div>
      ),
    },
  ];

  return (
    <AdminLayout title="Categories">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500 dark:text-slate-400">Organize services into categories</p>
        <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4" /> Add Category</button>
      </div>

      <DataTable columns={columns} data={categories} loading={loading} error={error} onRetry={fetchData} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(c) => c._id} emptyMessage="No categories yet" emptyDescription="Create categories to organize your services." />

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Category' : 'Add Category'} size="md" footer={<><button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Name" required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} error={errors.name} />
            <FormField label="Slug" required value={form.slug} onChange={e => setForm({ ...form, slug: e.target.value })} error={errors.slug} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField label="Icon (emoji/icon name)" value={form.icon} onChange={e => setForm({ ...form, icon: e.target.value })} helperText="e.g., gavel, file-text" />
            <FormField label="Display Order" type="number" value={form.displayOrder} onChange={e => setForm({ ...form, displayOrder: parseInt(e.target.value) || 0 })} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Show on Homepage" type="toggle" checked={form.showOnHomepage} onChange={v => setForm({ ...form, showOnHomepage: v })} />
            <FormField label="Active" type="toggle" checked={form.status} onChange={v => setForm({ ...form, status: v })} />
          </div>
        </form>
      </Modal>

      <Modal open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)} title="Delete Category" size="sm" footer={<><button onClick={() => setDeleteConfirm(null)} className="btn-secondary">Cancel</button><button onClick={() => deleteConfirm && handleDelete(deleteConfirm)} className="btn-danger">Delete</button></>}>
        <p className="text-sm text-slate-600 dark:text-slate-400">Are you sure? This cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
