'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet, apiDownload } from '@/lib/api';
import { Download, Eye, Search, ChevronDown, ChevronRight, FileText, Calendar, User, Phone, Clock } from 'lucide-react';

interface AppDoc { id: string; applicationId: string; documentType: string; fileName: string; fileUrl: string; mimeType: string; size: number; uploadedAt: string; }
interface AppGroup { appId: string; docs: AppDoc[]; docCount: number; completed: number; total: number; lastUpdated: string; }

const DOC_LABELS: Record<string,string> = {
  'sale-deed':'Registered Sale Deed','aadhaar':'Aadhaar Card','pan':'PAN Card',
  'sanctioned-letter':'Sanctioned Letter','bank-noc':'Bank NOC',
  'application-form':'Application Form','bank-request':'Request Letter from Bank',
  'tm-form':'T.M. Application Form','noc-builder':'Builder NOC','no-dues':'No Dues Certificate',
  'mortgage-noc':'Mortgage N.O.C','challan':'Challan Copy','affidavit':'Affidavit',
  'id-proof':'ID & Address Proof','occupancy':'Occupancy Certificate',
};

const SVC_STYLES: Record<string,string> = {
  'mutation':'bg-amber-50 text-amber-700 border-amber-200',
  'gnida_ptm':'bg-purple-50 text-purple-700 border-purple-200',
  'gnida_package':'bg-rose-50 text-rose-700 border-rose-200',
  'gnida_registry':'bg-blue-50 text-blue-700 border-blue-200',
};

const SVC_LABELS: Record<string,string> = {
  'mutation':'Mutation','gnida_ptm':'PTM','gnida_package':'5-in-1 Package','gnida_registry':'Registry',
  MUTATION:'Mutation','GNIDA_PTM':'PTM','GNIDA_PACKAGE':'5-in-1 Package','GNIDA_REGISTRY':'Registry',
};

const REQUIRED_COUNTS: Record<string,number> = { mutation: 2, gnida_ptm: 6, gnida_package: 8, gnida_registry: 4 };

export default function ApplicationDocumentsPage() {
  const [groups, setGroups] = useState<AppGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState<Record<string,boolean>>({});

  useEffect(() => { fetchDocs(); }, []);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { grouped: Record<string,AppDoc[]>; total:number } }>('/admin/applications/documents');
      if (res.data?.grouped) {
        const g = Object.entries(res.data.grouped).map(([appId, docs]) => {
          const d = docs as AppDoc[];
          const svcKey = appId.split('-')[0];
          return {
            appId,
            docs: d,
            docCount: d.length,
            completed: new Set(d.map(x => x.documentType)).size,
            total: REQUIRED_COUNTS[svcKey] || Object.keys(DOC_LABELS).length,
            lastUpdated: d.reduce((max,x) => x.uploadedAt > max ? x.uploadedAt : max, d[0]?.uploadedAt || ''),
          };
        });
        g.sort((a,b) => new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime());
        setGroups(g);
      }
    } catch {} finally { setLoading(false); }
  };

  const filtered = search ? groups.filter(g => {
    const s = search.toLowerCase();
    return g.appId.toLowerCase().includes(s) || g.docs.some(d => d.fileName.toLowerCase().includes(s) || (DOC_LABELS[d.documentType]||'').toLowerCase().includes(s));
  }) : groups;

  const toggleExpand = (appId: string) => setExpanded(p => ({ ...p, [appId]: !p[appId] }));

  if (loading) return <AdminLayout title="Documents"><div className="flex items-center justify-center py-20"><svg className="w-6 h-6 animate-spin text-admin-600" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg></div></AdminLayout>;

  return (
    <AdminLayout title="Documents">
      <div className="mb-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input type="text" placeholder="Search applications..." value={search} onChange={e => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-xl text-sm focus:outline-none focus:border-admin-500 focus:ring-2 focus:ring-admin-100" />
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="card p-10 text-center">
          <FileText className="w-12 h-12 text-slate-200 mx-auto mb-4" />
          <p className="text-sm font-semibold text-slate-500">No documents yet</p>
          <p className="text-xs text-slate-400 mt-1">Customer uploads will appear here.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map(({ appId, docs, completed, total, lastUpdated }) => {
            const svcKey = appId.split('-')[0];
            const svcName = SVC_LABELS[svcKey] || svcKey.toUpperCase();
            const svcStyle = SVC_STYLES[svcKey] || 'bg-slate-50 text-slate-700 border-slate-200';
            const isExpanded = expanded[appId];
            const pct = total ? Math.round(completed/total*100) : 0;

            return (
              <div key={appId} className="card overflow-hidden">
                <div className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold border ${svcStyle}`}>
                        <span className="w-2 h-2 rounded-full" style={{background: svcKey==='mutation'?'#d97706':svcKey==='gnida_ptm'?'#7c3aed':svcKey==='gnida_package'?'#e11d48':'#2563eb'}}/>
                        {svcName}
                      </span>
                    </div>
                    <span className="text-xs text-slate-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {new Date(lastUpdated).toLocaleDateString('en-IN', {day:'2-digit',month:'short'})}
                    </span>
                  </div>

                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <p className="text-xs text-slate-400">Documents</p>
                      <p className="text-lg font-bold text-slate-900">{completed}/{total}</p>
                    </div>
                    <div className="w-20 h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full transition-all ${pct===100?'bg-green-500':pct>=50?'bg-amber-500':'bg-red-400'}`} style={{width:pct+'%'}}/>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-1 mb-3">
                    {docs.slice(0,4).map(d => (
                      <span key={d.id} className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md">{DOC_LABELS[d.documentType]||d.documentType}</span>
                    ))}
                    {docs.length > 4 && <span className="text-xs text-slate-400 px-1">+{docs.length-4}</span>}
                  </div>

                  <button onClick={() => toggleExpand(appId)}
                    className="w-full flex items-center justify-center gap-1 text-xs font-semibold text-admin-600 hover:text-admin-800 py-1.5 rounded-lg hover:bg-admin-50 transition-colors">
                    {isExpanded ? <ChevronDown className="w-3.5 h-3.5"/> : <ChevronRight className="w-3.5 h-3.5"/>}
                    {isExpanded ? 'Hide details' : 'View all documents'}
                  </button>
                </div>

                {isExpanded && (
                  <div className="border-t border-slate-100 bg-slate-50/50">
                    {docs.map(d => (
                      <div key={d.id} className="flex items-center justify-between px-5 py-3 border-b border-slate-100 last:border-0 hover:bg-white transition-colors">
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-semibold text-slate-800">{DOC_LABELS[d.documentType]||d.documentType}</p>
                          <p className="text-xs text-slate-400 truncate">{d.fileName} · {(d.size/1024).toFixed(0)}KB</p>
                        </div>
                        <div className="flex gap-1 ml-2">
                          <button onClick={() => apiDownload(`/applications/documents/${d.id}/file`, d.fileName)} className="btn-secondary btn-sm p-1.5"><Download className="w-3 h-3"/></button>
                          <button onClick={async () => { try { const t = JSON.parse(localStorage.getItem('instadeed_admin_user')||'{}').token; const r = await fetch('/api/applications/documents/'+d.id+'/file',{headers:t?{Authorization:'Bearer '+t}:{}}); const b = await r.blob(); window.open(URL.createObjectURL(b),'_blank'); } catch {} }} className="btn-ghost btn-sm p-1.5"><Eye className="w-3 h-3"/></button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </AdminLayout>
  );
}
