'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import {
  FileText, Plus, Search, Download, RefreshCw, Loader2,
  X, ChevronRight, ChevronLeft, Calendar, Clock, AlertTriangle,
  CheckCircle, Ban, Send, MessageSquare, Mail, Phone, Home,
  User, IndianRupee, MapPin, Hash, Eye
} from 'lucide-react';
import toast from 'react-hot-toast';

interface RentAgreement {
  id: string;
  agreementId: string;
  customerName: string;
  mobile: string;
  email: string;
  landlordName: string;
  tenantName: string;
  propertyAddress: string;
  startDate: string;
  endDate: string;
  duration: number;
  securityDeposit: number;
  monthlyRent: number;
  paymentStatus: string;
  renewalStatus: string;
  daysLeft: number;
  reminders: any[];
  timeline: any[];
}

interface Stats {
  totalActive: number;
  expired: number;
  renewed: number;
  expiring7: number;
  expiring15: number;
  expiring30: number;
  expiring60: number;
  expiring90: number;
  renewedThisMonth: number;
}

export default function RentAgreementsPage() {
  const [agreements, setAgreements] = useState<RentAgreement[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<Stats | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [expiryFilter, setExpiryFilter] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [selected, setSelected] = useState<RentAgreement | null>(null);
  const [detailTab, setDetailTab] = useState<'info' | 'timeline' | 'reminders'>('info');
  const [submitting, setSubmitting] = useState(false);

  const [form, setForm] = useState({
    customerName: '', mobile: '', email: '', landlordName: '', tenantName: '',
    propertyAddress: '', startDate: '', endDate: '', duration: 12,
    securityDeposit: 0, monthlyRent: 0, paymentStatus: 'PENDING',
  });

  useEffect(() => { fetchStats(); }, []);
  useEffect(() => { fetchAgreements(); }, [page, statusFilter, expiryFilter]);

  const fetchStats = async () => {
    try { const r = await apiGet<any>('/admin/rent-agreements/stats'); setStats(r.data); }
    catch { /* ignore */ }
  };

  const fetchAgreements = async () => {
    setLoading(true);
    try {
      let url = `/admin/rent-agreements?page=${page}&limit=15`;
      if (statusFilter) url += `&status=${statusFilter}`;
      if (expiryFilter) url += `&expiry=${expiryFilter}`;
      const r = await apiGet<any>(url);
      setAgreements(r.data.agreements || []);
      setTotalPages(r.data.pagination.totalPages || 1);
      setTotal(r.data.pagination.total || 0);
    } catch (e: any) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const r = await apiGet<any>(`/admin/rent-agreements?search=${encodeURIComponent(search)}&page=1&limit=15`);
      setAgreements(r.data.agreements || []);
      setTotalPages(r.data.pagination.totalPages || 1);
      setTotal(r.data.pagination.total || 0);
      setPage(1);
    } catch (e: any) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await apiPost('/admin/rent-agreements', form);
      toast.success('Agreement created');
      setShowForm(false);
      resetForm();
      fetchAgreements();
      fetchStats();
    } catch (e: any) { toast.error(e.message); }
    finally { setSubmitting(false); }
  };

  const resetForm = () => {
    setForm({ customerName: '', mobile: '', email: '', landlordName: '', tenantName: '',
      propertyAddress: '', startDate: '', endDate: '', duration: 12,
      securityDeposit: 0, monthlyRent: 0, paymentStatus: 'PENDING' });
  };

  const handleRenew = async (agreement: RentAgreement) => {
    if (!confirm(`Renew agreement ${agreement.agreementId}?`)) return;
    try {
      const body = {
        monthlyRent: agreement.monthlyRent,
        startDate: new Date(agreement.endDate).toISOString().split('T')[0],
        endDate: new Date(new Date(agreement.endDate).getTime() + agreement.duration * 30 * 86400000).toISOString().split('T')[0],
        duration: agreement.duration,
      };
      const r = await apiPost(`/admin/rent-agreements/${agreement.id}/renew`, body);
      toast.success(`Renewed → ${r.data.renewed.agreementId}`);
      fetchAgreements();
      fetchStats();
    } catch (e: any) { toast.error(e.message); }
  };

  const handleScheduleReminders = async (agreement: RentAgreement) => {
    try {
      await apiPost(`/admin/rent-agreements/${agreement.id}/reminders`, { channels: ['EMAIL', 'WHATSAPP', 'SMS'] });
      toast.success('Reminders scheduled');
      fetchAgreements();
    } catch (e: any) { toast.error(e.message); }
  };

  const openDetail = async (a: RentAgreement) => {
    setSelected(a);
    setDetailTab('info');
    try {
      const r = await apiGet<any>(`/admin/rent-agreements/${a.id}`);
      setSelected(r.data);
    } catch {}
  };

  const statusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE': return 'badge-green';
      case 'RENEWED': return 'badge-blue';
      case 'ARCHIVED': return 'badge-slate';
      default: return 'badge-slate';
    }
  };

  const daysColor = (days: number) => {
    if (days < 0) return 'text-slate-400';
    if (days <= 7) return 'text-red-600 font-bold';
    if (days <= 30) return 'text-orange-500 font-semibold';
    if (days <= 90) return 'text-yellow-500';
    return 'text-green-600';
  };

  const columns: Column<RentAgreement>[] = [
    {
      key: 'agreementId', label: 'Agreement ID', sortable: true,
      render: (a) => <span className="font-mono text-xs font-medium text-slate-900 dark:text-white">{a.agreementId}</span>,
    },
    {
      key: 'customerName', label: 'Customer', sortable: true,
      render: (a) => (
        <div>
          <div className="font-medium text-slate-900 dark:text-white text-sm">{a.customerName}</div>
          <div className="text-xs text-slate-400">{a.mobile}</div>
        </div>
      ),
    },
    {
      key: 'startDate', label: 'Start Date',
      render: (a) => <span className="text-sm">{new Date(a.startDate).toLocaleDateString('en-IN')}</span>,
    },
    {
      key: 'endDate', label: 'End Date',
      render: (a) => <span className="text-sm">{new Date(a.endDate).toLocaleDateString('en-IN')}</span>,
    },
    {
      key: 'daysLeft', label: 'Days Left', sortable: true,
      render: (a) => {
        const d = a.daysLeft;
        return <span className={`text-sm font-medium ${daysColor(d)}`}>{d < 0 ? 'Expired' : `${d}d`}</span>;
      },
    },
    {
      key: 'renewalStatus', label: 'Status',
      render: (a) => <span className={`badge ${statusColor(a.renewalStatus)}`}>{a.renewalStatus}</span>,
    },
    {
      key: 'actions', label: 'Actions',
      render: (a) => (
        <div className="flex items-center gap-1">
          {a.renewalStatus === 'ACTIVE' && a.daysLeft <= 90 && (
            <button onClick={(e) => { e.stopPropagation(); handleRenew(a); }}
              className="btn-primary btn-xs">Renew</button>
          )}
          {a.reminders?.length === 0 && a.renewalStatus === 'ACTIVE' && (
            <button onClick={(e) => { e.stopPropagation(); handleScheduleReminders(a); }}
              className="btn-secondary btn-xs p-1" title="Schedule Reminders"><Bell className="w-3 h-3" /></button>
          )}
        </div>
      ),
    },
  ];

  const filterChips = [
    { label: 'Today', value: 'today' },
    { label: '7 Days', value: '7days' },
    { label: '15 Days', value: '15days' },
    { label: '30 Days', value: '30days' },
    { label: '60 Days', value: '60days' },
    { label: '90 Days', value: '90days' },
    { label: 'Expired', value: 'expired' },
    { label: 'Renewed', value: 'renewed' },
  ];

  const StatCard = ({ label, value, color }: { label: string; value: number | string; color: string }) => (
    <div className={`card p-4 border-l-4 ${color}`}>
      <div className="text-2xl font-bold text-slate-900 dark:text-white">{value}</div>
      <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">{label}</div>
    </div>
  );

  return (
    <AdminLayout title="Rent Agreements">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Rent Agreements</h1>
          <button onClick={() => { resetForm(); setShowForm(true); }} className="btn-primary">
            <Plus className="w-4 h-4" /> New Agreement
          </button>
        </div>

        {stats && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 xl:grid-cols-8 gap-3">
            <StatCard label="Active" value={stats.totalActive} color="border-l-green-500" />
            <StatCard label="Expiring 90d" value={stats.expiring90} color="border-l-yellow-400" />
            <StatCard label="Expiring 60d" value={stats.expiring60} color="border-l-yellow-500" />
            <StatCard label="Expiring 30d" value={stats.expiring30} color="border-l-orange-400" />
            <StatCard label="Expiring 15d" value={stats.expiring15} color="border-l-orange-500" />
            <StatCard label="Expiring 7d" value={stats.expiring7} color="border-l-red-500" />
            <StatCard label="Expired" value={stats.expired} color="border-l-slate-400" />
            <StatCard label="Renewed/Month" value={stats.renewedThisMonth} color="border-l-blue-500" />
          </div>
        )}

        <div className="card p-4">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input value={search} onChange={e => setSearch(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
                placeholder="Search by name, mobile, ID, address..."
                className="input pl-9 py-2 text-sm" />
            </div>
            <select value={statusFilter} onChange={e => { setStatusFilter(e.target.value); setPage(1); }}
              className="input py-2 text-sm w-auto">
              <option value="">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="RENEWED">Renewed</option>
              <option value="ARCHIVED">Archived</option>
            </select>
            <button onClick={() => { setSearch(''); setStatusFilter(''); setExpiryFilter(''); setPage(1); }}
              className="btn-secondary btn-sm">Clear</button>
            <button onClick={fetchAgreements} className="btn-secondary btn-sm p-2">
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {filterChips.map(f => (
              <button key={f.value} onClick={() => setExpiryFilter(expiryFilter === f.value ? '' : f.value)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  expiryFilter === f.value
                    ? 'bg-admin-600 text-white'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600'
                }`}>{f.label}</button>
            ))}
          </div>
        </div>

        <DataTable columns={columns} data={agreements} loading={loading}
          page={page} totalPages={totalPages} total={total}
          onPageChange={setPage} keyExtractor={(a) => a.id}
          onRowClick={openDetail}
          emptyMessage="No rent agreements found"
          emptyDescription="Create your first rental agreement to get started."
        />

        {selected && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-start justify-center pt-10 pb-10 overflow-y-auto"
            onClick={() => setSelected(null)}>
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-3xl mx-4 overflow-hidden"
              onClick={e => e.stopPropagation()}>
              <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-700">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900 dark:text-white">{selected.agreementId}</h2>
                  <p className="text-sm text-slate-500">{selected.customerName}</p>
                </div>
                <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-slate-600"><X className="w-5 h-5" /></button>
              </div>

              <div className="flex border-b border-slate-200 dark:border-slate-700">
                {['info', 'timeline', 'reminders'].map(tab => (
                  <button key={tab} onClick={() => setDetailTab(tab as any)}
                    className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                      detailTab === tab
                        ? 'border-admin-600 text-admin-700 dark:text-admin-300'
                        : 'border-transparent text-slate-500 hover:text-slate-700'
                    }`}>{tab.charAt(0).toUpperCase() + tab.slice(1)}</button>
                ))}
              </div>

              <div className="p-6 max-h-[60vh] overflow-y-auto">
                {detailTab === 'info' && (
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {[
                      { l: 'Landlord', v: selected.landlordName, I: User },
                      { l: 'Tenant', v: selected.tenantName, I: User },
                      { l: 'Property', v: selected.propertyAddress, I: MapPin },
                      { l: 'Start Date', v: new Date(selected.startDate).toLocaleDateString('en-IN'), I: Calendar },
                      { l: 'End Date', v: new Date(selected.endDate).toLocaleDateString('en-IN'), I: Calendar },
                      { l: 'Duration', v: `${selected.duration} months`, I: Clock },
                      { l: 'Monthly Rent', v: `₹${selected.monthlyRent?.toLocaleString('en-IN')}`, I: IndianRupee },
                      { l: 'Deposit', v: `₹${selected.securityDeposit?.toLocaleString('en-IN')}`, I: IndianRupee },
                      { l: 'Payment', v: selected.paymentStatus, I: CheckCircle },
                      { l: 'Status', v: selected.renewalStatus, I: Ban },
                    ].map(({ l, v, I }) => (
                      <div key={l} className="flex items-start gap-2">
                        <I className="w-4 h-4 text-slate-400 mt-0.5" />
                        <div><div className="text-slate-500 text-xs">{l}</div><div className="font-medium text-slate-900 dark:text-white">{v}</div></div>
                      </div>
                    ))}
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
                          <div className="text-sm font-medium text-slate-900 dark:text-white">{t.event}</div>
                          <div className="text-xs text-slate-500">{t.description}</div>
                          <div className="text-xs text-slate-400">{new Date(t.createdAt).toLocaleString('en-IN')}</div>
                        </div>
                      </div>
                    )) : <p className="text-sm text-slate-500 text-center py-4">No timeline events</p>}
                  </div>
                )}

                {detailTab === 'reminders' && (
                  <div className="space-y-3">
                    {(selected as any).reminders?.length > 0 ? (selected as any).reminders.map((r: any) => (
                      <div key={r.id} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg">
                        <div>
                          <div className="text-sm font-medium text-slate-900 dark:text-white">{r.channel}</div>
                          <div className="text-xs text-slate-500">{new Date(r.remindAt).toLocaleString('en-IN')}</div>
                        </div>
                        <span className={`badge ${r.status === 'SENT' ? 'badge-green' : r.status === 'SCHEDULED' ? 'badge-blue' : 'badge-slate'}`}>
                          {r.status}
                        </span>
                      </div>
                    )) : <p className="text-sm text-slate-500 text-center py-4">No reminders scheduled</p>}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {showForm && (
          <div className="fixed inset-0 bg-black/50 z-50 flex items-start justify-center pt-10 pb-10 overflow-y-auto"
            onClick={() => setShowForm(false)}>
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-2xl mx-4 overflow-hidden"
              onClick={e => e.stopPropagation()}>
              <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-700">
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">New Rent Agreement</h2>
                <button onClick={() => setShowForm(false)} className="text-slate-400 hover:text-slate-600"><X className="w-5 h-5" /></button>
              </div>
              <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
                <div className="grid grid-cols-2 gap-4">
                  <FormField label="Customer Name" value={form.customerName}
                    onChange={v => setForm(p => ({ ...p, customerName: v }))} required />
                  <FormField label="Mobile" value={form.mobile}
                    onChange={v => setForm(p => ({ ...p, mobile: v }))} required />
                  <FormField label="Email" value={form.email} type="email"
                    onChange={v => setForm(p => ({ ...p, email: v }))} />
                  <FormField label="Landlord Name" value={form.landlordName}
                    onChange={v => setForm(p => ({ ...p, landlordName: v }))} required />
                  <FormField label="Tenant Name" value={form.tenantName}
                    onChange={v => setForm(p => ({ ...p, tenantName: v }))} required />
                  <div className="col-span-2">
                    <label className="label">Property Address</label>
                    <textarea value={form.propertyAddress} onChange={e => setForm(p => ({ ...p, propertyAddress: e.target.value }))}
                      className="input" rows={2} required />
                  </div>
                  <FormField label="Start Date" value={form.startDate} type="date"
                    onChange={v => setForm(p => ({ ...p, startDate: v }))} required />
                  <FormField label="End Date" value={form.endDate} type="date"
                    onChange={v => setForm(p => ({ ...p, endDate: v }))} required />
                  <FormField label="Duration (months)" value={String(form.duration)} type="number"
                    onChange={v => setForm(p => ({ ...p, duration: parseInt(v) || 0 }))} required />
                  <FormField label="Monthly Rent (₹)" value={String(form.monthlyRent)} type="number"
                    onChange={v => setForm(p => ({ ...p, monthlyRent: parseInt(v) || 0 }))} required />
                  <FormField label="Security Deposit (₹)" value={String(form.securityDeposit)} type="number"
                    onChange={v => setForm(p => ({ ...p, securityDeposit: parseInt(v) || 0 }))} required />
                  <div>
                    <label className="label">Payment Status</label>
                    <select value={form.paymentStatus}
                      onChange={e => setForm(p => ({ ...p, paymentStatus: e.target.value }))} className="input">
                      <option value="PENDING">Pending</option>
                      <option value="PAID">Paid</option>
                      <option value="PARTIAL">Partial</option>
                    </select>
                  </div>
                </div>
                <div className="flex justify-end gap-3 pt-4 border-t border-slate-200 dark:border-slate-700">
                  <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
                  <button type="submit" disabled={submitting} className="btn-primary">
                    {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                    Create Agreement
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AdminLayout>
  );
}

function FormField({ label, value, onChange, type = 'text', required }: {
  label: string; value: string; onChange: (v: string) => void; type?: string; required?: boolean;
}) {
  return (
    <div>
      <label className="label">{label}{required && ' *'}</label>
      <input type={type} value={value} onChange={e => onChange(e.target.value)}
        className="input" required={required} />
    </div>
  );
}

function Bell({ className }: { className?: string }) {
  return <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
    strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
  </svg>;
}
