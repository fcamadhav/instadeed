import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import DocumentSelection from '../Steps/DocumentSelection';
import DocumentForm from '../Steps/DocumentForm';
import MobileVerification from '../Steps/MobileVerification';
import Checkout from '../Steps/Checkout';
import Confirmation from '../Steps/Confirmation';
import { CheckCircle2 } from 'lucide-react';

const steps = [
  { id: 1, title: 'Select Document' },
  { id: 2, title: 'Fill Details' },
  { id: 3, title: 'Verify Identity' },
  { id: 4, title: 'Checkout' },
  { id: 5, title: 'Confirmation' },
];

export default function DocumentWizard({ onViewAdmin }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    documentType: null,
    documentDetails: {},
    userProfile: null,
    paymentDetails: null,
  });

  const nextStep = () => setCurrentStep((prev) => Math.min(prev + 1, steps.length));
  const prevStep = () => setCurrentStep((prev) => Math.max(prev - 1, 1));
  const goToStep = (step) => setCurrentStep(step);

  const updateFormData = (key, data) => {
    setFormData((prev) => ({ ...prev, [key]: data }));
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <DocumentSelection 
          onSelect={(type) => { updateFormData('documentType', type); nextStep(); }} 
          selected={formData.documentType} 
        />;
      case 2:
        return <DocumentForm 
          documentType={formData.documentType}
          initialData={formData.documentDetails}
          onSubmit={(details) => { updateFormData('documentDetails', details); nextStep(); }}
          onBack={prevStep}
        />;
      case 3:
        return <MobileVerification 
          onVerified={(profile) => { updateFormData('userProfile', profile); nextStep(); }}
          onBack={prevStep}
        />;
      case 4:
        return <Checkout 
          documentType={formData.documentType}
          formData={formData}
          userProfile={formData.userProfile}
          onSuccess={(payment) => { updateFormData('paymentDetails', payment); nextStep(); }}
          onBack={prevStep}
        />;
      case 5:
        return <Confirmation 
          data={formData}
          onFinish={onViewAdmin ? () => onViewAdmin() : () => { /* reset */ }}
        />;
      default:
        return null;
    }
  };

  return (
    <div className="max-w-5xl mx-auto w-full px-4 py-8">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between relative">
          <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-slate-200 rounded-full z-0"></div>
          <div 
            className="absolute left-0 top-1/2 transform -translate-y-1/2 h-1 bg-blue-600 rounded-full z-0 transition-all duration-500 ease-in-out"
            style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
          ></div>
          
          {steps.map((step, idx) => {
            const isCompleted = step.id < currentStep;
            const isCurrent = step.id === currentStep;
            return (
              <div key={step.id} className="relative z-10 flex flex-col items-center">
                <div 
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                    isCompleted ? 'bg-blue-600 border-blue-600 text-white' : 
                    isCurrent ? 'bg-white border-blue-600 text-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.3)]' : 
                    'bg-white border-slate-300 text-slate-400'
                  }`}
                >
                  {isCompleted ? <CheckCircle2 className="w-6 h-6" /> : <span className="font-semibold">{step.id}</span>}
                </div>
                <div className="absolute top-12 text-xs font-medium text-slate-500 whitespace-nowrap hidden md:block">
                  {step.title}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Step Content */}
      <div className="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden min-h-[500px] relative">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="p-6 md:p-8 h-full"
          >
            {renderStep()}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
