import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, MoreVertical, FileText, CheckCircle2, Clock, Check, Download, AlertCircle, RefreshCw, LogIn, Mail, Lock, X } from 'lucide-react';

const API_BASE = '';

export default function AdminDashboard() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [token, setToken] = useState(() => localStorage.getItem('instadeed_admin_token') || '');
  const [showLogin, setShowLogin] = useState(false);
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [loginError, setLoginError] = useState('');

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await fetch(`${API_BASE}/orders`, { headers });
      if (res.ok) {
        const data = await res.json();
        setOrders(Array.isArray(data) ? data : []);
      } else {
        setShowLogin(true);
      }
    } catch {
      setShowLogin(true);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (token) {
      fetchOrders();
    } else {
      setShowLogin(true);
      setLoading(false);
    }
  }, [token]);

  const handleSendOtp = async () => {
    setLoginError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/send-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        setOtpSent(true);
      } else {
        setLoginError('Email not found. Use an admin account.');
      }
    } catch {
      setLoginError('Network error. Try again.');
    }
  };

  const handleVerifyOtp = async () => {
    setLoginError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/verify-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp }),
      });
      const data = await res.json();
      if (data.access_token) {
        localStorage.setItem('instadeed_admin_token', data.access_token);
        setToken(data.access_token);
        setShowLogin(false);
      } else {
        setLoginError('Invalid OTP. Try again.');
      }
    } catch {
      setLoginError('Network error. Try again.');
    }
  };

  const updateStatus = async (id, newStatus) => {
    if (!token) return;
    try {
      await fetch(`${API_BASE}/orders/${id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ status: newStatus }),
      });
      setOrders(orders.map(o => o.id === id ? { ...o, status: newStatus } : o));
    } catch {}
  };

  const filteredOrders = orders.filter(order => {
    const matchesFilter = filter === 'all' || order.status === filter;
    if (!searchQuery) return matchesFilter;
    const q = searchQuery.toLowerCase();
    return matchesFilter && (
      (order.id || '').toLowerCase().includes(q) ||
      (order.customer_name || order.customer_email || '').toLowerCase().includes(q) ||
      (order.agreement_type || '').toLowerCase().includes(q)
    );
  });

  function statusBadge(status) {
    const config = {
      pending: { bg: 'bg-amber-100', text: 'text-amber-800', icon: Clock },
      PENDING_PAYMENT: { bg: 'bg-amber-100', text: 'text-amber-800', icon: Clock },
      processing: { bg: 'bg-blue-100', text: 'text-blue-800', icon: AlertCircle },
      PAID: { bg: 'bg-blue-100', text: 'text-blue-800', icon: AlertCircle },
      completed: { bg: 'bg-emerald-100', text: 'text-emerald-800', icon: CheckCircle2 },
      COMPLETED: { bg: 'bg-emerald-100', text: 'text-emerald-800', icon: CheckCircle2 },
      DRAFTED: { bg: 'bg-indigo-100', text: 'text-indigo-800', icon: FileText },
      SIGNED: { bg: 'bg-purple-100', text: 'text-purple-800', icon: CheckCircle2 },
    };
    const c = config[status?.toLowerCase()] || config.pending;
    const Icon = c.icon;
    return <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold ${c.bg} ${c.text}`}><Icon size={12} /> {status}</span>;
  }

  if (showLogin) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl shadow-xl border border-slate-100 p-8 w-full max-w-md">
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Lock className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-2xl font-black text-slate-900">Admin Login</h2>
            <p className="text-slate-500 mt-1">Verify your admin email to continue</p>
          </div>
          {!otpSent ? (
            <>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Admin Email</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="admin@example.com" className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none mb-4" />
              {loginError && <p className="text-red-500 text-sm mb-3">{loginError}</p>}
              <button onClick={handleSendOtp} disabled={!email} className="w-full py-3 bg-slate-900 hover:bg-black text-white rounded-xl font-semibold disabled:opacity-50 transition-all">
                <Mail size={16} className="inline mr-2" />Send OTP
              </button>
            </>
          ) : (
            <>
              <p className="text-sm text-slate-500 mb-4">OTP sent to <strong>{email}</strong></p>
              <input type="text" value={otp} onChange={e => setOtp(e.target.value)} placeholder="Enter 6-digit OTP" maxLength={6} className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none mb-4 text-center text-2xl tracking-widest" />
              {loginError && <p className="text-red-500 text-sm mb-3">{loginError}</p>}
              <button onClick={handleVerifyOtp} disabled={otp.length !== 6} className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold disabled:opacity-50 transition-all">
                <LogIn size={16} className="inline mr-2" />Verify & Login
              </button>
              <button onClick={() => { setOtpSent(false); setOtp(''); setLoginError(''); }} className="w-full mt-3 py-2 text-sm text-slate-500 hover:text-slate-700">
                Change email
              </button>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 font-sans text-slate-800">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-slate-900">Admin Fulfillment Queue</h1>
            <p className="text-slate-500 mt-1">Manage and process incoming document drafting requests.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative flex-1 md:flex-initial">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
              <input 
                type="text" 
                placeholder="Search orders..." 
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm w-full md:w-64"
              />
            </div>
            <button onClick={fetchOrders} className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors" title="Refresh">
              <RefreshCw size={16} /> Refresh
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
            <div className="text-slate-500 text-sm font-medium mb-1">Total Orders</div>
            <div className="text-3xl font-black text-slate-800">{orders.length}</div>
          </div>
          <div className="bg-amber-50 p-6 rounded-2xl border border-amber-100 shadow-sm">
            <div className="text-amber-700 text-sm font-medium mb-1">Pending</div>
            <div className="text-3xl font-black text-amber-900">{orders.filter(o => o.status === 'PENDING_PAYMENT' || o.status === 'pending').length}</div>
          </div>
          <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100 shadow-sm">
            <div className="text-blue-700 text-sm font-medium mb-1">Paid / In Progress</div>
            <div className="text-3xl font-black text-blue-900">{orders.filter(o => o.status === 'PAID' || o.status === 'processing' || o.status === 'DRAFTED').length}</div>
          </div>
          <div className="bg-emerald-50 p-6 rounded-2xl border border-emerald-100 shadow-sm">
            <div className="text-emerald-700 text-sm font-medium mb-1">Completed</div>
            <div className="text-3xl font-black text-emerald-900">{orders.filter(o => o.status === 'COMPLETED' || o.status === 'SIGNED' || o.status === 'completed').length}</div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-6 border-b border-slate-200 mb-6 overflow-x-auto">
          {[
            { key: 'all', label: 'All' },
            { key: 'PENDING_PAYMENT', label: 'Pending' },
            { key: 'PAID', label: 'Paid' },
            { key: 'DRAFTED', label: 'Drafted' },
            { key: 'COMPLETED', label: 'Completed' },
            { key: 'SIGNED', label: 'Signed' },
          ].map((tab) => (
            <button 
              key={tab.key}
              onClick={() => setFilter(tab.key)}
              className={`pb-3 text-sm font-medium transition-colors relative whitespace-nowrap ${
                filter === tab.key ? 'text-blue-600' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {tab.label}
              {filter === tab.key && (
                <motion.div layoutId="activeTab" className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
              )}
            </button>
          ))}
        </div>

        {/* Orders Table */}
        <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden flex flex-col">
          {loading ? (
            <div className="text-center py-12 text-slate-400">
              <RefreshCw size={24} className="animate-spin mx-auto mb-3" />
              Loading orders...
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider font-semibold border-b border-slate-100">
                    <th className="px-6 py-4">Order ID & Date</th>
                    <th className="px-6 py-4">Document Type</th>
                    <th className="px-6 py-4">Customer</th>
                    <th className="px-6 py-4">Amount</th>
                    <th className="px-6 py-4">Status</th>
                    <th className="px-6 py-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredOrders.map((order) => (
                    <motion.tr 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      key={order.id} 
                      className="hover:bg-slate-50 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <div className="font-mono font-medium text-slate-800 text-sm">{order.id?.slice(0, 20)}</div>
                        <div className="text-xs text-slate-500 mt-1">{new Date(order.created_at || order.date).toLocaleString()}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <FileText size={16} className="text-blue-500" />
                          <span className="font-medium text-slate-700">{order.agreement_type || order.type || 'Document'}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm font-medium text-slate-700">{order.customer_name || 'Unknown'}</div>
                        <div className="text-xs text-slate-500">{order.customer_email || order.customer_phone || ''}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm font-semibold text-slate-700">₹{order.amount || 0}</div>
                      </td>
                      <td className="px-6 py-4">
                        {statusBadge(order.status)}
                      </td>
                      <td className="px-6 py-4 text-right">
                        {(order.status === 'PENDING_PAYMENT' || order.status === 'pending') && (
                          <div className="flex items-center justify-end gap-2">
                            <button onClick={() => updateStatus(order.id, 'PAID')} className="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold rounded-lg transition-colors">
                              Mark Paid
                            </button>
                          </div>
                        )}
                        {(order.status === 'PAID' || order.status === 'processing') && (
                          <div className="flex items-center justify-end gap-2">
                            <button onClick={() => updateStatus(order.id, 'DRAFTED')} className="px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold rounded-lg transition-colors">
                              Start Draft
                            </button>
                            <button onClick={() => updateStatus(order.id, 'COMPLETED')} className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                              <Check size={14} /> Fulfill
                            </button>
                          </div>
                        )}
                        {order.status === 'DRAFTED' && (
                          <div className="flex items-center justify-end gap-2">
                            <button onClick={() => updateStatus(order.id, 'SIGNED')} className="px-3 py-1.5 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                              <Check size={14} /> Mark Signed
                            </button>
                            <button onClick={() => updateStatus(order.id, 'COMPLETED')} className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                              <Check size={14} /> Fulfill
                            </button>
                          </div>
                        )}
                        {(order.status === 'COMPLETED' || order.status === 'SIGNED' || order.status === 'completed') && (
                          <button className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors" title="View details">
                            <MoreVertical size={16} />
                          </button>
                        )}
                      </td>
                    </motion.tr>
                  ))}
                  {filteredOrders.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                        No orders found. {!token && 'Login to view real orders.'}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
