'use client';

import { useState, useEffect, useCallback } from 'react';
import { Search, FileText, ShoppingCart, User, ArrowRight, Loader2 } from 'lucide-react';
import { apiGet } from '@/lib/api';
import { useRouter } from 'next/navigation';

interface SearchResults { orders: any[]; customers: any[]; documents: any[]; }

export default function SearchPalette() {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState('');
  const [results, setResults] = useState<SearchResults>({ orders: [], customers: [], documents: [] });
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(0);
  const router = useRouter();

  const allResults = useCallback(() => {
    const items: { type: string; id: string; label: string; sub: string; route: string }[] = [];
    results.orders.forEach(o => items.push({ type: 'order', id: o.id, label: `#${o.orderNumber?.replace('ID-','')}`, sub: `${o.customerName||'N/A'} · ${o.service?.name||''} · ₹${(o.total||0).toLocaleString('en-IN')}`, route: '/admin/orders' }));
    results.customers.forEach(c => items.push({ type: 'customer', id: c.id, label: c.name, sub: `${c.email||''} ${c.phone||''} · ${c._count?.orders||0} orders`, route: '/admin/customers' }));
    results.documents.forEach(d => items.push({ type: 'document', id: d.id, label: d.documentNumber, sub: `${d.documentType} · ${d.service?.name||''} · ${d.order?.orderNumber||''}`, route: '/admin/downloads' }));
    return items;
  }, [results]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); setOpen(o => !o); }
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, []);

  useEffect(() => { if (!q || q.length < 2) { setResults({ orders:[], customers:[], documents:[] }); return; }
    const t = setTimeout(() => { setLoading(true);
      apiGet<{ data: SearchResults }>(`/admin/search?q=${encodeURIComponent(q)}`).then(r => { if (r.data) setResults(r.data); }).catch(()=>{}).finally(()=>setLoading(false));
    }, 200);
    return () => clearTimeout(t);
  }, [q]);

  useEffect(() => { setSelected(0); }, [results]);

  if (!open) return null;

  const items = allResults();
  const select = (item: typeof items[0]) => { setOpen(false); router.push(item.route); };

  return (
    <div className="fixed inset-0 z-[9999] flex items-start justify-center pt-[15vh]" onClick={() => setOpen(false)}>
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden" onClick={e => e.stopPropagation()}>
        <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-100">
          <Search className="w-4 h-4 text-slate-400 flex-shrink-0" />
          <input autoFocus type="text" value={q} onChange={e => setQ(e.target.value)} placeholder="Search orders, customers, documents..."
            className="flex-1 text-sm outline-none placeholder:text-slate-400" />
          <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-medium text-slate-400 bg-slate-100 rounded">ESC</kbd>
        </div>
        <div className="max-h-80 overflow-y-auto">
          {loading ? <div className="py-8 text-center"><Loader2 className="w-5 h-5 animate-spin text-slate-300 mx-auto"/></div>
          : items.length === 0 && q.length >= 2 ? <div className="py-8 text-center text-sm text-slate-400">No results for &quot;{q}&quot;</div>
          : !q || q.length < 2 ? <div className="py-8 text-center text-sm text-slate-400">Type to search across orders, customers, and documents</div>
          : items.map((item, i) => {
            const Icon = item.type === 'order' ? ShoppingCart : item.type === 'customer' ? User : FileText;
            const color = item.type === 'order' ? 'text-blue-600 bg-blue-50' : item.type === 'customer' ? 'text-green-600 bg-green-50' : 'text-amber-600 bg-amber-50';
            return (
              <button key={`${item.type}-${item.id}`} onClick={() => select(item)}
                className={`w-full flex items-center gap-3 px-4 py-2.5 hover:bg-slate-50 transition-colors text-left ${i === selected ? 'bg-slate-50' : ''}`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${color}`}><Icon className="w-4 h-4"/></div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-800 truncate">{item.label}</p>
                  <p className="text-xs text-slate-400 truncate">{item.sub}</p>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
              </button>
            );
          })}
        </div>
        {items.length > 0 && (
          <div className="border-t border-slate-100 px-4 py-2 flex items-center justify-between text-[10px] text-slate-400">
            <span>{items.length} results</span>
            <span className="flex items-center gap-2">
              <span><kbd className="px-1 py-0.5 bg-slate-100 rounded">↑↓</kbd> Navigate</span>
              <span><kbd className="px-1 py-0.5 bg-slate-100 rounded">↵</kbd> Open</span>
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
