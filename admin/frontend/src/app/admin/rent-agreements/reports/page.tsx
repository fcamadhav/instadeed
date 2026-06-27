'use client';

import { useState } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import { apiGet } from '@/lib/api';
import { Download, BarChart3 } from 'lucide-react';
import toast from 'react-hot-toast';

export default function RentAgreementReportsPage() {
  const [reportType, setReportType] = useState('expiring-week');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const reportTypes = [
    { value: 'expiring-week', label: 'Expiring This Week' },
    { value: 'expiring-month', label: 'Expiring This Month' },
    { value: 'renewed-month', label: 'Renewed This Month' },
    { value: 'pending-renewals', label: 'Pending Renewals (Expired)' },
    { value: 'revenue-renewals', label: 'Revenue from Renewals' },
  ];

  const fetchReport = async () => {
    setLoading(true);
    try {
      const r = await apiGet<any>(`/admin/rent-agreements/reports?type=${reportType}`);
      setData(r.data);
    } catch (e: any) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  const exportCSV = () => {
    if (!data?.agreements?.length) { toast.error('No data to export'); return; }
    const headers = ['Agreement ID', 'Customer', 'Mobile', 'Landlord', 'Tenant', 'Property',
      'Start Date', 'End Date', 'Duration', 'Deposit', 'Monthly Rent', 'Payment', 'Status'];
    const rows = data.agreements.map((a: any) => [
      a.agreementId, a.customerName, a.mobile, a.landlordName, a.tenantName,
      `"${a.propertyAddress.replace(/"/g, '""')}"`,
      new Date(a.startDate).toLocaleDateString('en-IN'),
      new Date(a.endDate).toLocaleDateString('en-IN'),
      a.duration, a.securityDeposit, a.monthlyRent, a.paymentStatus, a.renewalStatus,
    ]);
    const csv = [headers.join(','), ...rows.map((r: string[]) => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `rent-agreements-${reportType}.csv`; a.click();
    URL.revokeObjectURL(url);
    toast.success('CSV exported');
  };

  const columns: Column<any>[] = [
    { key: 'agreementId', label: 'Agreement ID', render: (a) => <span className="font-mono text-xs">{a.agreementId}</span> },
    { key: 'customerName', label: 'Customer' },
    { key: 'mobile', label: 'Mobile' },
    { key: 'landlordName', label: 'Landlord' },
    { key: 'tenantName', label: 'Tenant' },
    { key: 'endDate', label: 'End Date', render: (a) => new Date(a.endDate).toLocaleDateString('en-IN') },
    { key: 'monthlyRent', label: 'Rent', render: (a) => `₹${a.monthlyRent?.toLocaleString('en-IN')}` },
    { key: 'renewalStatus', label: 'Status', render: (a) => <span className={`badge ${a.renewalStatus === 'RENEWED' ? 'badge-green' : 'badge-orange'}`}>{a.renewalStatus}</span> },
  ];

  return (
    <AdminLayout title="Rent Agreement Reports">
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Rent Agreement Reports</h1>

        <div className="card p-4">
          <div className="flex flex-wrap items-center gap-3">
            <select value={reportType} onChange={e => setReportType(e.target.value)} className="input py-2 text-sm w-auto">
              {reportTypes.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
            </select>
            <button onClick={fetchReport} className="btn-primary btn-sm">
              <BarChart3 className="w-4 h-4" /> Generate Report
            </button>
            {data && (
              <button onClick={exportCSV} className="btn-secondary btn-sm">
                <Download className="w-4 h-4" /> Export CSV
              </button>
            )}
          </div>
        </div>

        {data && (
          <>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="card p-4 border-l-4 border-l-blue-500">
                <div className="text-2xl font-bold text-slate-900 dark:text-white">{data.count || 0}</div>
                <div className="text-xs text-slate-500">Total Agreements</div>
              </div>
              {data.totalRevenue !== undefined && (
                <div className="card p-4 border-l-4 border-l-green-500">
                  <div className="text-2xl font-bold text-slate-900 dark:text-white">₹{(data.totalRevenue || 0).toLocaleString('en-IN')}</div>
                  <div className="text-xs text-slate-500">Total Revenue</div>
                </div>
              )}
            </div>

            <DataTable columns={columns} data={data.agreements || []} loading={loading}
              keyExtractor={(a) => a.id} emptyMessage="No agreements found for this report type." />
          </>
        )}
      </div>
    </AdminLayout>
  );
}
