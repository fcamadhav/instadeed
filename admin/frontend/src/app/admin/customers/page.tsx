'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import { Mail, Phone, ShoppingCart, IndianRupee, Calendar, Loader2, X, Monitor, Clock } from 'lucide-react';

interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  isActive: boolean;
  createdAt: string;
  lastLoginAt: string | null;
  _count: { orders: number };
}

interface LoginRecord {
  id: string;
  ipAddress: string | null;
  userAgent: string | null;
  createdAt: string;
}

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [selected, setSelected] = useState<Customer | null>(null);
  const [detailTab, setDetailTab] = useState<'orders' | 'documents' | 'logins'>('orders');
  const [detailData, setDetailData] = useState<any>(null);
  const [ordersData, setOrdersData] = useState<any[]>([]);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => { fetchCustomers(); }, [page]);

  const fetchCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiGet<{ data: { customers: Customer[]; pagination: { page: number; totalPages: number; total: number } } }>(`/admin/customers?page=${page}&limit=10`);
      if (res.data) {
        setCustomers(res.data.customers || []);
        setTotalPages(res.data.pagination?.totalPages || 1);
        setTotal(res.data.pagination?.total || 0);
      }
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const openDetail = async (c: Customer) => {
    setSelected(c);
    setDetailTab('orders');
    setDetailLoading(true);
    setOrdersData([]);
    try {
      const [detailRes, ordersRes] = await Promise.all([
        apiGet<{ data: any }>(`/admin/customers/${c.id}`).catch(() => null),
        apiGet<{ data: { orders: any[] } }>(`/admin/customers/${c.id}/orders`).catch(() => null),
      ]);
      if (detailRes?.data) setDetailData(detailRes.data);
      if (ordersRes?.data?.orders) setOrdersData(ordersRes.data.orders);
    } catch {} finally { setDetailLoading(false); }
  };

  const columns: Column<Customer>[] = [
    {
      key: 'name', label: 'Name', sortable: true,
      render: (c) => (
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-admin-100 dark:bg-admin-900/30 flex items-center justify-center text-sm font-medium text-admin-700 dark:text-admin-300">
            {c.name?.charAt(0)?.toUpperCase() || '?'}
          </div>
          <span className="font-medium text-slate-900 dark:text-white">{c.name}</span>
        </div>
      ),
    },
    { key: 'email', label: 'Email', render: (c) => <span className="text-xs text-slate-500">{c.email}</span> },
    { key: 'phone', label: 'Phone', render: (c) => c.phone || '—' },
    { key: '_count', label: 'Orders', render: (c) => c._count?.orders || 0 },
    { key: 'lastLoginAt', label: 'Last Login', render: (c) => c.lastLoginAt ? new Date(c.lastLoginAt).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : 'Never' },
    { key: 'isActive', label: 'Status', render: (c) => c.isActive ? <span className="badge-green">Active</span> : <span className="badge-slate">Inactive</span> },
  ];

  const tabs = [
    { key: 'orders' as const, label: 'Orders' },
    { key: 'documents' as const, label: 'Documents' },
    { key: 'logins' as const, label: 'Login History' },
  ];

  function shortenUA(ua: string | null): string {
    if (!ua) return 'Unknown';
    const m = ua.match(/Chrome\/(\d+)/);
    if (m) return `Chrome ${m[1]}`;
    const f = ua.match(/Firefox\/(\d+)/);
    if (f) return `Firefox ${f[1]}`;
    const s = ua.match(/Safari\/(\d+)/);
    if (s && !ua.includes('Chrome')) return `Safari ${s[1]}`;
    if (ua.includes('Mobile')) return 'Mobile Browser';
    return 'Desktop Browser';
  }

  return (
    <AdminLayout title="Customers">
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">Manage customer accounts and view login history</p>

      <DataTable columns={columns} data={customers} loading={loading} error={error} onRetry={fetchCustomers} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(c) => c.id} onRowClick={openDetail} emptyMessage="No customers yet" emptyDescription="Customers will appear here after they sign in via Google." />

      {selected && (
        <div className="fixed inset-0 z-40 flex justify-end">
          <div className="absolute inset-0 bg-black/50" onClick={() => setSelected(null)} />
          <div className="relative w-full max-w-lg bg-white dark:bg-slate-800 shadow-2xl overflow-y-auto">
            <div className="sticky top-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-admin-100 dark:bg-admin-900/30 flex items-center justify-center text-lg font-medium text-admin-700 dark:text-admin-300">{selected.name?.charAt(0)?.toUpperCase()}</div>
                <div>
                  <h2 className="font-semibold text-slate-900 dark:text-white">{selected.name}</h2>
                  <p className="text-xs text-slate-500">{selected.email}</p>
                </div>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-slate-600 text-xl">&times;</button>
            </div>

            <div className="border-b border-slate-200 dark:border-slate-700 flex">
              {tabs.map(t => (
                <button key={t.key} onClick={() => setDetailTab(t.key)} className={`px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${detailTab === t.key ? 'border-admin-600 text-admin-600 dark:text-admin-400' : 'border-transparent text-slate-500 hover:text-slate-700'}`}>{t.label}</button>
              ))}
            </div>

            <div className="p-4">
              {detailLoading ? (
                <div className="py-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div>
              ) : detailTab === 'orders' ? (
                <div className="space-y-2">
                  {ordersData.length === 0 ? (
                    <p className="text-sm text-slate-500 text-center py-4">No orders yet</p>
                  ) : ordersData.map((o: any) => (
                    <div key={o.id} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50">
                      <div>
                        <p className="text-sm font-medium text-slate-900 dark:text-white">{o.orderNumber}</p>
                        <p className="text-xs text-slate-500">{new Date(o.createdAt).toLocaleDateString('en-IN')} &middot; {o.status}</p>
                      </div>
                      <span className="text-sm font-medium text-admin-600">₹{(o.amount || 0).toLocaleString('en-IN')}</span>
                    </div>
                  ))}
                </div>
              ) : detailTab === 'documents' ? (
                <p className="text-sm text-slate-500 text-center py-4">No documents uploaded</p>
              ) : (
                /* Login History tab */
                <div className="space-y-2">
                  {(!detailData?.loginHistory || detailData.loginHistory.length === 0) ? (
                    <p className="text-sm text-slate-500 text-center py-4">No login history</p>
                  ) : detailData.loginHistory.map((l: LoginRecord) => (
                    <div key={l.id} className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50">
                      <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <Monitor className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="text-sm font-medium text-slate-900 dark:text-white">{shortenUA(l.userAgent)}</p>
                        </div>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-xs text-slate-500 flex items-center gap-1"><Clock className="w-3 h-3" />{new Date(l.createdAt).toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</span>
                          {l.ipAddress && <span className="text-xs text-slate-400">IP: {l.ipAddress}</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                  {detailData?._count?.loginHistory > (detailData?.loginHistory?.length || 0) && (
                    <p className="text-xs text-slate-400 text-center pt-2">Showing last {detailData.loginHistory.length} of {detailData._count.loginHistory} logins</p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
