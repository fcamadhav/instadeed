'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPut, apiPost } from '@/lib/api';
import toast from 'react-hot-toast';
import {
  Search, Filter, Download, RefreshCw, Loader2, Eye, FileText,
  UserCheck, MessageSquare, Archive, MoreHorizontal, ChevronDown
} from 'lucide-react';

interface DocLifecycle {
  id: string;
  status: string;
  assignedToId: string | null;
  assignedRole: string | null;
  assignedAt: string | null;
  authorityRefNo: string | null;
  createdAt: string;
  updatedAt: string;
  document: {
    id: string;
    documentNumber: string;
    documentType: string;
    status: string;
    pdfFilePath: string | null;
    createdAt: string;
    customer: { id: string; name: string; email: string; phone: string };
    service: { id: string; name: string };
    order: { id: string; orderNumber: string; paymentStatus: string; total: number } | null;
  };
  assignedTo: { id: string; name: string; email: string; role: string } | null;
  versions: { version: number; createdAt: string }[];
  timeline: { event: string; createdAt: string }[];
  _count: { notes: number; versions: number };
}

const STATUS_BADGES: Record<string, string> = {
  DRAFT: 'badge-slate',
  SUBMITTED: 'badge-blue',
  PAYMENT_PENDING: 'badge-yellow',
  PAYMENT_SUCCESS: 'badge-green',
  ASSIGNED: 'badge-blue',
  UNDER_REVIEW: 'badge-yellow',
  READY_FOR_SUBMISSION: 'badge-blue',
  SUBMITTED_TO_AUTHORITY: 'badge-purple',
  COMPLETED: 'badge-green',
  ARCHIVED: 'badge-slate',
};

export default function DocumentsManagementPage() {
  const [documents, setDocuments] = useState<DocLifecycle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [selected, setSelected] = useState<DocLifecycle | null>(null);
  const [detailTab, setDetailTab] = useState<'info' | 'timeline' | 'notes'>('info');
  const [newNote, setNewNote] = useState('');
  const [staffList, setStaffList] = useState<{ id: string; name: string; role: string }[]>([]);
  const [assignModal, setAssignModal] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState('');
  const [selectedRole, setSelectedRole] = useState('EMPLOYEE');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [bulkStatus, setBulkStatus] = useState('');

  useEffect(() => { fetchDocuments(); }, [page, statusFilter]);
  useEffect(() => { if (selected) fetchStaff(); }, [selected]);

  const fetchDocuments = async () => {
    setLoading(true); setError(null);
    try {
      let url = `/admin/documents-management?page=${page}&limit=20`;
      if (statusFilter) url += `&status=${statusFilter}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;
      const res = await apiGet<{ data: { documents: DocLifecycle[]; pagination: any } }>(url);
      setDocuments(res.data?.documents || []);
      setTotalPages(res.data?.pagination?.totalPages || 1);
      setTotal(res.data?.pagination?.total || 0);
    } catch (err: any) { setError(err.message); }
    finally { setLoading(false); }
  };

  const fetchStaff = async () => {
    try {
      const res = await apiGet<{ data: { id: string; name: string; role: string }[] }>('/admin/documents-management-staff');
      setStaffList(res.data || []);
    } catch {}
  };

  const handleSearch = async () => {
    setPage(1);
    fetchDocuments();
  };

  const changeStatus = async (id: string, status: string) => {
    try {
      await apiPut(`/admin/documents-management/${id}/status`, { status });
      toast.success('Status updated');
      fetchDocuments();
      if (selected?.id === id) setSelected(null);
    } catch (err: any) { toast.error(err.message); }
  };

  const handleAssign = async () => {
    if (!selectedStaff || !selected) return;
    try {
      if (selectedIds.length > 0) {
        await apiPut('/admin/documents-management/bulk/assign', { ids: selectedIds, staffId: selectedStaff, role: selectedRole });
        toast.success(`${selectedIds.length} documents assigned`);
        setSelectedIds([]);
      } else {
        await apiPut(`/admin/documents-management/${selected.id}/assign`, { staffId: selectedStaff, role: selectedRole });
        toast.success('Staff assigned');
      }
      setAssignModal(false);
      fetchDocuments();
    } catch (err: any) { toast.error(err.message); }
  };

  const addNote = async () => {
    if (!newNote.trim() || !selected) return;
    try {
      await apiPost(`/admin/documents-management/${selected.id}/notes`, { note: newNote });
      toast.success('Note added');
      setNewNote('');
      // Refresh detail
      const res = await apiGet<any>(`/admin/documents-management/${selected.id}`);
      setSelected(res.data);
    } catch (err: any) { toast.error(err.message); }
  };

  const toggleArchive = async (id: string) => {
    try {
      await apiPut(`/admin/documents-management/${id}/archive`, {});
      toast.success('Document archived/restored');
      fetchDocuments();
    } catch (err: any) { toast.error(err.message); }
  };

  const handleBulkStatus = async () => {
    if (!bulkStatus || selectedIds.length === 0) return;
    try {
      await apiPut('/admin/documents-management/bulk/status', { ids: selectedIds, status: bulkStatus });
      toast.success(`${selectedIds.length} documents updated`);
      setSelectedIds([]);
      setBulkStatus('');
      fetchDocuments();
    } catch (err: any) { toast.error(err.message); }
  };

  const openDetail = async (d: DocLifecycle) => {
    setSelected(d);
    setDetailTab('info');
    try {
      const res = await apiGet<any>(`/admin/documents-management/${d.id}`);
      setSelected(res.data);
    } catch {}
  };

  const columns: Column<DocLifecycle>[] = [
    { key: 'documentNumber', label: 'Doc ID', render: (d) => <span className="font-mono text-xs font-medium">{d.document?.documentNumber || d.id.slice(0, 8)}</span> },
    { key: 'customer', label: 'Customer', render: (d) => <div><div className="text-sm font-medium">{d.document?.customer?.name || '—'}</div><div className="text-xs text-slate-400">{d.document?.customer?.phone || ''}</div></div> },
    { key: 'documentType', label: 'Type', render: (d) => <span className="text-sm">{d.document?.documentType || '—'}</span> },
    { key: 'status', label: 'Status', render: (d) => <span className={`badge ${STATUS_BADGES[d.status] || 'badge-slate'}`}>{d.status.replace(/_/g, ' ')}</span> },
    { key: 'assigned', label: 'Assigned', render: (d) => <span className="text-xs">{d.assignedTo?.name || '—'}</span> },
    { key: 'updatedAt', label: 'Updated', render: (d) => <span className="text-xs text-slate-400">{new Date(d.updatedAt).toLocaleDateString('en-IN')}</span> },
  ];

  const statuses = ['DRAFT', 'SUBMITTED', 'PAYMENT_PENDING', 'PAYMENT_SUCCESS', 'ASSIGNED', 'UNDER_REVIEW', 'READY_FOR_SUBMISSION', 'SUBMITTED_TO_AUTHORITY', 'COMPLETED', 'ARCHIVED'];

  return (
    <AdminLayout title="Document Management">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">All Documents</h1>
          <div className="flex items-center gap-2">
            {selectedIds.length > 0 && (
              <>
                <select value={bulkStatus} onChange={e => setBulkStatus(e.target.value)} className="input py-1.5 text-sm w-auto">
                  <option value="">Bulk Status →</option>
                  {statuses.map(s => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
                </select>
                <button onClick={handleBulkStatus} disabled={!bulkStatus} className="btn-primary btn-sm">Apply</button>
                <button onClick={() => { setAssignModal(true); }} className="btn-secondary btn-sm">Assign</button>
                <span className="text-sm text-slate-500">{selectedIds.length} selected</span>
              </>
            )}
          </div>
        </div>

        {/* Filters */}
        <div className="card p-4">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input value={search} onChange={e => setSearch(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSearch()}
                placeholder="Search by name, mobile, email, doc ID, order ID..." className="input pl-9 py-2 text-sm" />
            </div>
            <select value={statusFilter} onChange={e => { setStatusFilter(e.target.value); setPage(1); }} className="input py-2 text-sm w-auto">
              <option value="">All Statuses</option>
              {statuses.map(s => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
            </select>
            <button onClick={() => { setSearch(''); setStatusFilter(''); setPage(1); }} className="btn-secondary btn-sm">Clear</button>
            <button onClick={fetchDocuments} className="btn-secondary btn-sm p-2"><RefreshCw className="w-4 h-4" /></button>
          </div>
        </div>

        {/* Table */}
        <DataTable
          columns={columns}
          data={documents}
          loading={loading}
          error={error}
          onRetry={fetchDocuments}
          page={page}
          totalPages={totalPages}
          total={total}
          onPageChange={setPage}
          keyExtractor={(d) => d.id}
          onRowClick={openDetail}
          emptyMessage="No documents found"
          emptyDescription="Documents will appear here when customers create them."
        />

        {/* Detail Modal */}
        {selected && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-start justify-center pt-10 pb-10 overflow-y-auto" onClick={() => setSelected(null)}>
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-4xl mx-4 overflow-hidden" onClick={e => e.stopPropagation()}>
              <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-700">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900 dark:text-white">{selected.document?.documentNumber || 'Document'} <span className={`badge ${STATUS_BADGES[selected.status]} ml-2`}>{selected.status.replace(/_/g, ' ')}</span></h2>
                  <p className="text-sm text-slate-500">{selected.document?.customer?.name} • {selected.document?.documentType}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button onClick={() => { setSelected(null); setAssignModal(true); }} className="btn-secondary btn-sm"><UserCheck className="w-3 h-3" /> Assign</button>
                  <button onClick={() => toggleArchive(selected.id)} className="btn-secondary btn-sm"><Archive className="w-3 h-3" /></button>
                  <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-slate-600 p-1"><MoreHorizontal className="w-5 h-5" /></button>
                </div>
              </div>

              {/* Tabs */}
              <div className="flex border-b border-slate-200 dark:border-slate-700">
                {['info', 'timeline', 'notes'].map(tab => (
                  <button key={tab} onClick={() => setDetailTab(tab as any)}
                    className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${detailTab === tab ? 'border-admin-600 text-admin-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}>
                    {tab.charAt(0).toUpperCase() + tab.slice(1)} {tab === 'notes' && selected._count?.notes > 0 && <span className="ml-1 text-xs bg-slate-200 px-1.5 rounded-full">{selected._count.notes}</span>}
                  </button>
                ))}
              </div>

              <div className="p-6 max-h-[60vh] overflow-y-auto">
                {detailTab === 'info' && (
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><span className="text-slate-500">Document ID:</span> <span className="font-medium ml-1">{selected.document?.documentNumber || selected.id}</span></div>
                    <div><span className="text-slate-500">Type:</span> <span className="font-medium ml-1">{selected.document?.documentType}</span></div>
                    <div><span className="text-slate-500">Customer:</span> <span className="font-medium ml-1">{selected.document?.customer?.name}</span></div>
                    <div><span className="text-slate-500">Mobile:</span> <span className="font-medium ml-1">{selected.document?.customer?.phone}</span></div>
                    <div><span className="text-slate-500">Email:</span> <span className="font-medium ml-1">{selected.document?.customer?.email}</span></div>
                    <div><span className="text-slate-500">Service:</span> <span className="font-medium ml-1">{selected.document?.service?.name}</span></div>
                    <div><span className="text-slate-500">Status:</span> <span className={`badge ${STATUS_BADGES[selected.status]} ml-1`}>{selected.status.replace(/_/g, ' ')}</span></div>
                    <div><span className="text-slate-500">Assigned:</span> <span className="font-medium ml-1">{selected.assignedTo?.name || '—'}</span></div>
                    <div><span className="text-slate-500">Created:</span> <span className="font-medium ml-1">{new Date(selected.createdAt).toLocaleString('en-IN')}</span></div>
                    <div><span className="text-slate-500">Updated:</span> <span className="font-medium ml-1">{new Date(selected.updatedAt).toLocaleString('en-IN')}</span></div>
                    {selected.document?.order && (
                      <div className="col-span-2"><span className="text-slate-500">Order:</span> <span className="font-medium ml-1">{selected.document.order.orderNumber} — ₹{selected.document.order.total} — {selected.document.order.paymentStatus}</span></div>
                    )}
                    {/* Change Status */}
                    <div className="col-span-2 pt-4 border-t border-slate-200">
                      <label className="label">Change Status</label>
                      <div className="flex gap-2 mt-1">
                        <select onChange={e => { const v = e.target.value; if (v) changeStatus(selected.id, v); }} className="input py-1.5 text-sm flex-1">
                          <option value="">Select status...</option>
                          {statuses.map(s => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
                        </select>
                        {selected.document?.pdfFilePath && (
                          <a href={`/api/admin/documents/${selected.document.id}/download/pdf`} target="_blank" className="btn-primary btn-sm"><Download className="w-3 h-3" /> PDF</a>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {detailTab === 'timeline' && (
                  <div className="space-y-4">
                    {(selected as any).timeline?.length > 0 ? (selected as any).timeline.map((t: any) => (
                      <div key={t.id} className="flex gap-3">
                        <div className="flex flex-col items-center">
                          <div className="w-3 h-3 rounded-full bg-admin-600 mt-1" />
                          <div className="w-0.5 flex-1 bg-slate-200 dark:bg-slate-700" />
                        </div>
                        <div>
                          <div className="text-sm font-medium text-slate-900 dark:text-white">{t.event.replace(/_/g, ' ')}</div>
                          {t.description && <div className="text-xs text-slate-500">{t.description}</div>}
                          <div className="text-xs text-slate-400">{new Date(t.createdAt).toLocaleString('en-IN')}</div>
                        </div>
                      </div>
                    )) : <p className="text-sm text-slate-500 text-center py-4">No timeline events</p>}
                  </div>
                )}

                {detailTab === 'notes' && (
                  <div>
                    <div className="flex gap-2 mb-4">
                      <input value={newNote} onChange={e => setNewNote(e.target.value)} placeholder="Add internal note..." className="input flex-1 py-2 text-sm" onKeyDown={e => e.key === 'Enter' && addNote()} />
                      <button onClick={addNote} disabled={!newNote.trim()} className="btn-primary btn-sm"><MessageSquare className="w-3 h-3" /> Add</button>
                    </div>
                    {(selected as any).notes?.length > 0 ? (selected as any).notes.map((n: any) => (
                      <div key={n.id} className="p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg mb-2">
                        <div className="text-sm">{n.note}</div>
                        <div className="text-xs text-slate-400 mt-1">{n.createdBy?.name || 'System'} • {new Date(n.createdAt).toLocaleString('en-IN')}</div>
                      </div>
                    )) : <p className="text-sm text-slate-500 text-center py-4">No notes yet</p>}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Assign Modal */}
        <Modal open={assignModal} onClose={() => setAssignModal(false)} title="Assign Staff" size="sm">
          <div className="space-y-4">
            <div>
              <label className="label">Staff Member</label>
              <select value={selectedStaff} onChange={e => setSelectedStaff(e.target.value)} className="input">
                <option value="">Select staff...</option>
                {staffList.map(s => <option key={s.id} value={s.id}>{s.name} ({s.role})</option>)}
              </select>
            </div>
            <FormField label="Role" value={selectedRole} onChange={e => setSelectedRole((e as any).target?.value || 'EMPLOYEE')}
              type="select" options={[
                { value: 'EMPLOYEE', label: 'Employee' },
                { value: 'ADVOCATE', label: 'Advocate' },
                { value: 'CASE_MANAGER', label: 'Case Manager' },
                { value: 'PROPERTY_EXECUTIVE', label: 'Property Executive' },
              ]} />
          </div>
          <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-slate-200">
            <button onClick={() => setAssignModal(false)} className="btn-secondary">Cancel</button>
            <button onClick={handleAssign} disabled={!selectedStaff} className="btn-primary"><UserCheck className="w-4 h-4" /> Assign</button>
          </div>
        </Modal>
      </div>
    </AdminLayout>
  );
}
