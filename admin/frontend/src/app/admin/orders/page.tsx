'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import {
  Search, Filter, ChevronDown, ChevronUp, Clock, CheckCircle,
  XCircle, AlertCircle, MessageSquare, RotateCcw, User, FileText,
  IndianRupee, CreditCard, Loader2, Download
} from 'lucide-react';

interface Order {
  id: string;
  orderNumber: string;
  customer: { id: string; name: string; email: string; phone: string };
  service: { id: string; name: string };
  amount: number;
  status: string;
  paymentStatus: string;
  paymentMethod: string;
  createdAt: string;
  notes?: string;
  timeline?: { status: string; timestamp: string; note?: string }[];
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [filters, setFilters] = useState({ status: '', paymentStatus: '', search: '' });

  useEffect(() => { fetchOrders(); }, [page, filters]);

  const fetchOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ page: String(page), limit: '10' });
      if (filters.status) params.set('status', filters.status);
      if (filters.paymentStatus) params.set('paymentStatus', filters.paymentStatus);
      if (filters.search) params.set('search', filters.search);
      const res = await apiGet<{ data: { orders: Order[]; pagination: { page: number; totalPages: number; total: number } } }>(`/admin/orders?${params}`);
      if (res.data) {
        setOrders(res.data.orders || []);
        setTotalPages(res.data.pagination?.totalPages || 1);
        setTotal(res.data.pagination?.total || 0);
      }
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const openDetail = async (order: Order) => {
    setDetailLoading(true);
    setSelectedOrder(order);
    try {
      const res = await apiGet<{ data: { order: Order } }>(`/admin/orders/${order.id}`);
      if (res.data?.order) setSelectedOrder(res.data.order);
    } catch {} finally { setDetailLoading(false); }
  };

  const updateStatus = async (id: string, status: string) => {
    try {
      await apiPut(`/admin/orders/${id}/status`, { status });
      toast.success(`Order ${status}`);
      fetchOrders();
      setSelectedOrder(null);
    } catch (err: any) { toast.error(err.message); }
  };

  const statusBadge = (s: string) => {
    const map: Record<string, string> = { pending: 'badge-yellow', processing: 'badge-blue', completed: 'badge-green', cancelled: 'badge-red', refunded: 'badge-red' };
    return <span className={map[s] || 'badge-slate'}>{s}</span>;
  };

  const paymentBadge = (s: string) => {
    const map: Record<string, string> = { pending: 'badge-yellow', paid: 'badge-green', failed: 'badge-red', refunded: 'badge-blue' };
    return <span className={map[s] || 'badge-slate'}>{s}</span>;
  };

  const columns: Column<Order>[] = [
    { key: 'orderNumber', label: 'Order #', sortable: true, render: (o) => <span className="font-medium text-admin-600 dark:text-admin-400">{o.orderNumber}</span> },
    { key: 'customer', label: 'Customer', render: (o) => o.customer?.name || 'N/A' },
    { key: 'service', label: 'Service', render: (o) => o.service?.name || 'N/A' },
    { key: 'amount', label: 'Amount', sortable: true, render: (o) => `₹${(o.amount || 0).toLocaleString('en-IN')}` },
    { key: 'status', label: 'Status', render: (o) => statusBadge(o.status) },
    { key: 'paymentStatus', label: 'Payment', render: (o) => paymentBadge(o.paymentStatus) },
    { key: 'createdAt', label: 'Date', sortable: true, render: (o) => new Date(o.createdAt).toLocaleDateString('en-IN') },
  ];

  const statusSteps = ['pending', 'processing', 'completed', 'cancelled'];

  return (
    <AdminLayout title="Orders">
      <div className="card p-4 mb-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input type="text" placeholder="Search by order # or customer..." value={filters.search} onChange={e => setFilters({ ...filters, search: e.target.value })} className="input pl-9" />
          </div>
          <select value={filters.status} onChange={e => setFilters({ ...filters, status: e.target.value })} className="select w-40">
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="processing">Processing</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <select value={filters.paymentStatus} onChange={e => setFilters({ ...filters, paymentStatus: e.target.value })} className="select w-40">
            <option value="">All Payments</option>
            <option value="pending">Pending</option>
            <option value="paid">Paid</option>
            <option value="failed">Failed</option>
            <option value="refunded">Refunded</option>
          </select>
          <button onClick={fetchOrders} className="btn-primary btn-sm"><Filter className="w-4 h-4" /> Filter</button>
        </div>
      </div>

      <DataTable columns={columns} data={orders} loading={loading} error={error} onRetry={fetchOrders} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={(o) => o.id} onRowClick={openDetail} emptyMessage="No orders found" emptyDescription="Orders will appear here once customers start placing them." />

      {selectedOrder && (
        <div className="fixed inset-0 z-40 flex justify-end">
          <div className="absolute inset-0 bg-black/50" onClick={() => setSelectedOrder(null)} />
          <div className="relative w-full max-w-lg bg-white dark:bg-slate-800 shadow-2xl overflow-y-auto">
            <div className="sticky top-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-6 py-4 flex items-center justify-between z-10">
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Order #{selectedOrder.orderNumber}</h2>
              <button onClick={() => setSelectedOrder(null)} className="text-slate-400 hover:text-slate-600">&times;</button>
            </div>

            {detailLoading ? (
              <div className="p-6 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div>
            ) : (
              <div className="p-6 space-y-6">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-slate-500 dark:text-slate-400">Customer</p>
                    <p className="font-medium text-slate-900 dark:text-white">{selectedOrder.customer?.name}</p>
                    <p className="text-slate-500">{selectedOrder.customer?.email}</p>
                  </div>
                  <div>
                    <p className="text-slate-500 dark:text-slate-400">Service</p>
                    <p className="font-medium text-slate-900 dark:text-white">{selectedOrder.service?.name}</p>
                  </div>
                  <div>
                    <p className="text-slate-500 dark:text-slate-400">Amount</p>
                    <p className="font-medium text-lg text-admin-600">₹{(selectedOrder.amount || 0).toLocaleString('en-IN')}</p>
                  </div>
                  <div>
                    <p className="text-slate-500 dark:text-slate-400">Payment</p>
                    <p>{paymentBadge(selectedOrder.paymentStatus)}</p>
                    <p className="text-xs text-slate-400 mt-1">{selectedOrder.paymentMethod}</p>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">Timeline</h4>
                  <div className="space-y-3">
                    {(selectedOrder.timeline || []).map((t, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <div className={`w-2 h-2 rounded-full mt-1.5 ${t.status === 'completed' ? 'bg-green-500' : t.status === 'cancelled' ? 'bg-red-500' : t.status === 'processing' ? 'bg-blue-500' : 'bg-yellow-500'}`} />
                        <div>
                          <p className="text-sm font-medium text-slate-700 dark:text-slate-300 capitalize">{t.status}</p>
                          {t.note && <p className="text-xs text-slate-500">{t.note}</p>}
                          <p className="text-xs text-slate-400">{new Date(t.timestamp).toLocaleString('en-IN')}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Notes</h4>
                  <p className="text-sm text-slate-600 dark:text-slate-400">{selectedOrder.notes || 'No notes'}</p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">Documents</h4>
                  <div className="space-y-2">
                    <a href="/admin/downloads" target="_blank" className="btn-secondary btn-sm inline-flex"><Download className="w-3.5 h-3.5" /> Download Generated PDF</a>
                    <a href="/admin/applications" className="btn-secondary btn-sm inline-flex"><FileText className="w-3.5 h-3.5" /> View Uploaded Docs</a>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">Update Status</h4>
                  <div className="flex flex-wrap gap-2">
                    {statusSteps.map(s => (
                      <button key={s} onClick={() => updateStatus(selectedOrder.id, s)} disabled={selectedOrder.status === s} className={`btn-sm capitalize ${selectedOrder.status === s ? 'btn-primary' : 'btn-secondary'}`}>{s}</button>
                    ))}
                  </div>
                </div>

                {selectedOrder.paymentStatus === 'paid' && (
                  <div>
                    <button onClick={() => updateStatus(selectedOrder.id, 'refunded')} className="btn-danger btn-sm"><RotateCcw className="w-3.5 h-3.5" /> Refund</button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
