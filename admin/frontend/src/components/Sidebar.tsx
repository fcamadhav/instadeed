'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import {
  LayoutDashboard, Package, IndianRupee, ShoppingCart, Users, CreditCard,
  Tag, Receipt, Bell, Brain, Scan, GitBranch, Globe, Settings, ScrollText,
  BarChart3, LogOut, X, ChevronRight, FileText, Calendar,
  ClipboardList, FolderTree, MoreHorizontal
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
  children?: NavItem[];
}

const navSections: { title: string; icon: any; items: NavItem[] }[] = [
  {
    title: 'Dashboard',
    icon: LayoutDashboard,
    items: [{ label: 'Overview', icon: LayoutDashboard, href: '/admin/dashboard' }],
  },
  {
    title: 'Orders & Commerce',
    icon: ShoppingCart,
    items: [
      { label: 'Orders', icon: ShoppingCart, href: '/admin/orders' },
      { label: 'Customers', icon: Users, href: '/admin/customers' },
      { label: 'Payments', icon: CreditCard, href: '/admin/payments' },
      { label: 'Coupons', icon: Tag, href: '/admin/coupons' },
      { label: 'GST & Tax', icon: Receipt, href: '/admin/gst' },
    ],
  },
  {
    title: 'Documents',
    icon: FileText,
    items: [
      { label: 'Rent Agreements', icon: FileText, href: '/admin/rent-agreements' },
      { label: 'Calendar', icon: Calendar, href: '/admin/rent-agreements/calendar' },
      { label: 'All Documents', icon: ClipboardList, href: '/admin/documents-management' },
      { label: 'Customer Uploads', icon: FileText, href: '/admin/applications' },
      { label: 'Downloads Center', icon: FileText, href: '/admin/downloads' },
    ],
  },
  {
    title: 'Services',
    icon: Package,
    items: [
      { label: 'Services', icon: Package, href: '/admin/services' },
      { label: 'Categories', icon: FolderTree, href: '/admin/categories' },
      { label: 'Pricing', icon: IndianRupee, href: '/admin/pricing' },
    ],
  },
  {
    title: 'Analytics',
    icon: BarChart3,
    items: [
      { label: 'Reports', icon: BarChart3, href: '/admin/reports' },
      { label: 'Rent Reports', icon: ClipboardList, href: '/admin/rent-agreements/reports' },
      { label: 'Audit Logs', icon: ScrollText, href: '/admin/audit' },
    ],
  },
  {
    title: 'Settings',
    icon: Settings,
    items: [
      { label: 'General', icon: Settings, href: '/admin/settings' },
      { label: 'Notifications', icon: Bell, href: '/admin/notifications' },
      { label: 'Website', icon: Globe, href: '/admin/website' },
    ],
  },
  {
    title: 'Advanced',
    icon: MoreHorizontal,
    items: [
      { label: 'Workflow', icon: GitBranch, href: '/admin/workflow' },
      { label: 'AI Settings', icon: Brain, href: '/admin/ai' },
      { label: 'OCR', icon: Scan, href: '/admin/ai' },
    ],
  },
];

export default function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    'Orders & Commerce': true,
    'Documents': true,
    'Services': true,
    'Analytics': true,
    'Settings': true,
    'Advanced': false,
  });

  const isActive = (href: string) => {
    if (href === '/admin/dashboard') return pathname === href;
    return pathname.startsWith(href);
  };

  const isSectionActive = (items: NavItem[]) => {
    return items.some(item => isActive(item.href) || item.children?.some(c => isActive(c.href)));
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
        className={`fixed top-0 left-0 z-50 h-full w-60 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 transform transition-transform duration-200 lg:translate-x-0 lg:static lg:z-auto ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between px-4 h-14 border-b border-slate-200 dark:border-slate-800">
            <Link href="/admin/dashboard" className="flex items-center gap-2">
              <span className="text-base font-bold tracking-tight text-slate-900 dark:text-white">
                INSTA<span className="text-admin-600 dark:text-admin-400">DEED</span>
              </span>
            </Link>
            <button onClick={onClose} className="lg:hidden text-slate-400 hover:text-slate-600 p-1">
              <X className="w-4 h-4" />
            </button>
          </div>

          <nav className="flex-1 overflow-y-auto scrollbar-thin px-2 py-3 space-y-1">
            {navSections.map((section) => {
              const isExpandable = section.items.length > 1;
              const active = isSectionActive(section.items);
              const expanded = expandedSections[section.title] !== false;

              return (
                <div key={section.title}>
                  <button
                    onClick={() => isExpandable && toggleSection(section.title)}
                    className={`flex items-center w-full gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider transition-colors ${
                      active
                        ? 'text-slate-900 dark:text-white'
                        : 'text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-400'
                    }`}
                  >
                    <section.icon className="w-3.5 h-3.5 flex-shrink-0" />
                    <span className="flex-1 text-left">{section.title}</span>
                    {isExpandable && (
                      <ChevronRight className={`w-3 h-3 transition-transform ${expanded ? 'rotate-90' : ''}`} />
                    )}
                  </button>

                  {(!isExpandable || expanded) && (
                    <div className="space-y-0.5 mt-0.5">
                      {section.items.map((item) => {
                        const active = isActive(item.href);
                        return (
                          <Link
                            key={item.href}
                            href={item.href}
                            onClick={onClose}
                            className={`flex items-center gap-2.5 px-3 py-1.5 pl-8 rounded-lg text-sm transition-all ${
                              active
                                ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-medium'
                                : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                            }`}
                          >
                            <item.icon className="w-3.5 h-3.5 flex-shrink-0" />
                            <span className="truncate">{item.label}</span>
                            {item.badge && (
                              <span className="ml-auto text-[10px] bg-slate-200 dark:bg-slate-700 px-1.5 py-0.5 rounded-full font-medium text-slate-600 dark:text-slate-400">
                                {item.badge}
                              </span>
                            )}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>

          <div className="border-t border-slate-200 dark:border-slate-800 p-3">
            <div className="flex items-center gap-2.5 mb-2">
              <div className="w-7 h-7 rounded-full bg-slate-800 dark:bg-white flex items-center justify-center text-white dark:text-slate-800 text-xs font-semibold">
                {user?.name?.charAt(0)?.toUpperCase() || 'A'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-slate-900 dark:text-white truncate">{user?.name || 'Admin'}</p>
                <p className="text-[11px] text-slate-400 truncate">{user?.email || ''}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 w-full px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              <LogOut className="w-3.5 h-3.5" />
              Sign Out
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
