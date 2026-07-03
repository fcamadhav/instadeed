'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import StatsCard from '@/components/StatsCard';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import {
  IndianRupee, ShoppingCart, Users, TrendingUp, Package, Clock,
  ArrowUpRight, ArrowDownRight, MoreHorizontal, Loader2, FileText,
  Home, AlertTriangle
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Area, AreaChart
} from 'recharts';

interface DashboardStats {
  todayRevenue: number;
  monthlyRevenue: number;
  totalOrders: number;
  activeCustomers: number;
  revenueTrend: number;
  ordersTrend: number;
  customersTrend: number;
}

interface Order {
  id: string;
  orderNumber: string;
  customer: { name: string; email: string };
  service: { name: string };
  amount: number;
  status: string;
  paymentStatus: string;
  createdAt: string;
}

interface Activity {
  id: string;
  action: string;
  user: string;
  module: string;
  timestamp: string;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [rentStats, setRentStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dashData, setDashData] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashRes, ordersRes, rentRes] = await Promise.all([
        apiGet<{ data: any }>('/admin/dashboard').catch(() => null),
        apiGet<{ data: { orders: Order[] } }>('/admin/orders?limit=10').catch(() => null),
        apiGet<{ data: any }>('/admin/rent-agreements/stats').catch(() => null),
      ]);
      if (dashRes?.data) {
        const d = dashRes.data;
        setDashData(d);
        setStats({
          todayRevenue: d.today?.revenue || 0,
          monthlyRevenue: d.monthly?.revenue || 0,
          totalOrders: d.totalOrders || 0,
          activeCustomers: d.customers?.active || 0,
          revenueTrend: 0,
          ordersTrend: 0,
          customersTrend: 0,
        });
        if (d.latestActivity) {
          setActivities(d.latestActivity.map((a: any) => ({
            id: a.id,
            action: a.action,
            user: a.user?.name || '',
            module: a.module,
            timestamp: a.createdAt,
          })));
        }
      }
      if (ordersRes?.data?.orders) setRecentOrders(ordersRes.data.orders);
      if (rentRes?.data) setRentStats(rentRes.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const orderColumns: Column<Order>[] = [
    { key: 'orderNumber', label: 'Order #', sortable: true },
    {
      key: 'customer', label: 'Customer',
      render: (o) => o.customer?.name || 'N/A',
    },
    {
      key: 'service', label: 'Service',
      render: (o) => o.service?.name || 'N/A',
    },
    {
      key: 'amount', label: 'Amount',
      render: (o) => `₹${(o.amount || 0).toLocaleString('en-IN')}`,
      sortable: true,
    },
    {
      key: 'status', label: 'Status',
      render: (o) => {
        const badges: Record<string, string> = {
          pending: 'badge-yellow', processing: 'badge-blue', completed: 'badge-green', cancelled: 'badge-red',
        };
        return <span className={badges[o.status] || 'badge-slate'}>{o.status}</span>;
      },
    },
    {
      key: 'createdAt', label: 'Date',
      render: (o) => new Date(o.createdAt).toLocaleDateString('en-IN'),
      sortable: true,
    },
  ];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="card p-3 text-sm shadow-lg">
          <p className="font-medium text-slate-900 dark:text-white mb-1">{label}</p>
          {payload.map((p: any, i: number) => (
            <p key={i} className="text-slate-600 dark:text-slate-400">
              {p.name}: <span className="font-medium">{p.name === 'Revenue' ? '₹' : ''}{p.value.toLocaleString('en-IN')}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <AdminLayout title="Dashboard">
      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-sm text-red-700 dark:text-red-400">
          {error}
          <button onClick={fetchDashboardData} className="ml-2 underline">Retry</button>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatsCard
          icon={IndianRupee}
          label="Today's Revenue"
          value={stats ? `₹${(stats.todayRevenue || 0).toLocaleString('en-IN')}` : '—'}
          trend={stats?.revenueTrend}
          accentColor="bg-emerald-500"
        />
        <StatsCard
          icon={TrendingUp}
          label="Monthly Revenue"
          value={stats ? `₹${(stats.monthlyRevenue || 0).toLocaleString('en-IN')}` : '—'}
          trend={8.2}
          accentColor="bg-admin-500"
        />
        <StatsCard
          icon={ShoppingCart}
          label="Total Orders"
          value={stats?.totalOrders?.toLocaleString() || '—'}
          trend={stats?.ordersTrend}
          accentColor="bg-violet-500"
        />
        <StatsCard
          icon={Users}
          label="Active Customers"
          value={stats?.activeCustomers?.toLocaleString() || '—'}
          trend={stats?.customersTrend}
          accentColor="bg-amber-500"
        />
      </div>

      {rentStats && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="section-title mb-0">
              <FileText className="w-4 h-4 inline mr-1" /> Rent Agreements
            </h3>
            <a href="/admin/rent-agreements" className="text-xs text-admin-600 hover:underline">View All →</a>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
            {[
              { label: 'Active', value: rentStats.totalActive, color: 'border-l-green-500' },
              { label: 'Expiring 90d', value: rentStats.expiring90, color: 'border-l-yellow-400' },
              { label: 'Expiring 60d', value: rentStats.expiring60, color: 'border-l-yellow-500' },
              { label: 'Expiring 30d', value: rentStats.expiring30, color: 'border-l-orange-400' },
              { label: 'Expiring 15d', value: rentStats.expiring15, color: 'border-l-orange-500' },
              { label: 'Expiring 7d', value: rentStats.expiring7, color: 'border-l-red-500' },
              { label: 'Expired', value: rentStats.expired, color: 'border-l-slate-400' },
              { label: 'Renewed/Mo', value: rentStats.renewedThisMonth, color: 'border-l-blue-500' },
            ].map(s => (
              <div key={s.label} className={`card p-3 border-l-4 ${s.color}`}>
                <div className="text-lg font-bold text-slate-900 dark:text-white">{s.value}</div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2 card p-5">
          <h3 className="section-title mb-4">Revenue Overview (30 days)</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              {dashData?.today?.revenue > 0 ? (
                <AreaChart data={[{ date: 'Today', revenue: dashData.today.revenue, orders: dashData.today.orders }]}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="#94a3b8" />
                  <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="revenue" stroke="#6366f1" fill="url(#revGrad)" strokeWidth={2} name="Revenue" />
                </AreaChart>
              ) : (
                <div className="h-full flex items-center justify-center text-sm text-slate-400">No revenue data available yet.</div>
              )}
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-5">
          <h3 className="section-title mb-4">Top Services</h3>
          {dashData?.topServices?.length > 0 ? (
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dashData.topServices} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
                  <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
                  <YAxis type="category" dataKey="name" tick={{ fontSize: 10 }} stroke="#94a3b8" width={100} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="revenue" fill="#6366f1" radius={[0, 4, 4, 0]} name="Revenue" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-72 flex items-center justify-center text-sm text-slate-400">No data available yet.</div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <h3 className="section-title mb-3">Recent Orders</h3>
          <DataTable
            columns={orderColumns}
            data={recentOrders}
            loading={loading}
            keyExtractor={(o) => o.id}
            emptyMessage="No orders yet"
            emptyDescription="Orders will appear here once customers start placing them."
          />
        </div>

        <div>
          <h3 className="section-title mb-3">Latest Activity</h3>
          <div className="card p-4 space-y-3">
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="flex items-start gap-3">
                  <div className="skeleton w-8 h-8 rounded-full" />
                  <div className="flex-1 space-y-1">
                    <div className="skeleton h-3 w-3/4" />
                    <div className="skeleton h-2 w-1/2" />
                  </div>
                </div>
              ))
            ) : activities.length === 0 ? (
              <div className="text-center py-6">
                <Clock className="w-8 h-8 text-slate-300 dark:text-slate-600 mx-auto mb-2" />
                <p className="text-sm text-slate-500 dark:text-slate-400">No recent activity</p>
              </div>
            ) : (
              activities.map((act) => (
                <div key={act.id} className="flex items-start gap-3 pb-3 border-b border-slate-100 dark:border-slate-700/50 last:border-0 last:pb-0">
                  <div className="w-8 h-8 rounded-full bg-admin-50 dark:bg-admin-900/30 flex items-center justify-center flex-shrink-0">
                    <Clock className="w-4 h-4 text-admin-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-700 dark:text-slate-300">
                      <span className="font-medium">{act.user}</span> {act.action}
                    </p>
                    <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">
                      {new Date(act.timestamp).toLocaleString('en-IN')}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}
