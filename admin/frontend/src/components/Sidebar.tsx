'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import {
  Scale, LayoutDashboard, Package, FolderTree, IndianRupee,
  ShoppingCart, Users, CreditCard, Tag, Receipt, Bell,
  Brain, Scan, GitBranch, Globe, Settings, ScrollText,
  BarChart3, LogOut, X, ChevronDown, FileText, Calendar,
  ClipboardList
} from 'lucide-react';
import { useState } from 'react';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

interface NavItem {
  label: string;
  icon: any;
  href: string;
  badge?: string;
}

const navSections: { title?: string; items: NavItem[] }[] = [
  {
    items: [{ label: 'Dashboard', icon: LayoutDashboard, href: '/admin/dashboard' }],
  },
  {
    title: 'Management',
    items: [
      { label: 'Services', icon: Package, href: '/admin/services' },
      { label: 'Categories', icon: FolderTree, href: '/admin/categories' },
      { label: 'Pricing', icon: IndianRupee, href: '/admin/pricing' },
    ],
  },
  {
    title: 'Rent Agreements',
    items: [
      { label: 'Overview', icon: FileText, href: '/admin/rent-agreements' },
      { label: 'Calendar', icon: Calendar, href: '/admin/rent-agreements/calendar' },
      { label: 'Reports', icon: ClipboardList, href: '/admin/rent-agreements/reports' },
    ],
  },
  {
    title: 'Document Management',
    items: [
      { label: 'All Documents', icon: FileText, href: '/admin/documents-management' },
    ],
  },
  {
    title: 'Commerce',
    items: [
      { label: 'Orders', icon: ShoppingCart, href: '/admin/orders' },
      { label: 'Customers', icon: Users, href: '/admin/customers' },
      { label: 'Payments', icon: CreditCard, href: '/admin/payments' },
      { label: 'Coupons', icon: Tag, href: '/admin/coupons' },
      { label: 'GST & Tax', icon: Receipt, href: '/admin/gst' },
    ],
  },
  {
    title: 'Communication',
    items: [
      { label: 'Notifications', icon: Bell, href: '/admin/notifications' },
    ],
  },
  {
    title: 'Configuration',
    items: [
      { label: 'AI Settings', icon: Brain, href: '/admin/ai' },
      { label: 'OCR Settings', icon: Scan, href: '/admin/ai' },
      { label: 'Workflow', icon: GitBranch, href: '/admin/workflow' },
      { label: 'Website', icon: Globe, href: '/admin/website' },
      { label: 'Settings', icon: Settings, href: '/admin/settings' },
    ],
  },
  {
    title: 'Analytics',
    items: [
      { label: 'Audit Logs', icon: ScrollText, href: '/admin/audit' },
      { label: 'Reports', icon: BarChart3, href: '/admin/reports' },
    ],
  },
];

export default function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  const isActive = (href: string) => {
    if (href === '/admin/dashboard') return pathname === href;
    return pathname.startsWith(href);
  };

  const toggleSection = (title: string) => {
    setExpandedSections(prev => ({ ...prev, [title]: !prev[title] }));
  };

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={onClose} />
      )}

      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 transform transition-transform duration-200 lg:translate-x-0 lg:static lg:z-auto ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between px-4 h-16 border-b border-slate-200 dark:border-slate-700">
            <Link href="/admin/dashboard" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-admin-600 flex items-center justify-center">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-slate-900 dark:text-white text-sm">INSTADEED</span>
            </Link>
            <button onClick={onClose} className="lg:hidden text-slate-500 hover:text-slate-700 dark:hover:text-slate-300">
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="flex-1 overflow-y-auto scrollbar-thin px-3 py-4 space-y-1">
            {navSections.map((section, idx) => (
              <div key={idx}>
                {section.title && (
                  <button
                    onClick={() => toggleSection(section.title!)}
                    className="flex items-center justify-between w-full px-2 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500"
                  >
                    {section.title}
                    <ChevronDown className={`w-3 h-3 transition-transform ${expandedSections[section.title] ? 'rotate-180' : ''}`} />
                  </button>
                )}
                <div className={`space-y-0.5 ${section.title && !expandedSections[section.title] ? 'hidden' : ''}`}>
                  {section.items.map((item) => {
                    const active = isActive(item.href);
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        onClick={onClose}
                        className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                          active
                            ? 'bg-admin-50 dark:bg-admin-900/30 text-admin-700 dark:text-admin-300 font-medium'
                            : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50'
                        }`}
                      >
                        <item.icon className="w-4 h-4 flex-shrink-0" />
                        <span className="truncate">{item.label}</span>
                        {item.badge && (
                          <span className="ml-auto badge badge-blue text-[10px] px-1.5 py-0.5">{item.badge}</span>
                        )}
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}
          </nav>

          <div className="border-t border-slate-200 dark:border-slate-700 p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-8 h-8 rounded-full bg-admin-600 flex items-center justify-center text-white text-sm font-medium">
                {user?.name?.charAt(0)?.toUpperCase() || 'A'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-900 dark:text-white truncate">{user?.name || 'Admin'}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 truncate">{user?.email || ''}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
