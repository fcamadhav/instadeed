import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Download, Copy, ExternalLink, CalendarDays, FileText } from 'lucide-react';

export default function Confirmation({ data, onFinish }) {
  const transactionId = data?.paymentDetails?.transactionId || 'TXN123456789';
  const docTitle = data?.documentType?.title || 'Legal Document';

  const handleCopy = () => {
    navigator.clipboard.writeText(transactionId);
    // In a real app, show a toast notification here
  };

  return (
    <div className="flex flex-col items-center justify-center h-full max-w-2xl mx-auto text-center py-10">
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 200, damping: 20 }}
        className="w-24 h-24 bg-gradient-to-tr from-emerald-400 to-emerald-600 rounded-full flex items-center justify-center text-white shadow-xl shadow-emerald-500/30 mb-8"
      >
        <CheckCircle2 size={48} strokeWidth={2.5} />
      </motion.div>

      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h2 className="text-3xl font-black text-slate-800 mb-3 tracking-tight">Order Confirmed!</h2>
        <p className="text-slate-500 max-w-md mx-auto mb-10 text-lg">
          Your payment was successful and your {docTitle.toLowerCase()} is ready for download.
        </p>

        <div className="bg-slate-50 rounded-2xl border border-slate-200 p-6 md:p-8 w-full max-w-lg mb-8 shadow-sm">
          <div className="flex items-center gap-3 mb-6 pb-6 border-b border-slate-200">
            <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center">
              <FileText size={24} />
            </div>
            <div className="text-left flex-grow">
              <h4 className="font-bold text-slate-800">{docTitle}</h4>
              <div className="flex gap-4 text-xs text-slate-500 mt-1">
                <span className="flex items-center gap-1"><CalendarDays size={14} /> {new Date().toLocaleDateString()}</span>
                <span>PDF Format</span>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-500">Tracking ID</span>
              <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-slate-200 font-mono font-medium text-slate-700">
                {transactionId}
                <button onClick={handleCopy} className="text-slate-400 hover:text-blue-600 transition-colors">
                  <Copy size={14} />
                </button>
              </div>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-500">Status</span>
              <span className="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-bold uppercase tracking-wider">
                Processing in Admin Queue
              </span>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-600/30 active:scale-[0.98]">
            <Download size={20} /> Download Draft PDF
          </button>
          <button 
            onClick={onFinish}
            className="px-8 py-4 bg-white border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-[0.98]"
          >
            Go to Dashboard <ExternalLink size={20} />
          </button>
        </div>
      </motion.div>
    </div>
  );
}
