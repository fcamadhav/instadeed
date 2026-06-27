'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import { Mail, Phone, ShoppingCart, IndianRupee, Calendar, Loader2, X } from 'lucide-react';

interface Customer {
  _id: string;
  name: string;
  email: string;
  phone: string;
  ordersCount: number;
  totalSpent: number;
  lastOrderDate: string;
  status: string;
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
  const [detailTab, setDetailTab] = useState<'orders' | 'documents' | 'notes' | 'logins'>('orders');
  const [detailData, setDetailData] = useState<any>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => { fetchCustomers(); }, [page]);

  const fetchCustomers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiGet<{ data: { customers: Customer[]; page: number; totalPages: number; total: number } }>(`/admin/customers?page=${page}&limit=10`);
      if (res.data) {
        setCustomers(res.data.customers || []);
        setTotalPages(res.data.totalPages || 1);
        setTotal(res.data.total || 0);
      }
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const openDetail = async (c: Customer) => {
    setSelected(c);
    setDetailTab('orders');
    setDetailLoading(true);
    try {
      const res = await apiGet<{ data: any }>(`/admin/customers/${c._id}`);
      setDetailData(res.data);
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
    { key: 'ordersCount', label: 'Orders', sortable: true, render: (c) => c.ordersCount || 0 },
    { key: 'totalSpent', label: 'Total Spent', sortable: true, render: (c) => `₹${(c.totalSpent || 0).toLocaleString('en-IN')}` },
    { key: 'lastOrderDate', label: 'Last Order', render: (c) => c.lastOrderDate ? new Date(c.lastOrderDate).toLocaleDateString('en-IN') : '—' },
    { key: 'status', label: 'Status', render: (c) => c.status === 'active' ? <span className="badge-green">Active</span> : <span className="badge-slate">Inactive</span> },
  ];

  const tabs = [
    { key: 'orders' as const, label: 'Orders' },
    { key: 'documents' as const, label: 'Documents' },
    { key: 'notes' as const, label: 'Notes' },
    { key: 'logins' as const, label: 'Login History' },
  ];

  return (
    <AdminLayout title="Customers">
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">Manage customer accounts</p>

      <DataTable columns={columns} data={customers} loading={loading} error={error} onRetry={fetchCustomers} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(c) => c._id} onRowClick={openDetail} emptyMessage="No customers yet" emptyDescription="Customers will appear here once they sign up." />

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
                  {(detailData?.orders || []).length === 0 ? (
                    <p className="text-sm text-slate-500 text-center py-4">No orders yet</p>
                  ) : (detailData?.orders || []).map((o: any) => (
                    <div key={o._id} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50">
                      <div>
                        <p className="text-sm font-medium text-slate-900 dark:text-white">{o.orderNumber}</p>
                        <p className="text-xs text-slate-500">{new Date(o.createdAt).toLocaleDateString('en-IN')}</p>
                      </div>
                      <span className="text-sm font-medium text-admin-600">₹{(o.amount || 0).toLocaleString('en-IN')}</span>
                    </div>
                  ))}
                </div>
              ) : detailTab === 'documents' ? (
                <p className="text-sm text-slate-500 text-center py-4">No documents uploaded</p>
              ) : detailTab === 'notes' ? (
                <p className="text-sm text-slate-500 text-center py-4">No notes</p>
              ) : (
                <p className="text-sm text-slate-500 text-center py-4">No login history</p>
              )}
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
