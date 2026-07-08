import React, { useState } from 'react';
import { ChevronLeft, ShieldCheck, CreditCard, Landmark, Lock, ArrowRight, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

const API_BASE = '';

export default function Checkout({ documentType, formData, userProfile, onSuccess, onBack }) {
  const [method, setMethod] = useState('upi');
  const [processing, setProcessing] = useState(false);
  const [orderCreated, setOrderCreated] = useState(false);
  const [error, setError] = useState('');

  const price = documentType?.price || 499;
  const tax = Math.round(price * 0.18);
  const total = price + tax;

  const handlePayment = async () => {
    setProcessing(true);
    setError('');

    try {
      const res = await fetch(`${API_BASE}/create-offline-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name: formData?.documentDetails?.party1Name || userProfile?.name || 'Customer',
          customer_phone: userProfile?.phone || '',
          customer_email: userProfile?.email || '',
          agreement_type: documentType?.type || documentType?.slug || 'RENT',
          amount: total,
          status: 'PAID',
          form_data: formData?.documentDetails || {},
        }),
      });

      const data = await res.json();
      if (data.status === 'success') {
        setOrderCreated(true);
        setTimeout(() => {
          onSuccess({
            transactionId: data.order_id,
            amount: total,
            method: method,
            date: new Date().toISOString(),
            type: documentType?.title || 'Legal Document',
          });
        }, 1500);
      } else {
        setError(data.detail || 'Order creation failed');
      }
    } catch {
      setError('Network error. Please try again.');
    }
    setProcessing(false);
  };

  if (orderCreated) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center px-6">
        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200, damping: 20 }}>
          <CheckCircle2 size={72} className="text-emerald-500 mx-auto mb-4" />
        </motion.div>
        <h2 className="text-2xl font-black text-slate-800 mb-2">Order Created!</h2>
        <p className="text-slate-500">Your document is being processed. Redirecting to confirmation...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-4 mb-8 pb-4 border-b border-slate-100">
        <button onClick={onBack} className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500" disabled={processing}>
          <ChevronLeft size={24} />
        </button>
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Checkout</h2>
          <p className="text-sm text-slate-500">Review and confirm your order</p>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8 flex-grow">
        <div className="flex-1 order-2 lg:order-1">
          <h3 className="text-lg font-bold text-slate-800 mb-4">Payment Method</h3>
          <div className="space-y-3">
            {[
              { id: 'upi', title: 'UPI (GPay, PhonePe, Paytm)', icon: <div className="font-bold text-blue-600">UPI</div> },
              { id: 'card', title: 'Credit / Debit Card', icon: <CreditCard size={20} className="text-slate-600" /> },
              { id: 'netbanking', title: 'Net Banking', icon: <Landmark size={20} className="text-slate-600" /> },
            ].map(option => (
              <label 
                key={option.id}
                className={`flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all ${
                  method === option.id 
                    ? 'border-blue-600 bg-blue-50/50 shadow-sm' 
                    : 'border-slate-100 hover:border-slate-200 bg-white'
                }`}
              >
                <input type="radio" name="paymentMethod" value={option.id} checked={method === option.id} onChange={() => setMethod(option.id)} className="w-4 h-4 text-blue-600 border-slate-300 focus:ring-blue-500" />
                <div className="ml-4 flex items-center justify-between w-full">
                  <span className={`font-semibold ${method === option.id ? 'text-blue-900' : 'text-slate-700'}`}>{option.title}</span>
                  <div className="w-10 h-6 flex items-center justify-center bg-white border border-slate-200 rounded">{option.icon}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        <div className="w-full lg:w-[350px] order-1 lg:order-2">
          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 sticky top-6">
            <h3 className="text-lg font-bold text-slate-800 mb-6">Order Summary</h3>
            <div className="space-y-4 text-sm">
              <div className="flex justify-between text-slate-600">
                <span>{documentType?.title || 'Legal Document'}</span>
                <span className="font-medium text-slate-800">₹{price}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>Platform Fee</span>
                <span className="font-medium text-slate-800">Free</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>GST (18%)</span>
                <span className="font-medium text-slate-800">₹{tax}</span>
              </div>
              <div className="pt-4 border-t border-slate-200 flex justify-between items-center">
                <span className="font-bold text-slate-800">Total Amount</span>
                <span className="text-2xl font-black text-blue-600">₹{total}</span>
              </div>
            </div>

            {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}

            <button 
              onClick={handlePayment}
              disabled={processing}
              className="w-full mt-8 py-4 bg-slate-900 hover:bg-black text-white rounded-xl font-semibold flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-slate-900/20 disabled:opacity-70 disabled:scale-100"
            >
              {processing ? (
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Creating Order...
                </div>
              ) : (
                <>Confirm Order <Lock size={16} /></>
              )}
            </button>
            <div className="flex items-center justify-center gap-1 mt-4 text-xs text-slate-400 font-medium">
              <ShieldCheck size={14} className="text-emerald-500" /> Secure & encrypted
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
