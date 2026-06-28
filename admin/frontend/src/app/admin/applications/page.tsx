'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet } from '@/lib/api';
import { FileText, Download, Eye, Printer, Loader2, ChevronDown, ChevronRight } from 'lucide-react';

interface AppDoc {
  id: string;
  applicationId: string;
  documentType: string;
  fileName: string;
  fileUrl: string;
  mimeType: string;
  size: number;
  uploadedAt: string;
}

const DOC_LABELS: Record<string, string> = {
  'sale-deed': 'Registered Sale Deed',
  'aadhaar': 'Aadhaar Card',
  'pan': 'PAN Card',
  'sanctioned-letter': 'Sanctioned Letter',
  'bank-noc': 'Bank NOC',
  'application-form': 'Application Form',
  'bank-request': 'Request Letter from Bank',
  'tm-form': 'T.M. Application Form',
  'noc-builder': 'NOC from Builder',
  'no-dues': 'No Dues Certificate',
  'mortgage-noc': 'Mortgage N.O.C',
  'challan': 'Challan Copy',
  'affidavit': 'Affidavit',
  'id-proof': 'ID & Address Proof',
  'occupancy': 'Occupancy Certificate',
};

export default function ApplicationDocumentsPage() {
  const [groups, setGroups] = useState<{ appId: string; docs: AppDoc[] }[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  useEffect(() => { fetchDocs(); }, []);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { grouped: Record<string, AppDoc[]>; total: number } }>('/admin/applications/documents');
      if (res.data?.grouped) {
        const g = Object.entries(res.data.grouped).map(([appId, docs]) => ({ appId, docs: docs as AppDoc[] }));
        g.sort((a, b) => new Date(b.docs[0].uploadedAt).getTime() - new Date(a.docs[0].uploadedAt).getTime());
        setGroups(g);
      }
    } catch {} finally { setLoading(false); }
  };

  const toggleExpand = (appId: string) => {
    setExpanded(prev => ({ ...prev, [appId]: !prev[appId] }));
  };

  const handlePrint = (appId: string) => {
    window.open(`/admin/applications/documents/print?appId=${appId}`, '_blank');
  };

  if (loading) {
    return <AdminLayout title="Application Documents"><div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin" /></div></AdminLayout>;
  }

  return (
    <AdminLayout title="Application Documents">
      <p className="text-sm text-slate-500 mb-6">View, download, and print documents uploaded by customers for each application.</p>

      {groups.length === 0 ? (
        <div className="card p-8 text-center">
          <FileText className="w-10 h-10 text-slate-300 mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-600">No documents uploaded yet</p>
          <p className="text-xs text-slate-400 mt-1">Customer documents will appear here after upload.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {groups.map(({ appId, docs }) => {
            const isExpanded = expanded[appId];
            return (
              <div key={appId} className="card overflow-hidden">
                <button onClick={() => toggleExpand(appId)} className="w-full flex items-center justify-between p-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-center gap-3">
                    {isExpanded ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
                    <div className="text-left">
                      <span className="font-medium text-slate-900 text-sm">{appId}</span>
                      <span className="text-xs text-slate-400 ml-2">{docs.length} documents</span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={(e) => { e.stopPropagation(); handlePrint(appId); }} className="btn-secondary btn-sm"><Printer className="w-3 h-3" /> Print All</button>
                  </div>
                </button>

                {isExpanded && (
                  <div className="border-t border-slate-200">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-slate-50 text-left text-xs font-semibold text-slate-500 uppercase">
                          <th className="px-4 py-2">Document Type</th>
                          <th className="px-4 py-2">File Name</th>
                          <th className="px-4 py-2">Size</th>
                          <th className="px-4 py-2">Uploaded</th>
                          <th className="px-4 py-2">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {docs.map(doc => (
                          <tr key={doc.id} className="border-t border-slate-100 hover:bg-slate-50">
                            <td className="px-4 py-3 font-medium text-slate-900">{DOC_LABELS[doc.documentType] || doc.documentType}</td>
                            <td className="px-4 py-3 text-slate-600">{doc.fileName}</td>
                            <td className="px-4 py-3 text-slate-400">{(doc.size / 1024).toFixed(0)} KB</td>
                            <td className="px-4 py-3 text-slate-400">{new Date(doc.uploadedAt).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}</td>
                            <td className="px-4 py-3">
                              <div className="flex gap-1.5">
                                <a href={`/api/applications/documents/${doc.id}/file`} download className="btn-secondary btn-sm"><Download className="w-3 h-3" /></a>
                                <a href={`/api/applications/documents/${doc.id}/file`} target="_blank" className="btn-ghost btn-sm"><Eye className="w-3 h-3" /></a>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </AdminLayout>
  );
}
