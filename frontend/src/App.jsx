import React, { useState } from 'react';
import DocumentWizard from './components/Wizard/DocumentWizard';
import AdminDashboard from './components/Admin/AdminDashboard';
import { Home, UserCog } from 'lucide-react';

function App() {
  const [view, setView] = useState('user'); // 'user' | 'admin'

  return (
    <div className="min-h-screen bg-slate-50 font-sans selection:bg-blue-100 selection:text-blue-900 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 text-blue-700 font-black text-xl tracking-tight cursor-pointer" onClick={() => setView('user')}>
            <div className="w-8 h-8 bg-blue-600 text-white rounded-lg flex items-center justify-center shadow-inner">
              M
            </div>
            Madhav Drafting
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
            <button onClick={() => setView('user')} className={`transition-colors ${view === 'user' ? 'text-blue-600 font-bold' : 'hover:text-blue-600'}`}>User Flow</button>
            <button onClick={() => setView('admin')} className={`transition-colors ${view === 'admin' ? 'text-blue-600 font-bold' : 'hover:text-blue-600'}`}>Admin View</button>
          </div>
          <button 
            onClick={() => setView(view === 'user' ? 'admin' : 'user')}
            className="flex items-center gap-2 text-sm font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-lg transition-colors"
          >
            {view === 'user' ? <><UserCog size={16} /> Admin Login</> : <><Home size={16} /> Back to Site</>}
          </button>
        </div>
      </header>

      {/* Main View Area */}
      <main className="flex-grow flex flex-col">
        {view === 'user' ? (
          <>
            <div className="bg-gradient-to-b from-blue-900 to-slate-900 text-white py-12 md:py-20 px-4">
              <div className="max-w-3xl mx-auto text-center">
                <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">Create your document in minutes</h1>
                <p className="text-blue-200 text-lg md:text-xl font-medium max-w-2xl mx-auto">
                  Our streamlined process makes drafting legally binding agreements faster, easier, and more secure than ever before.
                </p>
              </div>
            </div>
            <div className="flex-grow -mt-10 md:-mt-16 relative z-10 pb-20">
              <DocumentWizard onViewAdmin={() => setView('admin')} />
            </div>
          </>
        ) : (
          <AdminDashboard />
        )}
      </main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-8 text-center text-slate-500 text-sm">
        <p>&copy; {new Date().getFullYear()} Madhav Drafting Hub. All rights reserved.</p>
        <div className="flex justify-center gap-4 mt-4">
          <a href="#" className="hover:text-blue-600">Terms</a>
          <a href="#" className="hover:text-blue-600">Privacy</a>
          <a href="#" className="hover:text-blue-600">Contact</a>
        </div>
      </footer>
    </div>
  );
}

export default App;
