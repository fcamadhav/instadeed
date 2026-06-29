'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet, apiDownload } from '@/lib/api';
import { Download, FileText, Image, Loader2, Check } from 'lucide-react';

interface GenDoc { id: string; documentNumber: string; documentType: string; pdfFilePath: string | null; status: string; createdAt: string; customer?: { name: string }; service?: { name: string }; }
interface AppDoc { id: string; applicationId: string; documentType: string; fileName: string; size: number; uploadedAt: string; }

const DOC_NAMES: Record<string,string> = {'sale-deed':'Sale Deed','aadhaar':'Aadhaar','pan':'PAN','sanctioned-letter':'Sanctioned Letter','bank-noc':'Bank NOC','application-form':'Application Form','bank-request':'Bank Request','tm-form':'TM Application','noc-builder':'Builder NOC','no-dues':'No Dues','mortgage-noc':'Mortgage NOC','challan':'Fee Challan','affidavit':'Affidavit','id-proof':'ID Proof','occupancy':'Occupancy Certificate'};

export default function DownloadsPage() {
  const [genDocs, setGenDocs] = useState<GenDoc[]>([]);
  const [appDocs, setAppDocs] = useState<AppDoc[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState<string | null>(null);
  const [downloaded, setDownloaded] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      apiGet<{ data: { documents: GenDoc[] } }>('/admin/documents?limit=200').catch(() => null),
      apiGet<{ data: { documents: AppDoc[]; total: number } }>('/admin/applications/documents').catch(() => null),
    ]).then(([gd, ad]) => {
      if (gd?.data?.documents) setGenDocs(gd.data.documents);
      if (ad?.data?.documents) setAppDocs(ad.data.documents);
    }).finally(() => setLoading(false));
  }, []);

  async function downloadGenDoc(d: GenDoc) {
    setDownloading(d.id);
    try {
      await apiDownload(`/admin/documents/${d.id}/download/pdf`, `${d.documentNumber}.pdf`);
      setDownloaded(d.id);
      setTimeout(() => setDownloaded(null), 2000);
    } catch (err) {
      console.error('Download failed', err);
    } finally {
      setDownloading(null);
    }
  }

  async function downloadAppDoc(d: AppDoc) {
    setDownloading(d.id);
    try {
      await apiDownload(`/applications/documents/${d.id}/file`, d.fileName);
      setDownloaded(d.id);
      setTimeout(() => setDownloaded(null), 2000);
    } catch (err) {
      console.error('Download failed', err);
    } finally {
      setDownloading(null);
    }
  }

  if (loading) return <AdminLayout title="Downloads Center"><Loader2 className="w-6 h-6 animate-spin mx-auto mt-20" /></AdminLayout>;

  return (
    <AdminLayout title="Downloads Center">
      <p className="text-sm text-slate-500 mb-6">All generated documents and customer uploads — download or open in new tab.</p>

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
                <button
                  onClick={() => downloadGenDoc(d)}
                  disabled={downloading === d.id}
                  className="btn-primary btn-sm p-1.5 disabled:opacity-50"
                  title="Download PDF"
                >
                  {downloading === d.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> :
                   downloaded === d.id ? <Check className="w-3.5 h-3.5 text-green-400" /> :
                   <Download className="w-3.5 h-3.5" />}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

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
                <button
                  onClick={() => downloadAppDoc(d)}
                  disabled={downloading === d.id}
                  className="btn-primary btn-sm p-1.5 flex-shrink-0 disabled:opacity-50"
                  title="Download file"
                >
                  {downloading === d.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> :
                   downloaded === d.id ? <Check className="w-3.5 h-3.5 text-green-400" /> :
                   <Download className="w-3.5 h-3.5" />}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </AdminLayout>
  );
}
