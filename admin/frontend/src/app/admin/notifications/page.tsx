'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Mail, MessageSquare, Send, Edit2, FileText, Loader2, Plus } from 'lucide-react';

interface EmailTemplate {
  id: string;
  name: string;
  subject: string;
  body: string;
  variables: string[];
}

interface WhatsAppTemplate {
  id: string;
  name: string;
  templateId: string;
  body: string;
  variables: string[];
}

export default function NotificationsPage() {
  const [tab, setTab] = useState<'email' | 'whatsapp' | 'log'>('email');
  const [emailTemplates, setEmailTemplates] = useState<EmailTemplate[]>([]);
  const [whatsappTemplates, setWhatsappTemplates] = useState<WhatsAppTemplate[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string | null>(null);
  const [form, setForm] = useState({ name: '', subject: '', body: '', variables: '', templateId: '' });
  const [saving, setSaving] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => { fetchData(); }, [tab, page]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (tab === 'email') {
        const res = await apiGet<{ data: { templates: EmailTemplate[]; page: number; totalPages: number } }>(`/admin/notifications/email-templates?page=${page}&limit=10`);
        setEmailTemplates(res.data?.templates || []);
        setTotalPages(res.data?.totalPages || 1);
      } else if (tab === 'whatsapp') {
        const res = await apiGet<{ data: { templates: WhatsAppTemplate[]; page: number; totalPages: number } }>(`/admin/notifications/whatsapp-templates?page=${page}&limit=10`);
        setWhatsappTemplates(res.data?.templates || []);
        setTotalPages(res.data?.totalPages || 1);
      } else {
        const res = await apiGet<{ data: { logs: any[]; page: number; totalPages: number } }>(`/admin/notifications/logs?page=${page}&limit=10`);
        setLogs(res.data?.logs || []);
        setTotalPages(res.data?.totalPages || 1);
      }
    } catch {} finally { setLoading(false); }
  };

  const openCreate = () => {
    setEditing(null);
    setForm({ name: '', subject: '', body: '', variables: '', templateId: '' });
    setModalOpen(true);
  };

  const openEdit = (t: any) => {
    setEditing(t.id);
    setForm({
      name: t.name || '',
      subject: t.subject || '',
      body: t.body || '',
      variables: (t.variables || []).join(', '),
      templateId: t.templateId || '',
    });
    setModalOpen(true);
  };

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    const payload = {
      ...form,
      variables: form.variables.split(',').map(v => v.trim()).filter(Boolean),
    };
    try {
      const endpoint = tab === 'email' ? '/admin/notifications/email-templates' : '/admin/notifications/whatsapp-templates';
      if (editing) { await apiPut(`${endpoint}/${editing}`, payload); toast.success('Template updated'); }
      else { await apiPost(endpoint, payload); toast.success('Template created'); }
      setModalOpen(false);
      fetchData();
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const emailColumns: Column<EmailTemplate>[] = [
    { key: 'name', label: 'Name', sortable: true, render: (t) => <span className="font-medium text-slate-900 dark:text-white">{t.name}</span> },
    { key: 'subject', label: 'Subject', render: (t) => t.subject },
    { key: 'variables', label: 'Variables', render: (t) => (t.variables || []).map(v => <span key={v} className="badge-blue mr-1 text-[10px]">{`{{${v}}}`}</span>) },
    { key: 'actions', label: '', render: (t) => <button onClick={(e) => { e.stopPropagation(); openEdit(t); }} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button> },
  ];

  const whatsappColumns: Column<WhatsAppTemplate>[] = [
    { key: 'name', label: 'Name', render: (t) => <span className="font-medium text-slate-900 dark:text-white">{t.name}</span> },
    { key: 'templateId', label: 'Template ID' },
    { key: 'variables', label: 'Variables', render: (t) => (t.variables || []).map(v => <span key={v} className="badge-blue mr-1 text-[10px]">{`{{${v}}}`}</span>) },
    { key: 'actions', label: '', render: (t) => <button onClick={(e) => { e.stopPropagation(); openEdit(t); }} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3.5 h-3.5" /></button> },
  ];

  return (
    <AdminLayout title="Notifications">
      <div className="flex items-center justify-between mb-4">
        <div className="flex gap-1 bg-slate-100 dark:bg-slate-700 rounded-lg p-1">
          {([
            { key: 'email' as const, label: 'Email Templates', icon: Mail },
            { key: 'whatsapp' as const, label: 'WhatsApp Templates', icon: MessageSquare },
            { key: 'log' as const, label: 'Notification Log', icon: FileText },
          ]).map(t => (
            <button key={t.key} onClick={() => { setTab(t.key); setPage(1); }} className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${tab === t.key ? 'bg-white dark:bg-slate-800 shadow-sm text-admin-600 dark:text-admin-400 font-medium' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'}`}>
              <t.icon className="w-3.5 h-3.5" /> {t.label}
            </button>
          ))}
        </div>
        {tab !== 'log' && (
          <button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4" /> Add Template</button>
        )}
      </div>

      {tab === 'email' && (
        <DataTable columns={emailColumns} data={emailTemplates} loading={loading} page={page} totalPages={totalPages} onPageChange={setPage} keyExtractor={(t) => t.id} emptyMessage="No email templates" emptyDescription="Create email notification templates." />
      )}
      {tab === 'whatsapp' && (
        <DataTable columns={whatsappColumns} data={whatsappTemplates} loading={loading} page={page} totalPages={totalPages} onPageChange={setPage} keyExtractor={(t) => t.id} emptyMessage="No WhatsApp templates" emptyDescription="Create WhatsApp notification templates." />
      )}
      {tab === 'log' && (
        <div className="card p-6 text-center text-sm text-slate-500 dark:text-slate-400">
          <Send className="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
          Notification logs will appear here.
        </div>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Template' : 'Add Template'} size="lg" footer={<><button onClick={() => setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : editing ? 'Update' : 'Create'}</button></>}>
        <form onSubmit={handleSave} className="space-y-4">
          <FormField label="Template Name" required value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          {tab === 'email' && <FormField label="Subject" required value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })} />}
          {tab === 'whatsapp' && <FormField label="Template ID" value={form.templateId} onChange={e => setForm({ ...form, templateId: e.target.value })} />}
          <FormField label="Body" type="textarea" required value={form.body} onChange={e => setForm({ ...form, body: e.target.value })} rows={6} helperText="Use {{variable}} for dynamic content" />
          <FormField label="Variables" value={form.variables} onChange={e => setForm({ ...form, variables: e.target.value })} helperText="Comma-separated variable names (e.g., name, orderId, amount)" />
        </form>
      </Modal>
    </AdminLayout>
  );
}
