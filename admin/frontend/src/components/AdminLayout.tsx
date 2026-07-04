'use client';

import { useState, ReactNode } from 'react';
import Sidebar from './Sidebar';
import Topbar from './Topbar';
import SearchPalette from './SearchPalette';

interface AdminLayoutProps {
  title: string;
  children: ReactNode;
}

export default function AdminLayout({ title, children }: AdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen flex bg-white dark:bg-slate-950" style={{ minHeight: '100dvh' }}>
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar title={title} onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 p-4 lg:p-6 overflow-x-hidden">
          {children}
        </main>
      </div>
      <SearchPalette />
    </div>
  );
}
