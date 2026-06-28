'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import { Search, Filter, ChevronDown, ChevronUp, Loader2, ScrollText } from 'lucide-react';

interface AuditLog {
  _id: string;
  timestamp: string;
  user: string;
  action: string;
  module: string;
  recordId: string;
  ip: string;
  oldValue?: any;
  newValue?: any;
}

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [filters, setFilters] = useState({ module: '', action: '', user: '', startDate: '', endDate: '' });

  useEffect(() => { fetchLogs(); }, [page, filters]);

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ page: String(page), limit: '10' });
      if (filters.module) params.set('module', filters.module);
      if (filters.action) params.set('action', filters.action);
      if (filters.user) params.set('userId', filters.user);
      if (filters.startDate) params.set('dateFrom', filters.startDate);
      if (filters.endDate) params.set('dateTo', filters.endDate);
      const res = await apiGet<{ data: { logs: AuditLog[]; pagination: { page: number; totalPages: number; total: number } } }>(`/admin/audit-logs?${params}`);
      if (res.data) {
        setLogs(res.data.logs || []);
        setTotalPages(res.data.pagination?.totalPages || 1);
        setTotal(res.data.pagination?.total || 0);
      }
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const columns: Column<AuditLog>[] = [
    { key: 'timestamp', label: 'Timestamp', sortable: true, render: (l) => <span className="text-xs text-slate-500">{new Date(l.timestamp).toLocaleString('en-IN')}</span> },
    { key: 'user', label: 'User', sortable: true, render: (l) => <span className="font-medium text-slate-900 dark:text-white">{l.user}</span> },
    {
      key: 'action', label: 'Action',
      render: (l) => {
        const colors: Record<string, string> = { create: 'badge-green', update: 'badge-blue', delete: 'badge-red', login: 'badge-yellow' };
        return <span className={colors[l.action] || 'badge-slate'}>{l.action}</span>;
      },
    },
    { key: 'module', label: 'Module', render: (l) => <span className="badge-slate">{l.module}</span> },
    { key: 'recordId', label: 'Record ID', render: (l) => <code className="text-xs text-slate-400">{l.recordId?.slice(0, 8) || '—'}...</code> },
    { key: 'ip', label: 'IP', render: (l) => l.ip || '—' },
  ];

  return (
    <AdminLayout title="Audit Logs">
      <div className="card p-4 mb-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input type="text" placeholder="User..." value={filters.user} onChange={e => setFilters({ ...filters, user: e.target.value })} className="input pl-9 text-sm" />
          </div>
          <select value={filters.module} onChange={e => setFilters({ ...filters, module: e.target.value })} className="select text-sm">
            <option value="">All Modules</option>
            <option value="services">Services</option>
            <option value="orders">Orders</option>
            <option value="customers">Customers</option>
            <option value="payments">Payments</option>
            <option value="auth">Auth</option>
            <option value="settings">Settings</option>
          </select>
          <select value={filters.action} onChange={e => setFilters({ ...filters, action: e.target.value })} className="select text-sm">
            <option value="">All Actions</option>
            <option value="create">Create</option>
            <option value="update">Update</option>
            <option value="delete">Delete</option>
            <option value="login">Login</option>
          </select>
          <input type="date" value={filters.startDate} onChange={e => setFilters({ ...filters, startDate: e.target.value })} className="input text-sm" placeholder="Start date" />
          <input type="date" value={filters.endDate} onChange={e => setFilters({ ...filters, endDate: e.target.value })} className="input text-sm" placeholder="End date" />
        </div>
        <div className="mt-3 flex justify-end">
          <button onClick={fetchLogs} className="btn-primary btn-sm"><Filter className="w-4 h-4" /> Apply Filters</button>
        </div>
      </div>

      <DataTable columns={columns} data={logs} loading={loading} error={error} onRetry={fetchLogs} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(l) => l._id} onRowClick={(l) => setExpanded(expanded === l._id ? null : l._id)} emptyMessage="No audit logs found" emptyDescription="Actions will be logged here." />

      {expanded && (
        <div className="card p-5 mt-3">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white">Change Details</h4>
            <button onClick={() => setExpanded(null)} className="text-slate-400 hover:text-slate-600">&times;</button>
          </div>
          {(() => {
            const log = logs.find(l => l._id === expanded);
            if (!log) return null;
            return (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-2">Old Value</p>
                  <pre className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-xs text-slate-700 dark:text-slate-300 overflow-x-auto max-h-60">{JSON.stringify(log.oldValue, null, 2) || 'N/A'}</pre>
                </div>
                <div>
                  <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-2">New Value</p>
                  <pre className="bg-slate-50 dark:bg-slate-900 rounded-lg p-3 text-xs text-slate-700 dark:text-slate-300 overflow-x-auto max-h-60">{JSON.stringify(log.newValue, null, 2) || 'N/A'}</pre>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </AdminLayout>
  );
}
