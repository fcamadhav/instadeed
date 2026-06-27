'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import {
  Download, FileText, FileSpreadsheet, Printer, Loader2,
  BarChart3, TrendingUp, ShoppingCart, Users, Tag, CreditCard, Package, ArrowUpDown
} from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, Legend
} from 'recharts';
import toast from 'react-hot-toast';

const reportTypes = [
  { value: 'revenue', label: 'Revenue', icon: TrendingUp },
  { value: 'orders', label: 'Orders', icon: ShoppingCart },
  { value: 'customers', label: 'Customers', icon: Users },
  { value: 'coupons', label: 'Coupons', icon: Tag },
  { value: 'payments', label: 'Payments', icon: CreditCard },
  { value: 'top_services', label: 'Top Services', icon: Package },
  { value: 'monthly_growth', label: 'Monthly Growth', icon: BarChart3 },
];

const mockRevenueData = Array.from({ length: 12 }, (_, i) => ({
  month: new Date(2025, i).toLocaleString('en-IN', { month: 'short' }),
  revenue: Math.floor(Math.random() * 500000 + 100000),
  orders: Math.floor(Math.random() * 200 + 50),
  customers: Math.floor(Math.random() * 100 + 20),
}));

const mockTopServices = [
  { name: 'Legal Notice Drafting', count: 142, revenue: 285000 },
  { name: 'Agreement Review', count: 98, revenue: 192000 },
  { name: 'Property Documentation', count: 67, revenue: 156000 },
  { name: 'Contract Drafting', count: 55, revenue: 134000 },
  { name: 'Legal Consultation', count: 120, revenue: 98000 },
];

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e', '#f97316'];

export default function ReportsPage() {
  const [reportType, setReportType] = useState('revenue');
  const [startDate, setStartDate] = useState(() => new Date(Date.now() - 30 * 86400000).toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any[]>([]);

  useEffect(() => { fetchReport(); }, [reportType, startDate, endDate]);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { report: any[] } }>(`/admin/reports/${reportType}?startDate=${startDate}&endDate=${endDate}`).catch(() => null);
      if (res?.data?.report) setData(res.data.report);
      else setData(reportType === 'top_services' ? mockTopServices : mockRevenueData);
    } catch { setData(reportType === 'top_services' ? mockTopServices : mockRevenueData); } finally { setLoading(false); }
  };

  const exportCSV = () => {
    toast.success('CSV export started (placeholder)');
  };
  const exportExcel = () => {
    toast.success('Excel export started (placeholder)');
  };
  const exportPDF = () => {
    toast.success('PDF export started (placeholder)');
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="card p-3 text-sm shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white mb-1">{label}</p>
          {payload.map((p: any, i: number) => (
            <p key={i} className="text-slate-600 dark:text-slate-400">
              {p.name}: <span className="font-medium">{p.name === 'Revenue' || p.name === 'revenue' ? '₹' : ''}{typeof p.value === 'number' ? p.value.toLocaleString('en-IN') : p.value}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const renderChart = () => {
    if (loading) return <div className="h-80 flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-admin-600" /></div>;

    if (reportType === 'top_services') {
      return (
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
            <YAxis type="category" dataKey="name" tick={{ fontSize: 11 }} stroke="#94a3b8" width={140} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="revenue" fill="#6366f1" radius={[0, 4, 4, 0]} name="Revenue" />
          </BarChart>
        </ResponsiveContainer>
      );
    }

    if (reportType === 'coupons' || reportType === 'payments') {
      return (
        <ResponsiveContainer width="100%" height={320}>
          <PieChart>
            <Pie data={data} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={120} label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
              {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      );
    }

    return (
      <ResponsiveContainer width="100%" height={320}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="cRev" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="month" tick={{ fontSize: 11 }} stroke="#94a3b8" />
          <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" />
          <Tooltip content={<CustomTooltip />} />
          <Area type="monotone" dataKey="revenue" stroke="#6366f1" fill="url(#cRev)" strokeWidth={2} name="Revenue" />
          <Line type="monotone" dataKey="orders" stroke="#f97316" strokeWidth={2} name="Orders" />
          <Line type="monotone" dataKey="customers" stroke="#22c55e" strokeWidth={2} name="Customers" />
          <Legend />
        </AreaChart>
      </ResponsiveContainer>
    );
  };

  const reportColumns: Column<any>[] = data.length > 0 ? Object.keys(data[0]).filter(k => k !== '_id').map(key => ({
    key,
    label: key.charAt(0).toUpperCase() + key.slice(1),
    render: (row: any) => {
      const val = row[key];
      if (typeof val === 'number') {
        return key.toLowerCase().includes('revenue') || key.toLowerCase().includes('amount') || key.toLowerCase().includes('spent')
          ? `₹${val.toLocaleString('en-IN')}` : val.toLocaleString('en-IN');
      }
      return val;
    },
  })) : [];

  return (
    <AdminLayout title="Reports">
      <div className="card p-4 mb-4">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="label text-xs">Report Type</label>
              <select value={reportType} onChange={e => setReportType(e.target.value)} className="select text-sm">
                {reportTypes.map(rt => <option key={rt.value} value={rt.value}>{rt.label}</option>)}
              </select>
            </div>
            <div>
              <label className="label text-xs">Start Date</label>
              <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="input text-sm" />
            </div>
            <div>
              <label className="label text-xs">End Date</label>
              <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="input text-sm" />
            </div>
          </div>
          <div className="flex items-end gap-2">
            <button onClick={exportPDF} className="btn-secondary btn-sm"><FileText className="w-3.5 h-3.5" /> PDF</button>
            <button onClick={exportExcel} className="btn-secondary btn-sm"><FileSpreadsheet className="w-3.5 h-3.5" /> Excel</button>
            <button onClick={exportCSV} className="btn-secondary btn-sm"><Download className="w-3.5 h-3.5" /> CSV</button>
          </div>
        </div>
      </div>

      <div className="card p-5 mb-6">
        <h3 className="section-title mb-4 capitalize">{reportType.replace('_', ' ')} Report</h3>
        {renderChart()}
      </div>

      <div>
        <h3 className="section-title mb-3">Data Table</h3>
        <DataTable columns={reportColumns} data={data} loading={loading} keyExtractor={(_, i) => String(i ?? 0)} emptyMessage="No data available" emptyDescription="Select a report type and date range to view data." />
      </div>
    </AdminLayout>
  );
}
