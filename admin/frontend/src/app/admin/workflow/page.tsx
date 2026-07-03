'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { GitBranch, Plus, Edit2, Trash2, Loader2 } from 'lucide-react';

interface WorkflowStep {
  name: string;
  type: 'payment' | 'ocr' | 'ai' | 'pdf' | 'email' | 'whatsapp' | 'webhook';
  config: string;
}

interface Workflow {
  id: string;
  name: string;
  description: string;
  active: boolean;
  steps: WorkflowStep[];
}

const stepTypes = [
  { value: 'payment', label: 'Payment', icon: '💳' },
  { value: 'ocr', label: 'OCR', icon: '📄' },
  { value: 'ai', label: 'AI Processing', icon: '🤖' },
  { value: 'pdf', label: 'PDF Generation', icon: '📑' },
  { value: 'email', label: 'Email', icon: '📧' },
  { value: 'whatsapp', label: 'WhatsApp', icon: '💬' },
  { value: 'webhook', label: 'Webhook', icon: '🔗' },
];

export default function WorkflowPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState({ name: '', description: '', active: true, steps: [] as WorkflowStep[] });
  const [saving, setSaving] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);

  useEffect(() => { fetchWorkflows(); }, []);

  const fetchWorkflows = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { workflows: Workflow[] } }>('/admin/workflows');
      setWorkflows(res.data?.workflows || []);
    } catch {} finally { setLoading(false); }
  };

  const openCreate = () => { setEditing(null); setForm({ name: '', description: '', active: true, steps: [] }); setModalOpen(true); };

  const openEdit = (w: Workflow) => {
    setEditing(w.id);
    setForm({ name: w.name, description: w.description || '', active: w.active, steps: w.steps || [] });
    setModalOpen(true);
  };

  const addStep = () => {
    setForm({ ...form, steps: [...form.steps, { name: '', type: 'payment', config: '{}' }] });
  };

  const removeStep = (idx: number) => {
    setForm({ ...form, steps: form.steps.filter((_, i) => i !== idx) });
  };

  const updateStep = (idx: number, field: keyof WorkflowStep, value: any) => {
    const steps = [...form.steps];
    (steps[idx] as any)[field] = value;
    setForm({ ...form, steps });
  };

  const moveStep = (idx: number, direction: -1 | 1) => {
    const newIdx = idx + direction;
    if (newIdx < 0 || newIdx >= form.steps.length) return;
    const steps = [...form.steps];
    [steps[idx], steps[newIdx]] = [steps[newIdx], steps[idx]];
    setForm({ ...form, steps });
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.name.trim()) { toast.error('Name is required'); return; }
    setSaving(true);
    try {
      if (editing) { await apiPut(`/admin/workflows/${editing}`, form); toast.success('Workflow updated'); }
      else { await apiPost('/admin/workflows', form); toast.success('Workflow created'); }
      setModalOpen(false);
      fetchWorkflows();
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const handleDelete = async (id: string) => {
    try { await apiDelete(`/admin/workflows/${id}`); toast.success('Workflow deleted'); setDeleteConfirm(null); fetchWorkflows(); } catch (err: any) { toast.error(err.message); }
  };

  const typeIcon = (type: string) => {
    const map: Record<string, string> = { payment: '💳', ocr: '📄', ai: '🤖', pdf: '📑', email: '📧', whatsapp: '💬', webhook: '🔗' };
    return map[type] || '⚙️';
  };

  return (
    <AdminLayout title="Workflow">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-slate-500 dark:text-slate-400">Design order processing workflows</p>
        <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4" /> Create Workflow</button>
      </div>

      {loading ? (
        <div className="space-y-3">{Array.from({ length: 3 }).map((_, i) => <div key={i} className="card p-5"><div className="skeleton h-5 w-40 mb-3" /><div className="skeleton h-3 w-64" /></div>)}</div>
      ) : workflows.length === 0 ? (
        <div className="card p-8 text-center">
          <GitBranch className="w-10 h-10 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-900 dark:text-white">No workflows</p>
          <p className="text-sm text-slate-500 dark:text-slate-400">Create your first workflow to automate order processing.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {workflows.map(w => (
            <div key={w.id} className="card p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-slate-900 dark:text-white">{w.name}</h3>
                    {w.active ? <span className="badge-green">Active</span> : <span className="badge-slate">Inactive</span>}
                  </div>
                  {w.description && <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">{w.description}</p>}
                </div>
                <div className="flex items-center gap-1">
                  <button onClick={() => openEdit(w)} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button>
                  <button onClick={() => setDeleteConfirm(w.id)} className="btn-ghost btn-sm p-1.5 text-red-500"><Trash2 className="w-3.5 h-3.5" /></button>
                </div>
              </div>

              <div className="flex items-center gap-1 flex-wrap">
                {w.steps.map((step, i) => (
                  <div key={i} className="flex items-center">
                    <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-admin-50 dark:bg-admin-900/30 text-sm text-admin-700 dark:text-admin-300">
                      <span>{typeIcon(step.type)}</span>
                      <span className="text-xs font-medium">{step.name || step.type}</span>
                    </div>
                    {i < w.steps.length - 1 && <div className="w-4 h-0.5 bg-slate-300 dark:bg-slate-600" />}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Workflow' : 'Create Workflow'} size="xl" footer={<><button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <FormField label="Workflow Name" required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          <FormField label="Description" type="textarea" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
          <FormField label="Active" type="toggle" checked={form.active} onChange={v => setForm({ ...form, active: v })} />

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="label mb-0">Steps</label>
              <button type="button" onClick={addStep} className="btn-secondary btn-sm"><Plus className="w-3 h-3" /> Add Step</button>
            </div>
            {form.steps.length === 0 ? (
              <p className="text-sm text-slate-400 py-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-lg">No steps added yet</p>
            ) : (
              <div className="space-y-2">
                {form.steps.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-2 p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg">
                    <div className="flex flex-col gap-0.5 pt-1">
                      <button type="button" onClick={() => moveStep(idx, -1)} disabled={idx === 0} className="text-slate-400 hover:text-slate-600 disabled:opacity-30"><svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" /></svg></button>
                      <button type="button" onClick={() => moveStep(idx, 1)} disabled={idx === form.steps.length - 1} className="text-slate-400 hover:text-slate-600 disabled:opacity-30"><svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg></button>
                    </div>
                    <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-2">
                      <FormField label="Step Name" value={step.name} onChange={e => updateStep(idx, 'name', e.target.value)} placeholder="Step name" />
                      <FormField type="select" label="Type" value={step.type} onChange={e => updateStep(idx, 'type', e.target.value)} options={stepTypes} />
                      <FormField label="Config (JSON)" value={step.config} onChange={e => updateStep(idx, 'config', e.target.value)} placeholder='{"key": "value"}' />
                    </div>
                    <button type="button" onClick={() => removeStep(idx)} className="text-red-400 hover:text-red-600 pt-5"><Trash2 className="w-4 h-4" /></button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </form>
      </Modal>

      <Modal open={!!deleteConfirm} onClose={() => setDeleteConfirm(null)} title="Delete Workflow" size="sm" footer={<><button onClick={() => setDeleteConfirm(null)} className="btn-secondary">Cancel</button><button onClick={() => deleteConfirm && handleDelete(deleteConfirm)} className="btn-danger">Delete</button></>}>
        <p className="text-sm text-slate-600 dark:text-slate-400">Are you sure? This cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
