import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, ArrowRight, Eye, Edit3, ShieldAlert } from 'lucide-react';

export default function DocumentForm({ documentType, initialData, onSubmit, onBack }) {
  const [formData, setFormData] = useState(initialData || {});
  const [errors, setErrors] = useState({});
  const [showPreview, setShowPreview] = useState(window.innerWidth > 1024);

  const docName = documentType?.title || 'Document';

  // Basic inline validation
  const validate = (field, value) => {
    if (!value || value.trim() === '') {
      setErrors(prev => ({ ...prev, [field]: 'This field is required' }));
      return false;
    }
    setErrors(prev => ({ ...prev, [field]: null }));
    return true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    validate(name, value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate all fields (mock for now, normally would loop through required fields)
    const party1Valid = validate('party1', formData.party1);
    const party2Valid = validate('party2', formData.party2);
    
    if (party1Valid && party2Valid) {
      onSubmit(formData);
    }
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-100">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500">
            <ChevronLeft size={24} />
          </button>
          <div>
            <h2 className="text-2xl font-bold text-slate-800">{docName} Details</h2>
            <p className="text-sm text-slate-500">Fill in the specific details for your document</p>
          </div>
        </div>
        
        {/* Mobile preview toggle */}
        <button 
          className="lg:hidden flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors"
          onClick={() => setShowPreview(!showPreview)}
        >
          {showPreview ? <Edit3 size={18} /> : <Eye size={18} />}
          {showPreview ? 'Edit Form' : 'Live Preview'}
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-8 flex-grow">
        {/* Form Column */}
        <div className={`flex-1 flex flex-col ${showPreview ? 'hidden lg:flex' : 'flex'}`}>
          <form id="document-form" onSubmit={handleSubmit} className="space-y-6 flex-grow">
            
            <div className="space-y-1">
              <label className="text-sm font-semibold text-slate-700 flex justify-between">
                First Party Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="party1"
                value={formData.party1 || ''}
                onChange={handleChange}
                onBlur={(e) => validate('party1', e.target.value)}
                placeholder="e.g. John Doe / Company Ltd"
                className={`w-full px-4 py-3 rounded-xl border ${errors.party1 ? 'border-red-500 focus:ring-red-200' : 'border-slate-200 focus:ring-blue-100'} bg-slate-50 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 transition-all`}
              />
              {errors.party1 && (
                <motion.p initial={{opacity:0, height:0}} animate={{opacity:1, height:'auto'}} className="text-red-500 text-xs mt-1 flex items-center gap-1">
                  <ShieldAlert size={12} /> {errors.party1}
                </motion.p>
              )}
            </div>

            <div className="space-y-1">
              <label className="text-sm font-semibold text-slate-700 flex justify-between">
                Second Party Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="party2"
                value={formData.party2 || ''}
                onChange={handleChange}
                onBlur={(e) => validate('party2', e.target.value)}
                placeholder="e.g. Jane Smith / Another Co"
                className={`w-full px-4 py-3 rounded-xl border ${errors.party2 ? 'border-red-500 focus:ring-red-200' : 'border-slate-200 focus:ring-blue-100'} bg-slate-50 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 transition-all`}
              />
              {errors.party2 && (
                <motion.p initial={{opacity:0, height:0}} animate={{opacity:1, height:'auto'}} className="text-red-500 text-xs mt-1 flex items-center gap-1">
                  <ShieldAlert size={12} /> {errors.party2}
                </motion.p>
              )}
            </div>
            
            <div className="space-y-1">
              <label className="text-sm font-semibold text-slate-700">
                Additional Terms (Optional)
              </label>
              <textarea
                name="terms"
                value={formData.terms || ''}
                onChange={handleChange}
                placeholder="Any specific clauses..."
                rows={4}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all resize-none"
              ></textarea>
            </div>
            
          </form>
          
          <div className="pt-6 mt-6 border-t border-slate-100">
            <button 
              onClick={handleSubmit}
              className="w-full py-4 bg-slate-900 hover:bg-black text-white rounded-xl font-semibold flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-slate-900/20"
            >
              Continue to Verification <ArrowRight size={18} />
            </button>
          </div>
        </div>

        {/* Live Preview Column */}
        <div className={`flex-1 bg-slate-50 rounded-2xl border border-slate-200 p-6 flex flex-col relative overflow-hidden ${!showPreview ? 'hidden lg:flex' : 'flex'}`}>
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-400 to-indigo-500"></div>
          
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2 text-blue-600 font-medium text-sm">
              <Eye size={16} /> Live Preview
            </div>
            <div className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded uppercase tracking-wider">
              Draft
            </div>
          </div>
          
          <div className="bg-white rounded-xl border border-slate-100 p-6 md:p-8 flex-grow shadow-sm flex flex-col relative">
            <div className="absolute inset-0 pointer-events-none" style={{ backgroundImage: 'radial-gradient(#e2e8f0 1px, transparent 1px)', backgroundSize: '20px 20px', opacity: 0.3 }}></div>
            
            <h1 className="text-center font-bold text-xl uppercase mb-8 border-b-2 border-slate-800 pb-2 inline-block mx-auto text-slate-800">
              {docName.toUpperCase()}
            </h1>
            
            <div className="space-y-6 text-slate-700 text-sm leading-relaxed font-serif">
              <p>
                This agreement is made and entered into on <strong>{new Date().toLocaleDateString()}</strong>, by and between:
              </p>
              
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded text-yellow-900 transition-all duration-300">
                <strong className="block text-xs uppercase text-yellow-600 mb-1">Party 1</strong>
                {formData.party1 || <span className="italic text-yellow-500 opacity-50">[First Party Name will appear here]</span>}
              </div>
              
              <p className="text-center italic">AND</p>
              
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded text-yellow-900 transition-all duration-300">
                <strong className="block text-xs uppercase text-yellow-600 mb-1">Party 2</strong>
                {formData.party2 || <span className="italic text-yellow-500 opacity-50">[Second Party Name will appear here]</span>}
              </div>
              
              <p>
                The parties agree to the standard terms and conditions outlined in the full {docName.toLowerCase()}.
              </p>
              
              {formData.terms && (
                <div className="mt-4 pt-4 border-t border-slate-100">
                  <strong className="block mb-2">Special Terms:</strong>
                  <p className="whitespace-pre-wrap text-slate-600 bg-slate-50 p-3 rounded">{formData.terms}</p>
                </div>
              )}
            </div>
            
            <div className="mt-auto pt-10 flex justify-between">
              <div className="w-32 border-t border-slate-400 pt-2 text-center text-xs text-slate-500 font-serif">Signature (Party 1)</div>
              <div className="w-32 border-t border-slate-400 pt-2 text-center text-xs text-slate-500 font-serif">Signature (Party 2)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
