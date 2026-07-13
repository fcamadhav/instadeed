import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Home, Copyright, Building, Briefcase, FileSignature } from 'lucide-react';

const documentTypes = [
  { id: 'rent_agreement', title: 'Rent Agreement', icon: Home, description: 'Standard residential or commercial lease agreement', color: 'bg-blue-50 text-blue-600 border-blue-200' },
  { id: 'sale_deed', title: 'Sale Deed', icon: Building, description: 'Legal document for property ownership transfer', color: 'bg-indigo-50 text-indigo-600 border-indigo-200' },
  { id: 'trademark', title: 'Trademark', icon: Copyright, description: 'Brand and logo protection registration', color: 'bg-purple-50 text-purple-600 border-purple-200' },
  { id: 'nda', title: 'Non-Disclosure Agreement', icon: FileSignature, description: 'Protect your confidential business information', color: 'bg-emerald-50 text-emerald-600 border-emerald-200' },
  { id: 'employment', title: 'Employment Contract', icon: Briefcase, description: 'Standard hiring and employee agreement', color: 'bg-orange-50 text-orange-600 border-orange-200' },
  { id: 'other', title: 'Other Document', icon: FileText, description: 'Custom legal drafting services', color: 'bg-slate-50 text-slate-600 border-slate-200' },
];

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

export default function DocumentSelection({ onSelect, selected }) {
  return (
    <div className="flex flex-col h-full">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold text-slate-800 mb-3 tracking-tight">What do you need drafted?</h2>
        <p className="text-slate-500 max-w-lg mx-auto">Select the type of document you need. Our intelligent system will guide you through the process.</p>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {documentTypes.map((doc) => {
          const Icon = doc.icon;
          const isSelected = selected?.id === doc.id;
          
          return (
            <motion.div
              key={doc.id}
              variants={itemVariants}
              whileHover={{ scale: 1.03, translateY: -5 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onSelect(doc)}
              className={`cursor-pointer rounded-2xl p-6 border-2 transition-all duration-300 flex flex-col h-full ${
                isSelected 
                  ? 'border-blue-600 shadow-[0_10px_40px_-10px_rgba(37,99,235,0.3)] bg-blue-50/50' 
                  : 'border-slate-100 shadow-sm hover:shadow-md hover:border-slate-200 bg-white'
              }`}
            >
              <div className={`w-14 h-14 rounded-xl flex items-center justify-center mb-5 border ${doc.color}`}>
                <Icon size={28} strokeWidth={1.5} />
              </div>
              <h3 className="text-lg font-bold text-slate-800 mb-2">{doc.title}</h3>
              <p className="text-sm text-slate-500 leading-relaxed flex-grow">{doc.description}</p>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
}
