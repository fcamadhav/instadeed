'use client';

import { useState, useEffect, useCallback } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet, apiPost, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Upload, FileText, CheckCircle, X, Loader2, Shield, AlertCircle, ArrowRight } from 'lucide-react';

interface RequiredDoc { key: string; title: string; accept: string; required: boolean; maxSize: string; }
interface UploadedDoc { id: string; documentType: string; fileName: string; fileUrl: string; mimeType: string; size: number; uploadedAt: string; }

export default function ApplicationDocumentsPage() {
  const [requiredDocs, setRequiredDocs] = useState<RequiredDoc[]>([]);
  const [uploadedDocs, setUploadedDocs] = useState<UploadedDoc[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState<Record<string, boolean>>({});
  const [progress, setProgress] = useState<Record<string, number>>({});

  useEffect(() => { fetchRequiredDocs(); }, []);

  const fetchRequiredDocs = async () => {
    try {
      const res = await apiGet<{ data: RequiredDoc[] }>('/applications/documents/required/mutation');
      setRequiredDocs(res.data || []);
    } catch { setRequiredDocs([]); } finally { setLoading(false); }
  };

  const refreshUploaded = useCallback(async (appId: string) => {
    try {
      const res = await apiGet<{ data: UploadedDoc[] }>(`/applications/${appId}/documents`);
      setUploadedDocs(res.data || []);
    } catch {}
  }, []);

  const handleUpload = async (docType: string, file: File) => {
    setUploading(prev => ({ ...prev, [docType]: true }));
    setProgress(prev => ({ ...prev, [docType]: 0 }));

    const formData = new FormData();
    formData.append('file', file);
    formData.append('applicationId', 'mutation-app-1'); // TODO: real app ID
    formData.append('documentType', docType);

    try {
      await apiPost('/applications/documents/upload', formData);
      toast.success('Uploaded successfully');
      await refreshUploaded('mutation-app-1');
    } catch (err: any) {
      toast.error(err.message || 'Upload failed');
    } finally {
      setUploading(prev => ({ ...prev, [docType]: false }));
      setProgress(prev => ({ ...prev, [docType]: 0 }));
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiDelete(`/applications/documents/${id}`);
      toast.success('Document removed');
      await refreshUploaded('mutation-app-1');
    } catch { toast.error('Delete failed'); }
  };

  const getUploadedForType = (docType: string) => uploadedDocs.filter(d => d.documentType === docType);
  const allUploaded = requiredDocs.every(d => getUploadedForType(d.key).length > 0);

  if (loading) {
    return <AdminLayout title="Upload Documents"><div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin text-admin-600" /></div></AdminLayout>;
  }

  return (
    <AdminLayout title="Upload Required Documents">
      {/* Success Card */}
      <div className="card p-6 mb-6 border-l-4 border-l-green-500 bg-green-50/50 dark:bg-green-900/10">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0 mt-0.5">
            <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Your Mutation application has been received.</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">To start processing your application, please upload the following mandatory documents.</p>
          </div>
        </div>
      </div>

      {/* Upload Cards */}
      <div className="grid gap-4">
        {requiredDocs.map(doc => {
          const uploaded = getUploadedForType(doc.key);
          const isUploading = uploading[doc.key];
          const prog = progress[doc.key] || 0;
          const file = uploaded.length > 0 ? uploaded[0] : null;

          return (
            <div key={doc.key} className={`card p-6 ${file ? 'border-green-300 dark:border-green-700' : ''}`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-base font-semibold text-slate-900 dark:text-white">{doc.title}</h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Accept: {doc.accept.replace(/,/g, ', ').replace('application/', '.')} • Max: {doc.maxSize}
                    {doc.required && <span className="text-red-500 ml-1">* Required</span>}
                  </p>
                </div>
                {file && (
                  <span className="badge badge-green flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> Uploaded
                  </span>
                )}
              </div>

              {file ? (
                <div className="flex items-center justify-between bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-admin-600" />
                    <div>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">{file.fileName}</p>
                      <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(0)} KB • {new Date(file.uploadedAt).toLocaleDateString('en-IN')}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <label className="btn-secondary btn-sm cursor-pointer">
                      <Upload className="w-3 h-3" /> Replace
                      <input type="file" className="hidden" accept={doc.accept} onChange={e => { const f = e.target.files?.[0]; if (f) handleUpload(doc.key, f); }} />
                    </label>
                    <button onClick={() => handleDelete(file.id)} className="btn-ghost btn-sm text-red-500 hover:bg-red-50">
                      <X className="w-3 h-3" /> Remove
                    </button>
                  </div>
                </div>
              ) : isUploading ? (
                <div className="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4">
                  <div className="flex items-center gap-3 mb-2">
                    <Loader2 className="w-4 h-4 animate-spin text-admin-600" />
                    <span className="text-sm text-slate-600 dark:text-slate-400">Uploading...</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
                    <div className="bg-admin-600 h-1.5 rounded-full transition-all" style={{ width: `${prog}%` }} />
                  </div>
                </div>
              ) : (
                <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-xl p-8 cursor-pointer hover:border-admin-400 dark:hover:border-admin-600 transition-colors group">
                  <div className="w-12 h-12 rounded-full bg-admin-50 dark:bg-admin-900/30 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
                    <Upload className="w-5 h-5 text-admin-600 dark:text-admin-400" />
                  </div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Drag & drop or <span className="text-admin-600 dark:text-admin-400">Choose File</span></p>
                  <input type="file" className="hidden" accept={doc.accept} onChange={e => { const f = e.target.files?.[0]; if (f) handleUpload(doc.key, f); }} />
                </label>
              )}
            </div>
          );
        })}
      </div>

      {/* Continue Button */}
      <div className="mt-8 flex justify-end">
        <button
          disabled={!allUploaded}
          className={`btn-primary btn-lg ${!allUploaded ? 'opacity-50 cursor-not-allowed' : ''}`}
          onClick={() => toast.success('Documents uploaded! Redirecting to payment...')}
        >
          Continue to Payment
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </AdminLayout>
  );
}
