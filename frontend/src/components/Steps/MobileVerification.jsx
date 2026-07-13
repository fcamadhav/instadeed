import React, { useState } from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import { motion } from 'framer-motion';
import { ChevronLeft, ShieldCheck, Fingerprint, CheckCircle2 } from 'lucide-react';

// NOTE: Replace this with your actual Google Client ID
const GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com";

export default function MobileVerification({ onVerified, onBack }) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [profile, setProfile] = useState(null);

  const handleSuccess = (credentialResponse) => {
    setLoading(true);
    try {
      const decoded = jwtDecode(credentialResponse.credential);
      setProfile(decoded);
      setSuccess(true);
      
      // Artificial delay for smooth UX
      setTimeout(() => {
        onVerified(decoded);
      }, 1500);
    } catch (error) {
      console.error('Error decoding JWT', error);
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-md mx-auto">
      <div className="flex items-center gap-4 mb-8 pb-4 border-b border-slate-100">
        <button onClick={onBack} className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500">
          <ChevronLeft size={24} />
        </button>
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Verify Identity</h2>
        </div>
      </div>

      <div className="flex-grow flex flex-col items-center justify-center text-center">
        <div className="w-20 h-20 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 text-blue-600 shadow-inner">
          <Fingerprint size={40} strokeWidth={1.5} />
        </div>
        
        <h3 className="text-xl font-bold text-slate-800 mb-2">Passwordless Login</h3>
        <p className="text-slate-500 mb-8 max-w-sm">
          Securely authenticate with Google to access your documents anywhere. No passwords to remember.
        </p>

        {!success ? (
          <div className="w-full max-w-xs space-y-4">
            <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
              <div className="flex justify-center overflow-hidden rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow bg-white">
                <GoogleLogin
                  onSuccess={handleSuccess}
                  onError={() => {
                    console.log('Login Failed');
                  }}
                  useOneTap
                  theme="outline"
                  size="large"
                  text="continue_with"
                  shape="rectangular"
                  width="320"
                />
              </div>
            </GoogleOAuthProvider>
            
            <div className="flex items-center justify-center gap-2 text-xs text-slate-400 mt-6">
              <ShieldCheck size={14} />
              <span>256-bit Secure Authentication</span>
            </div>
          </div>
        ) : (
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-full max-w-xs bg-emerald-50 border border-emerald-200 rounded-2xl p-6 flex flex-col items-center"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring' }}
              className="w-16 h-16 bg-emerald-500 rounded-full flex items-center justify-center text-white mb-4 shadow-lg shadow-emerald-500/30"
            >
              <CheckCircle2 size={32} />
            </motion.div>
            <h4 className="font-bold text-emerald-800 mb-1">Verified Successfully</h4>
            <p className="text-sm text-emerald-600 mb-4">{profile?.email}</p>
            <div className="w-full h-1 bg-emerald-200 rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ duration: 1.5, ease: 'linear' }}
                className="h-full bg-emerald-500"
              />
            </div>
            <p className="text-xs text-emerald-600 mt-3 font-medium">Preparing checkout...</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
