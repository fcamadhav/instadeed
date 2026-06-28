'use client';

import { useState } from 'react';
import { apiPost } from '@/lib/api';
import toast from 'react-hot-toast';
import { Shield, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

export default function BackupSection() {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string; files?: string[] } | null>(null);

  const runBackup = async () => {
    setRunning(true);
    setResult(null);
    try {
      const res = await apiPost<{ data: { message: string; files: string[] } }>('/admin/backup/run');
      if (res?.data) {
        setResult({ success: true, message: res.data.message, files: res.data.files });
        toast.success('Backup completed');
      }
    } catch (err: any) {
      setResult({ success: false, message: err.message });
      toast.error(err.message);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div>
      <button
        onClick={runBackup}
        disabled={running}
        className="btn-primary inline-flex items-center gap-2"
      >
        {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Shield className="w-4 h-4" />}
        {running ? 'Running Backup...' : 'Run Backup Now'}
      </button>

      {result && (
        <div className={`mt-4 p-4 rounded-xl border text-sm ${result.success ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-red-50 border-red-200 text-red-700'}`}>
          <div className="flex items-center gap-2 font-semibold mb-1">
            {result.success ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
            {result.success ? 'Backup Completed' : 'Backup Failed'}
          </div>
          <p className="opacity-80">{result.message}</p>
          {result.files && result.files.length > 0 && (
            <ul className="mt-2 space-y-0.5 text-xs opacity-70">
              {result.files.map(f => <li key={f}>• {f}</li>)}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
