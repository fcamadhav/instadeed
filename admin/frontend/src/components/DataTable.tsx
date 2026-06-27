'use client';

import { useState, ReactNode } from 'react';
import {
  ChevronUp, ChevronDown, ChevronLeft, ChevronRight,
  ChevronsLeft, ChevronsRight, ArrowUpDown, Loader2, Inbox
} from 'lucide-react';

export interface Column<T> {
  key: string;
  label: string;
  sortable?: boolean;
  render?: (item: T) => ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  page?: number;
  totalPages?: number;
  total?: number;
  onPageChange?: (page: number) => void;
  sortKey?: string;
  sortOrder?: 'asc' | 'desc';
  onSort?: (key: string) => void;
  keyExtractor: (item: T, index?: number) => string | number;
  emptyMessage?: string;
  emptyDescription?: string;
  onRowClick?: (item: T) => void;
}

export default function DataTable<T extends Record<string, any>>({
  columns,
  data,
  loading,
  error,
  onRetry,
  page = 1,
  totalPages = 1,
  total,
  onPageChange,
  sortKey,
  sortOrder,
  onSort,
  keyExtractor,
  emptyMessage = 'No data found',
  emptyDescription = 'There are no records to display.',
  onRowClick,
}: DataTableProps<T>) {
  const [pageInput, setPageInput] = useState('');

  const getSortIcon = (key: string) => {
    if (sortKey !== key) return <ArrowUpDown className="w-3 h-3 text-slate-400" />;
    return sortOrder === 'asc' ? (
      <ChevronUp className="w-3 h-3 text-admin-600" />
    ) : (
      <ChevronDown className="w-3 h-3 text-admin-600" />
    );
  };

  if (error) {
    return (
      <div className="card p-8 text-center">
        <div className="w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center mx-auto mb-3">
          <Inbox className="w-6 h-6 text-red-500" />
        </div>
        <p className="text-sm font-medium text-slate-900 dark:text-white mb-1">Error loading data</p>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">{error}</p>
        {onRetry && (
          <button onClick={onRetry} className="btn-primary btn-sm">
            Try Again
          </button>
        )}
      </div>
    );
  }

  if (loading) {
    return (
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
                {columns.map(col => (
                  <th key={col.key} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    {col.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: 5 }).map((_, i) => (
                <tr key={i} className="border-b border-slate-100 dark:border-slate-700/50">
                  {columns.map(col => (
                    <td key={col.key} className="px-4 py-3">
                      <div className="skeleton h-4 w-24" />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="card p-8 text-center">
        <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center mx-auto mb-3">
          <Inbox className="w-6 h-6 text-slate-400" />
        </div>
        <p className="text-sm font-medium text-slate-900 dark:text-white mb-1">{emptyMessage}</p>
        <p className="text-sm text-slate-500 dark:text-slate-400">{emptyDescription}</p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto scrollbar-thin">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
              {columns.map(col => (
                <th
                  key={col.key}
                  className={`px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider ${
                    col.sortable ? 'cursor-pointer hover:text-slate-700 dark:hover:text-slate-200 select-none' : ''
                  } ${col.className || ''}`}
                  onClick={() => col.sortable && onSort?.(col.key)}
                >
                  <div className="flex items-center gap-1">
                    {col.label}
                    {col.sortable && getSortIcon(col.key)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr
                key={keyExtractor(item)}
                onClick={() => onRowClick?.(item)}
                className={`border-b border-slate-100 dark:border-slate-700/50 hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors ${
                  onRowClick ? 'cursor-pointer' : ''
                }`}
              >
                {columns.map(col => (
                  <td key={col.key} className={`px-4 py-3 text-sm text-slate-700 dark:text-slate-300 ${col.className || ''}`}>
                    {col.render ? col.render(item) : item[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && onPageChange && (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 px-4 py-3 border-t border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
          <div className="text-sm text-slate-500 dark:text-slate-400">
            {total !== undefined && `Total: ${total} records`}
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => onPageChange(1)}
              disabled={page === 1}
              className="p-1.5 rounded text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronsLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page === 1}
              className="p-1.5 rounded text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-1 mx-1">
              <span className="text-sm text-slate-600 dark:text-slate-400">Page</span>
              <input
                type="number"
                min={1}
                max={totalPages}
                value={pageInput || page}
                onChange={e => setPageInput(e.target.value)}
                onBlur={() => {
                  if (pageInput) {
                    const p = Math.max(1, Math.min(totalPages, parseInt(pageInput) || 1));
                    onPageChange(p);
                    setPageInput('');
                  }
                }}
                onKeyDown={e => {
                  if (e.key === 'Enter') {
                    const p = Math.max(1, Math.min(totalPages, parseInt(pageInput) || 1));
                    onPageChange(p);
                    setPageInput('');
                  }
                }}
                className="w-12 text-center input py-1 px-1 text-sm"
              />
              <span className="text-sm text-slate-500 dark:text-slate-400">of {totalPages}</span>
            </div>

            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page === totalPages}
              className="p-1.5 rounded text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onPageChange(totalPages)}
              disabled={page === totalPages}
              className="p-1.5 rounded text-slate-500 hover:bg-slate-200 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronsRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
