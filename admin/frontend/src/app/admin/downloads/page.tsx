'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet } from '@/lib/api';
import { Download, FileText, Image, Loader2, ExternalLink } from 'lucide-react';

interface GenDoc { id: string; documentNumber: string; documentType: string; pdfFilePath: string | null; status: string; createdAt: string; customer?: { name: string }; service?: { name: string }; }
interface AppDoc { id: string; applicationId: string; documentType: string; fileName: string; size: number; uploadedAt: string; }

const DOC_NAMES: Record<string,string> = {'sale-deed':'Sale Deed','aadhaar':'Aadhaar','pan':'PAN','sanctioned-letter':'Sanctioned Letter','bank-noc':'Bank NOC','application-form':'Application Form','bank-request':'Bank Request','tm-form':'TM Application','noc-builder':'Builder NOC','no-dues':'No Dues','mortgage-noc':'Mortgage NOC','challan':'Fee Challan','affidavit':'Affidavit','id-proof':'ID Proof','occupancy':'Occupancy Certificate'};

export default function DownloadsPage() {
  const [genDocs, setGenDocs] = useState<GenDoc[]>([]);
  const [appDocs, setAppDocs] = useState<AppDoc[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiGet<{ data: { documents: GenDoc[] } }>('/admin/documents?limit=200').catch(() => null),
      apiGet<{ data: { documents: AppDoc[]; total: number } }>('/admin/applications/documents').catch(() => null),
    ]).then(([gd, ad]) => {
      if (gd?.data?.documents) setGenDocs(gd.data.documents);
      if (ad?.data?.documents) setAppDocs(ad.data.documents);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return <AdminLayout title="Downloads Center"><Loader2 className="w-6 h-6 animate-spin mx-auto mt-20" /></AdminLayout>;

  return (
    <AdminLayout title="Downloads Center">
      <p className="text-sm text-slate-500 mb-6">All generated documents and customer uploads — download or open in new tab.</p>

      {/* Generated PDFs */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">Generated Documents ({genDocs.length})</h3>
        {genDocs.length === 0 ? (
          <div className="card p-6 text-center text-sm text-slate-400">No PDFs generated yet. They appear automatically after payment.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {genDocs.map(d => (
              <div key={d.id} className="card p-4 flex items-center gap-3 group hover:border-admin-200 transition-colors">
                <FileText className="w-8 h-8 text-admin-600 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900 truncate">{d.documentNumber}</p>
                  <p className="text-xs text-slate-400">{d.documentType} • {new Date(d.createdAt).toLocaleDateString('en-IN')}</p>
                </div>
                <div className="flex gap-1.5 flex-shrink-0">
                  <a href={`/api/admin/documents/${d.id}/download/pdf`} download className="btn-primary btn-sm p-1.5"><Download className="w-3.5 h-3.5" /></a>
                  <a href={`/api/admin/documents/${d.id}/download/pdf`} target="_blank" className="btn-ghost btn-sm p-1.5"><ExternalLink className="w-3.5 h-3.5" /></a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Customer Uploads */}
      <div>
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3">Customer Uploaded Documents ({appDocs.length})</h3>
        {appDocs.length === 0 ? (
          <div className="card p-6 text-center text-sm text-slate-400">No customer documents uploaded yet.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {appDocs.map(d => (
              <div key={d.id} className="card p-4 flex items-center gap-3 group hover:border-admin-200 transition-colors">
                <Image className="w-8 h-8 text-amber-500 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900 truncate">{DOC_NAMES[d.documentType] || d.documentType}</p>
                  <p className="text-xs text-slate-400">{d.fileName} • {(d.size/1024).toFixed(0)} KB • {new Date(d.uploadedAt).toLocaleDateString('en-IN')}</p>
                </div>
                <a href={`/api/applications/documents/${d.id}/file`} download className="btn-primary btn-sm p-1.5 flex-shrink-0"><Download className="w-3.5 h-3.5" /></a>
              </div>
            ))}
          </div>
        )}
      </div>
    </AdminLayout>
  );
}
