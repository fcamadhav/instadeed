'use client';

import { useState, useEffect, useCallback } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Search, Filter, Clock, CheckCircle, XCircle, AlertCircle, MessageSquare, RotateCcw, FileText, IndianRupee, CreditCard, Loader2, Download } from 'lucide-react';

interface Order {
  id: string; orderNumber: string; customerName: string | null; customerPhone: string | null; customerEmail: string | null;
  service: { id: string; name: string } | null;
  amount: number; total: number; status: string; paymentStatus: string;
  notes: string | null; createdAt: string; quotation: any;
  customer: { id: string; name: string; email: string; phone: string } | null;
  subStatus: string | null;
}

const SUB_STATUSES: Record<string,Record<string,string>> = {
  PENDING: { default: 'Awaiting Documents', 'Awaiting Documents':'Missing Co-Applicant Info','Payment Pending':'Payment Awaiting' },
  PROCESSING: { default: 'Under Review', 'Verification':'Draft Verification','Stamp':'Procuring Stamp Paper','Sign':'Awaiting E-Signatures' },
  COMPLETED: { default: 'Delivered', 'Downloaded':'Downloaded','Dispatched':'Dispatched','Delivered':'Delivered' },
  CANCELLED: { default: 'Cancelled' },
  REFUNDED: { default: 'Refunded' },
};

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
  const [exporting, setExporting] = useState(false);

  useEffect(() => { fetchOrders(); }, [page, filters]);

  const fetchOrders = async () => {
    setLoading(true); setError(null);
    try {
      const params = new URLSearchParams({ page: String(page), limit: '10' });
      if (filters.status) params.set('status', filters.status);
      if (filters.paymentStatus) params.set('paymentStatus', filters.paymentStatus);
      if (filters.search) params.set('search', filters.search);
      const res = await apiGet<{ data: { orders: Order[]; pagination: { page: number; totalPages: number; total: number } } }>(`/orders?${params}`);
      if (res.data) { setOrders(res.data.orders || []); setTotalPages(res.data.pagination?.totalPages || 1); setTotal(res.data.pagination?.total || 0); }
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const openDetail = async (order: Order) => {
    setDetailLoading(true); setSelectedOrder(order);
    try { const res = await apiGet<{ data: Order }>(`/orders/${order.id}`); if (res.data) setSelectedOrder(res.data); }
    catch { toast.error('Failed to load order details'); } finally { setDetailLoading(false); }
  };

  const updateStatus = async (id: string, status: string) => {
    try { await apiPut(`/admin/orders/${id}/status`, { status }); toast.success(`Order ${status}`); fetchOrders(); setSelectedOrder(null); }
    catch (err: any) { toast.error(err.message); }
  };

  const exportCSV = async () => {
    setExporting(true);
    try {
      const params = new URLSearchParams({ limit: '10000' });
      if (filters.status) params.set('status', filters.status);
      if (filters.paymentStatus) params.set('paymentStatus', filters.paymentStatus);
      if (filters.search) params.set('search', filters.search);
      const res = await apiGet<{ data: { orders: Order[] } }>(`/orders?${params}`);
      const orders = res.data?.orders || [];
      const header = 'Order ID,Customer,Phone,Email,Service,Amount,Status,Payment,Date\n';
      const rows = orders.map(o => [
        o.orderNumber, (o.customerName||o.customer?.name||'N/A').replace(/,/g,' '),
        (o.customerPhone||o.customer?.phone||''), (o.customerEmail||o.customer?.email||''),
        (o.service?.name||'N/A'), o.total||o.amount, o.status, o.paymentStatus,
        new Date(o.createdAt).toLocaleDateString('en-IN')
      ].join(',')).join('\n');
      const blob = new Blob([header + rows], {type:'text/csv'});
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
      a.download = `orders-export-${new Date().toISOString().slice(0,10)}.csv`;
      a.click(); URL.revokeObjectURL(a.href);
      toast.success(`Exported ${orders.length} orders`);
    } catch { toast.error('Export failed'); }
    finally { setExporting(false); }
  };

  const statusLabel = (s: string) => s?.replace(/_/g,' ').replace(/\b\w/g, c => c.toUpperCase());
  const subStatusLabel = (o: Order) => {
    if (o.subStatus) return o.subStatus;
    const statusGroup = SUB_STATUSES[o.status?.toUpperCase()] || {};
    return statusGroup.default || statusLabel(o.status||'');
  };

  const columns: Column<Order>[] = [
    { key:'orderNumber', label:'Order ID', render:(o)=><span className="font-bold text-admin-600">{o.orderNumber}</span> },
    { key:'customerName', label:'Customer', render:(o)=><div><span className="font-medium text-slate-900">{o.customerName||o.customer?.name||'N/A'}</span>{o.customerPhone && <span className="block text-xs text-slate-400">{o.customerPhone}</span>}</div> },
    { key:'service', label:'Service', render:(o)=><span className="text-sm text-slate-600">{o.service?.name||'N/A'}</span> },
    { key:'total', label:'Amount', render:(o)=><span className="font-semibold">₹{(o.total||o.amount||0).toLocaleString('en-IN')}</span> },
    {
      key:'paymentStatus', label:'Payment',
      render:(o)=><span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${o.paymentStatus==='PAID'?'bg-green-100 text-green-700':o.paymentStatus==='PENDING'?'bg-yellow-100 text-yellow-700':'bg-slate-100 text-slate-600'}`}>{statusLabel(o.paymentStatus)}</span>
    },
    {
      key:'status', label:'Status',
      render:(o)=><div><span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${o.status==='COMPLETED'?'bg-green-100 text-green-700':o.status==='PENDING'?'bg-yellow-100 text-yellow-700':o.status==='PROCESSING'?'bg-blue-100 text-blue-700':'bg-slate-100 text-slate-600'}`}>{statusLabel(o.status)}</span><span className="block text-[10px] text-slate-400 mt-0.5">{subStatusLabel(o)}</span></div>
    },
    { key:'createdAt', label:'Created', render:(o)=><span className="text-xs text-slate-500">{new Date(o.createdAt).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'})}</span> },
  ];

  return (
    <AdminLayout title="Orders">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
        <div className="flex items-center gap-2 flex-wrap">
          <div className="relative"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400"/><input type="text" placeholder="Search..." value={filters.search} onChange={e=>setFilters({...filters,search:e.target.value})} className="input pl-9 text-sm w-48"/></div>
          <select value={filters.status} onChange={e=>setFilters({...filters,status:e.target.value})} className="select text-sm"><option value="">All Status</option><option value="PENDING">Pending</option><option value="PROCESSING">Processing</option><option value="COMPLETED">Completed</option><option value="CANCELLED">Cancelled</option></select>
          <select value={filters.paymentStatus} onChange={e=>setFilters({...filters,paymentStatus:e.target.value})} className="select text-sm"><option value="">All Payments</option><option value="PAID">Paid</option><option value="PENDING">Pending</option><option value="FAILED">Failed</option></select>
          <button onClick={fetchOrders} className="btn-primary btn-sm"><Filter className="w-3 h-3"/> Filter</button>
        </div>
        <button onClick={exportCSV} disabled={exporting} className="btn-secondary btn-sm"><Download className="w-3 h-3"/> {exporting?'Exporting...':'Export CSV'}</button>
      </div>

      <DataTable columns={columns} data={orders} loading={loading} error={error} onRetry={fetchOrders} page={page} totalPages={totalPages} total={total} onPageChange={setPage} keyExtractor={o=>o.id} onRowClick={openDetail} emptyMessage="No orders found"/>

      {selectedOrder && (
        <div className="fixed inset-0 z-40 flex justify-end">
          <div className="absolute inset-0 bg-black/50" onClick={()=>setSelectedOrder(null)}/>
          <div className="relative w-full max-w-lg bg-white dark:bg-slate-800 shadow-2xl overflow-y-auto">
            <div className="sticky top-0 bg-white dark:bg-slate-800 border-b px-6 py-4 flex items-center justify-between">
              <div><h2 className="font-semibold text-slate-900">{selectedOrder.orderNumber}</h2><p className="text-xs text-slate-500">{selectedOrder.service?.name||'Service'}</p></div>
              <button onClick={()=>setSelectedOrder(null)} className="text-slate-400 hover:text-slate-600 text-xl">&times;</button>
            </div>
            <div className="p-4 space-y-4">
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-slate-500">Customer</span><p className="font-medium">{selectedOrder.customerName||selectedOrder.customer?.name||'N/A'}</p></div>
                <div><span className="text-slate-500">Phone</span><p className="font-medium">{selectedOrder.customerPhone||selectedOrder.customer?.phone||'—'}</p></div>
                <div><span className="text-slate-500">Email</span><p className="font-medium text-xs">{selectedOrder.customerEmail||selectedOrder.customer?.email||'—'}</p></div>
                <div><span className="text-slate-500">Amount</span><p className="font-bold">₹{(selectedOrder.total||selectedOrder.amount||0).toLocaleString('en-IN')}</p></div>
                <div><span className="text-slate-500">Status</span><p className={selectedOrder.status==='COMPLETED'?'text-green-600 font-semibold':'text-yellow-600 font-semibold'}>{statusLabel(selectedOrder.status)}</p></div>
                <div><span className="text-slate-500">Payment</span><p className={selectedOrder.paymentStatus==='PAID'?'text-green-600 font-semibold':'text-yellow-600 font-semibold'}>{statusLabel(selectedOrder.paymentStatus)}</p></div>
              </div>
              <div><h4 className="text-sm font-semibold text-slate-700 mb-2">Update Status</h4><div className="flex flex-wrap gap-2">
                {['DRAFT','PENDING','PROCESSING','VERIFICATION','DOCUMENTS_UPLOADED','DRAFT_READY','SIGN_PENDING','COMPLETED','CANCELLED','REFUNDED'].map(s=><button key={s} onClick={()=>updateStatus(selectedOrder.id,s)} disabled={selectedOrder.status===s} className={`btn-sm capitalize ${selectedOrder.status===s?'btn-primary':'btn-secondary'}`}>{statusLabel(s)}</button>)}
              </div></div>
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
