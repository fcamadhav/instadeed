'use client';

import { useState, useEffect, useCallback } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Search, Download, IndianRupee, Clock, CheckCircle, XCircle, Loader2, MoreHorizontal, ExternalLink } from 'lucide-react';

interface Order {
  id: string; orderNumber: string; customerName: string | null; customerPhone: string | null; customerEmail: string | null;
  customer: { id: string; name: string; email: string; phone: string } | null;
  service: { id: string; name: string } | null; amount: number; total: number;
  status: string; paymentStatus: string; notes: string | null; createdAt: string; quotation: any;
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [payFilter, setPayFilter] = useState('');
  const [selected, setSelected] = useState<Order | null>(null);
  const [selectedFull, setSelectedFull] = useState<any>(null);
  const [custProfile, setCustProfile] = useState<any>(null);
  const [custOrders, setCustOrders] = useState<any[]>([]);
  const [custLoading, setCustLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [summary, setSummary] = useState({ total: 0, revenue: 0, pending: 0, completed: 0 });

  const fmt = (n: number) => n?.toLocaleString('en-IN') || '0';
  const date = (d: string) => new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  const statusColor = (s: string) => s === 'COMPLETED' ? 'bg-emerald-50 text-emerald-700' : s === 'PROCESSING' ? 'bg-blue-50 text-blue-700' : s === 'CANCELLED' ? 'bg-red-50 text-red-700' : 'bg-amber-50 text-amber-700';
  const payColor = (s: string) => s === 'PAID' ? 'bg-emerald-50 text-emerald-700' : s === 'FAILED' ? 'bg-red-50 text-red-700' : 'bg-amber-50 text-amber-700';
  const custName = (o: Order) => o.customerName || o.customer?.name || o.customerEmail || o.customerPhone || 'N/A';
  const custSub = (o: Order) => o.customerPhone || o.customer?.phone || (o.customerName ? '' : o.customerEmail || '');
  const label = (s: string) => s?.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  const fetchOrders = useCallback(async () => {
    setLoading(true);
    try {
      const p = new URLSearchParams({ page: String(page), limit: '15' });
      if (statusFilter) p.set('status', statusFilter);
      if (payFilter) p.set('paymentStatus', payFilter);
      if (search) p.set('search', search);
      const [ord, all] = await Promise.all([
        apiGet<{ data: { orders: Order[]; pagination: { totalPages: number } } }>(`/orders?${p}`),
        apiGet<{ data: { orders: Order[] } }>('/orders?limit=10000'),
      ]);
      if (ord?.data) { setOrders(ord.data.orders || []); setTotalPages(ord.data.pagination?.totalPages || 1); }
      if (all?.data?.orders) {
        const o = all.data.orders;
        setSummary({ total: o.length, revenue: o.reduce((s:any,x:any)=>x.status==='COMPLETED'?s+(x.total||x.amount||0):s,0), pending: o.filter((x:any)=>x.status==='PENDING'||x.status==='PROCESSING').length, completed: o.filter((x:any)=>x.status==='COMPLETED').length });
      }
    } catch {} finally { setLoading(false); }
  }, [page, search, statusFilter, payFilter]);

  useEffect(() => { fetchOrders(); }, [fetchOrders]);

  const openDetail = async (o: Order) => {
    setSelected(o);
    try { const r = await apiGet<{ data: any }>(`/orders/${o.id}`); if (r.data) setSelectedFull(r.data); }
    catch { toast.error('Failed to load'); }
  };

  const openCustomerProfile = async (o: Order) => {
    setCustLoading(true); setCustProfile({ name: custName(o), phone: custSub(o), email: o.customerEmail || o.customer?.email });
    try {
      const custs = await apiGet<{ data: { customers: any[] } }>(`/admin/customers?search=${encodeURIComponent(o.customerEmail || o.customerPhone || o.customerName || '')}`);
      if (custs?.data?.customers?.length > 0) {
        const cid = custs.data.customers[0].id;
        const [detail, orders] = await Promise.all([
          apiGet<{ data: any }>(`/admin/customers/${cid}`),
          apiGet<{ data: { orders: any[] } }>('/orders?limit=100'),
        ]);
        const custOrders = (orders?.data?.orders || []).filter((x:any) => (x.customerEmail && x.customerEmail === o.customerEmail) || (x.customerPhone && x.customerPhone === o.customerPhone));
        setCustOrders(custOrders);
        setCustProfile({ ...custProfile, ...detail?.data, totalOrders: custOrders.length, lifetimeValue: custOrders.reduce((s,x)=>s+(x.total||x.amount||0),0) });
      }
    } catch {} finally { setCustLoading(false); }
  };

  const updateStatus = async (id: string, status: string) => {
    try { await apiPut(`/admin/orders/${id}/status`, { status }); toast.success(`Updated to ${label(status)}`); setSelected(null); fetchOrders(); }
    catch (e: any) { toast.error(e.message || 'Failed'); }
  };

  const exportCSV = async () => { setExporting(true);
    try { const p = new URLSearchParams({ limit: '10000' }); if (statusFilter) p.set('status', statusFilter); if (payFilter) p.set('paymentStatus', payFilter); if (search) p.set('search', search);
      const r = await apiGet<{ data: { orders: Order[] } }>(`/orders?${p}`);
      const rows = (r.data?.orders||[]).map(o => [o.orderNumber, custName(o), o.customerPhone||o.customer?.phone||'', o.customerEmail||o.customer?.email||'', o.service?.name||'', o.total||o.amount, o.status, o.paymentStatus, date(o.createdAt)].join(','));
      const blob = new Blob(['Order,Customer,Phone,Email,Service,Amount,Status,Payment,Date\n'+rows.join('\n')], {type:'text/csv'});
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `orders-${new Date().toISOString().slice(0,10)}.csv`; a.click(); toast.success('Exported');
    } catch { toast.error('Export failed'); } finally { setExporting(false); }
  };

  return (
    <AdminLayout title="Orders">
      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        {[{label:'Total Orders',value:summary.total,icon:IndianRupee,color:'text-slate-600',bg:'bg-slate-50'},{label:'Revenue',value:`₹${fmt(summary.revenue)}`,icon:IndianRupee,color:'text-emerald-600',bg:'bg-emerald-50'},{label:'Pending',value:summary.pending,icon:Clock,color:'text-amber-600',bg:'bg-amber-50'},{label:'Completed',value:summary.completed,icon:CheckCircle,color:'text-blue-600',bg:'bg-blue-50'}].map(c=><div key={c.label} className={`${c.bg} rounded-xl p-3`}><div className="flex items-center justify-between"><span className="text-xs font-medium text-slate-500">{c.label}</span><c.icon className={`w-4 h-4 ${c.color}`}/></div><p className={`text-lg font-bold mt-1 ${c.color}`}>{c.value}</p></div>)}
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 mb-3">
        <div className="relative flex-1 max-w-xs"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400"/><input type="text" placeholder="Search orders..." value={search} onChange={e=>{setSearch(e.target.value);setPage(1)}} className="w-full h-8 pl-9 pr-3 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none focus:border-slate-300 focus:ring-1 focus:ring-slate-200"/></div>
        <div className="flex gap-2">
          <select value={statusFilter} onChange={e=>{setStatusFilter(e.target.value);setPage(1)}} className="h-8 px-2 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none"><option value="">All Status</option><option value="PENDING">Pending</option><option value="PROCESSING">Processing</option><option value="COMPLETED">Completed</option><option value="CANCELLED">Cancelled</option></select>
          <select value={payFilter} onChange={e=>{setPayFilter(e.target.value);setPage(1)}} className="h-8 px-2 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none"><option value="">All Payments</option><option value="PAID">Paid</option><option value="PENDING">Pending</option><option value="FAILED">Failed</option></select>
          <button onClick={exportCSV} disabled={exporting} className="h-8 px-3 text-xs font-medium bg-white border border-slate-200 rounded-lg hover:bg-slate-50 flex items-center gap-1.5"><Download className="w-3 h-3"/>{exporting?'Exporting...':'Export'}</button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50/50">
                <th className="h-11 px-4 text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Order</th>
                <th className="h-11 px-4 text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Customer</th>
                <th className="h-11 px-4 text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider hidden md:table-cell">Service</th>
                <th className="h-11 px-4 text-right text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Amount</th>
                <th className="h-11 px-4 text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Payment</th>
                <th className="h-11 px-4 text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wider hidden sm:table-cell">Status</th>
                <th className="h-11 px-4 text-right text-[11px] font-semibold text-slate-500 uppercase tracking-wider hidden lg:table-cell">Date</th>
                <th className="h-11 w-10"></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={8} className="py-12 text-center"><Loader2 className="w-5 h-5 animate-spin text-slate-300 mx-auto"/></td></tr>
              ) : orders.length === 0 ? (
                <tr><td colSpan={8} className="py-12 text-center text-sm text-slate-400">No orders found</td></tr>
              ) : orders.map(o => (
                <tr key={o.id} className="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                  <td className="py-2.5 px-4">
                    <button onClick={(e)=>{e.stopPropagation();openDetail(o)}} className="text-xs font-mono font-semibold text-admin-600 hover:text-admin-800 hover:underline focus:outline-none focus:underline cursor-pointer transition-colors">
                      #{o.orderNumber.replace('ID-','')}
                    </button>
                  </td>
                  <td className="py-2.5 px-4">
                    <button onClick={(e)=>{e.stopPropagation();openCustomerProfile(o)}} className="text-left hover:underline focus:outline-none">
                      <span className="text-xs font-medium text-slate-800">{custName(o)}</span>
                      {custSub(o) && <span className="block text-[11px] text-slate-400">{custSub(o)}</span>}
                    </button>
                  </td>
                  <td className="py-2.5 px-4 hidden md:table-cell"><span className="text-xs text-slate-600">{o.service?.name || 'N/A'}</span></td>
                  <td className="py-2.5 px-4 text-right"><span className="text-xs font-semibold text-slate-800">₹{fmt(o.total||o.amount||0)}</span></td>
                  <td className="py-2.5 px-4"><span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${payColor(o.paymentStatus)}`}>{label(o.paymentStatus)}</span></td>
                  <td className="py-2.5 px-4 hidden sm:table-cell"><span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${statusColor(o.status)}`}>{label(o.status)}</span></td>
                  <td className="py-2.5 px-4 text-right hidden lg:table-cell"><span className="text-[11px] text-slate-400">{date(o.createdAt)}</span></td>
                  <td className="py-2.5 px-1">
                    <button onClick={e=>{e.stopPropagation();openDetail(o)}} className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400"><MoreHorizontal className="w-3.5 h-3.5"/></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-4 py-2 border-t border-slate-100 bg-slate-50/30">
            <span className="text-[11px] text-slate-400">Page {page} of {totalPages}</span>
            <div className="flex gap-1">
              <button onClick={()=>setPage(p=>Math.max(1,p-1))} disabled={page===1} className="px-2 py-1 text-[11px] font-medium rounded-md bg-white border border-slate-200 hover:bg-slate-50 disabled:opacity-30">Prev</button>
              <button onClick={()=>setPage(p=>Math.min(totalPages,p+1))} disabled={page===totalPages} className="px-2 py-1 text-[11px] font-medium rounded-md bg-white border border-slate-200 hover:bg-slate-50 disabled:opacity-30">Next</button>
            </div>
          </div>
        )}
      </div>

      {/* Detail Slide-over */}
      {selected && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="absolute inset-0 bg-black/40" onClick={()=>{setSelected(null);setSelectedFull(null)}}/>
          <div className="relative w-full max-w-md bg-white shadow-2xl overflow-y-auto animate-in slide-in-from-right duration-200">
            <div className="sticky top-0 bg-white border-b border-slate-100 px-5 py-3 flex items-center justify-between z-10">
              <div><h3 className="text-sm font-bold text-slate-900">#{selected.orderNumber.replace('ID-','')}</h3><p className="text-[11px] text-slate-400">{selected.service?.name||'Service'}</p></div>
              <button onClick={()=>{setSelected(null);setSelectedFull(null)}} className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400 text-lg">&times;</button>
            </div>
            <div className="p-5 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[{k:'Customer',v:custName(selected)},{k:'Phone',v:selected.customerPhone||selected.customer?.phone||'—'},{k:'Email',v:selected.customerEmail||selected.customer?.email||'—'},{k:'Amount',v:'₹'+fmt(selected.total||selected.amount||0)},{k:'Status',v:label(selected.status),c:statusColor(selected.status)},{k:'Payment',v:label(selected.paymentStatus),c:payColor(selected.paymentStatus)}].map(f=><div key={f.k}><p className="text-[10px] font-medium text-slate-400 uppercase">{f.k}</p><p className={`text-xs font-semibold mt-0.5 ${f.c||'text-slate-800'}`}>{f.v}</p></div>)}
              </div>
              <div><p className="text-[10px] font-medium text-slate-400 uppercase mb-2">Update Status</p>
                <div className="flex flex-wrap gap-1.5">
                  {['PENDING','PROCESSING','VERIFICATION','DRAFT_READY','SIGN_PENDING','COMPLETED','CANCELLED'].map(s=><button key={s} onClick={()=>updateStatus(selected.id,s)} className={`px-2.5 py-1 text-[10px] font-semibold rounded-full border transition-colors ${selected.status===s?'bg-slate-800 text-white border-slate-800':'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'}`}>{label(s)}</button>)}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Customer Profile Slide-over */}
      {custProfile && (
        <div className="fixed inset-0 z-50 flex justify-end">
          <div className="absolute inset-0 bg-black/40" onClick={()=>{setCustProfile(null);setCustOrders([])}}/>
          <div className="relative w-full max-w-md bg-white shadow-2xl overflow-y-auto animate-in slide-in-from-right duration-200">
            <div className="sticky top-0 bg-white border-b border-slate-100 px-5 py-3 flex items-center justify-between z-10">
              <div><h3 className="text-sm font-bold text-slate-900">{custProfile.name||'Customer'}</h3><p className="text-[11px] text-slate-400">{custProfile.phone||custProfile.email||''}</p></div>
              <button onClick={()=>{setCustProfile(null);setCustOrders([])}} className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400 text-lg">&times;</button>
            </div>
            <div className="p-5 space-y-4">
              {custLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto"/> : <>
                <div className="grid grid-cols-2 gap-3">
                  {[{k:'Total Orders',v:custProfile.totalOrders||custOrders.length},{k:'Lifetime Value',v:'₹'+fmt(custProfile.lifetimeValue||0)},{k:'Email',v:custProfile.email||'—'},{k:'Phone',v:custProfile.phone||'—'}].map(f=><div key={f.k}><p className="text-[10px] font-medium text-slate-400 uppercase">{f.k}</p><p className="text-xs font-semibold text-slate-800 mt-0.5">{f.v}</p></div>)}
                </div>
                <div><p className="text-[10px] font-medium text-slate-400 uppercase mb-2">Orders</p>
                  <div className="space-y-1.5">
                    {custOrders.length===0 ? <p className="text-xs text-slate-400">No orders found</p> :
                      custOrders.map((co:any)=><div key={co.id} className="flex items-center justify-between p-2 rounded-lg bg-slate-50 text-xs">
                        <div><span className="font-mono font-semibold text-admin-600">#{co.orderNumber?.replace('ID-','')}</span><span className="text-slate-400 ml-2">{co.service?.name||''}</span></div>
                        <div className="flex items-center gap-2"><span className="font-semibold">₹{fmt(co.total||co.amount||0)}</span><span className={`px-1.5 py-0.5 rounded-full text-[9px] font-semibold ${payColor(co.paymentStatus)}`}>{label(co.paymentStatus)}</span></div>
                      </div>)}
                  </div>
                </div>
              </>}
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
}
