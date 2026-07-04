'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2 } from 'lucide-react';

interface Category {
  id: string;
  name: string;
  slug: string;
  icon: string | null;
  displayOrder: number;
  showOnHomepage: boolean;
  isActive: boolean;
}

const emptyForm = { name: '', slug: '', icon: '', displayOrder: 0, showOnHomepage: true, isActive: true };

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  useEffect(() => { fetchData(); }, [page]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { categories: Category[]; pagination: { totalPages: number } } }>(`/admin/categories?page=${page}&limit=10`);
      if (res.data) {
        setCategories(res.data.categories || []);
        setTotalPages(res.data.pagination?.totalPages || 1);
      }
    } catch (err: any) { setError(err.message || 'Failed to load categories'); } finally { setLoading(false); }
  };

  const openCreate = () => { setEditing(null); setForm(emptyForm); setErrors({}); setModalOpen(true); };
  const openEdit = (c: Category) => {
    setEditing(c.id);
    setForm({ name: c.name, slug: c.slug, icon: c.icon || '', displayOrder: c.displayOrder, showOnHomepage: c.showOnHomepage, isActive: c.isActive });
    setErrors({}); setModalOpen(true);
  };

  const validate = () => {
    const e: Record<string,string> = {};
    if(!form.name.trim()) e.name='Required';
    if(!form.slug.trim()) e.slug='Required';
    setErrors(e); return Object.keys(e).length===0;
  };

  const handleSave = async (ev: FormEvent) => {
    ev.preventDefault(); if(!validate()) return;
    setSaving(true);
    try {
      if(editing){ await apiPut(`/admin/categories/${editing}`, form); toast.success('Updated'); }
      else { await apiPost('/admin/categories', form); toast.success('Created'); }
      setModalOpen(false); fetchData();
    } catch(e:any){ toast.error(e.message||'Failed'); }
    finally { setSaving(false); }
  };

  const handleDelete = async (id: string) => {
    try { await apiDelete(`/admin/categories/${id}`); toast.success('Deleted'); setDeleteConfirm(null); fetchData(); }
    catch(e:any){ toast.error(e.message||'Failed'); }
  };

  const columns: Column<Category>[] = [
    { key:'name', label:'Name', render:(c)=><span className="font-medium">{c.name}</span> },
    { key:'slug', label:'Slug', render:(c)=><code className="text-xs text-slate-500">{c.slug}</code> },
    { key:'icon', label:'Icon', render:(c)=>c.icon||'—' },
    { key:'displayOrder', label:'Order' },
    { key:'isActive', label:'Status', render:(c)=>c.isActive?<span className="badge-green">Active</span>:<span className="badge-slate">Inactive</span> },
    { key:'actions', label:'', render:(c)=>(<div className="flex gap-1">
      <button onClick={e=>{e.stopPropagation();openEdit(c)}} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5"/></button>
      <button onClick={e=>{e.stopPropagation();setDeleteConfirm(c.id)}} className="btn-ghost btn-sm p-1.5 text-red-500"><Trash2 className="w-3.5 h-3.5"/></button>
    </div>) },
  ];

  return (
    <AdminLayout title="Categories">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500">Organize services into categories</p>
        <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4"/> Add Category</button>
      </div>
      <DataTable columns={columns} data={categories} loading={loading} error={error} onRetry={fetchData} page={page} totalPages={totalPages} onPageChange={setPage}
        keyExtractor={c=>c.id} onRowClick={openEdit} emptyMessage="No categories yet" />
      <Modal open={modalOpen} onClose={()=>setModalOpen(false)} title={editing?'Edit':'Add Category'} size="md"
        footer={<><button onClick={()=>setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving?'Saving...':'Save'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} error={errors.name}/>
            <FormField label="Slug" value={form.slug} onChange={e=>setForm({...form,slug:e.target.value})} error={errors.slug}/>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Icon" value={form.icon} onChange={e=>setForm({...form,icon:e.target.value})} helperText="e.g., gavel, shield"/>
            <FormField label="Display Order" type="number" value={form.displayOrder} onChange={e=>setForm({...form,displayOrder:parseInt(e.target.value)||0})}/>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Show on Homepage" type="toggle" checked={form.showOnHomepage} onChange={v=>setForm({...form,showOnHomepage:v})}/>
            <FormField label="Active" type="toggle" checked={form.isActive} onChange={v=>setForm({...form,isActive:v})}/>
          </div>
        </form>
      </Modal>
      <Modal open={!!deleteConfirm} onClose={()=>setDeleteConfirm(null)} title="Delete" size="sm"
        footer={<><button onClick={()=>setDeleteConfirm(null)} className="btn-secondary">Cancel</button><button onClick={()=>deleteConfirm&&handleDelete(deleteConfirm)} className="btn-danger">Delete</button></>}>
        <p className="text-sm">Delete this category? Cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
