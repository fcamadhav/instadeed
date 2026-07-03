'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet, apiDownload } from '@/lib/api';
import { Search, Download, Eye, ChevronDown, ChevronRight, FileText, Clock, CheckCircle, AlertCircle, X } from 'lucide-react';

interface AppDoc { id: string; applicationId: string; documentType: string; fileName: string; fileUrl: string; mimeType: string; size: number; uploadedAt: string; }
interface AppGroup { appId: string; docs: AppDoc[]; completed: number; total: number; lastUpdated: string; svcKey: string; svcName: string; }

const DOC_LABELS: Record<string,string> = {
  'sale-deed':'Sale Deed','aadhaar':'Aadhaar Card','pan':'PAN Card',
  'sanctioned-letter':'Sanctioned Letter','bank-noc':'Bank NOC',
  'application-form':'Application Form','bank-request':'Bank Request Letter',
  'tm-form':'TM Application','noc-builder':'Builder NOC','no-dues':'No Dues',
  'mortgage-noc':'Mortgage NOC','challan':'Challan','affidavit':'Affidavit',
  'id-proof':'ID Proof','occupancy':'Occupancy Certificate',
};

const SVC: Record<string,{name:string;color:string;bg:string;border:string}> = {
  mutation:{name:'Mutation',color:'#d97706',bg:'bg-amber-50',border:'border-amber-200'},
  gnida_ptm:{name:'Permission to Mortgage',color:'#7c3aed',bg:'bg-violet-50',border:'border-violet-200'},
  gnida_package:{name:'5-in-1 Package',color:'#e11d48',bg:'bg-rose-50',border:'border-rose-200'},
  gnida_registry:{name:'Registry Deed',color:'#2563eb',bg:'bg-blue-50',border:'border-blue-200'},
};
SVC['GNIDA_PTM']=SVC.gnida_ptm; SVC['MUTATION']=SVC.mutation;
SVC['GNIDA_PACKAGE']=SVC.gnida_package; SVC['GNIDA_REGISTRY']=SVC.gnida_registry;

const REQUIRED: Record<string,number> = { mutation:2, gnida_ptm:6, gnida_package:8, gnida_registry:4 };

export default function ApplicationDocumentsPage() {
  const [groups, setGroups] = useState<AppGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [expanded, setExpanded] = useState<string|null>(null);

  useEffect(() => { fetchDocs(); }, []);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { grouped: Record<string,AppDoc[]>; total:number } }>('/admin/applications/documents');
      if (res.data?.grouped) {
        const g = Object.entries(res.data.grouped).map(([appId, docs]) => {
          const d = docs as AppDoc[]; const k = appId.split('-')[0];
          const svc = SVC[k]||{name:k.toUpperCase(),color:'#64748b',bg:'bg-slate-50',border:'border-slate-200'};
          return { appId, docs:d, completed:new Set(d.map(x=>x.documentType)).size, total:REQUIRED[k]||8,
            lastUpdated:d.reduce((m,x)=>x.uploadedAt>m?x.uploadedAt:m,d[0]?.uploadedAt||''), svcKey:k, svcName:svc.name };
        });
        g.sort((a,b)=>new Date(b.lastUpdated).getTime()-new Date(a.lastUpdated).getTime());
        setGroups(g);
      }
    } catch {} finally { setLoading(false); }
  };

  const filtered = search ? groups.filter(g => {
    const s = search.toLowerCase();
    return g.appId.toLowerCase().includes(s) || g.svcName.toLowerCase().includes(s) ||
      g.docs.some(d => d.fileName.toLowerCase().includes(s) || (DOC_LABELS[d.documentType]||'').toLowerCase().includes(s));
  }) : groups;

  if (loading) return <AdminLayout title="Application Documents"><div className="flex items-center justify-center py-20"><div className="w-8 h-8 border-2 border-admin-600 border-t-transparent rounded-full animate-spin"/></div></AdminLayout>;

  return (
    <AdminLayout title="Application Documents">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5">
        <p className="text-sm text-slate-500">{filtered.length} application{filtered.length!==1?'s':''}</p>
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input type="text" placeholder="Search by service, document name..." value={search} onChange={e => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-admin-500 focus:ring-2 focus:ring-admin-100" />
          {search && <button onClick={() => setSearch('')} className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"><X className="w-3.5 h-3.5"/></button>}
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-16 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-slate-50 flex items-center justify-center">
            <FileText className="w-7 h-7 text-slate-300" />
          </div>
          <h3 className="text-base font-semibold text-slate-700 mb-1">No documents yet</h3>
          <p className="text-sm text-slate-400">Customer uploads from Mutation, PTM, and 5-in-1 Package applications will appear here.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(g => {
            const svc = SVC[g.svcKey]||{name:g.svcKey.toUpperCase(),color:'#64748b',bg:'bg-slate-50',border:'border-slate-200'};
            const pct = g.total ? Math.round(g.completed/g.total*100) : 0;
            const isOpen = expanded === g.appId;
            const statusLabel = pct===100?'Complete':pct>=50?'In Progress':'Pending';
            const StatusIcon = pct===100 ? CheckCircle : pct>=50 ? Clock : AlertCircle;

            return (
              <div key={g.appId} className="bg-white rounded-xl border border-slate-200 overflow-hidden transition-all hover:shadow-md">
                <div className="p-5">
                  <div className="flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-xl ${svc.bg} flex items-center justify-center flex-shrink-0`} style={{color:svc.color}}>
                      <FileText className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-bold text-slate-900">{g.svcName}</span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${svc.border} ${svc.bg}`} style={{color:svc.color}}>{g.svcKey.toUpperCase()}</span>
                      </div>
                      <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                        <span className="flex items-center gap-1"><FileText className="w-3 h-3"/>{g.docs.length} file{g.docs.length!==1?'s':''}</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3"/>{new Date(g.lastUpdated).toLocaleDateString('en-IN',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'})}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 flex-shrink-0">
                      <div className="hidden sm:flex items-center gap-2">
                        <div className="w-24 h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div className={`h-full rounded-full transition-all ${pct===100?'bg-green-500':pct>=50?'bg-amber-500':'bg-slate-300'}`} style={{width:pct+'%'}}/>
                        </div>
                        <span className="text-xs font-semibold text-slate-500 w-8 text-right">{pct}%</span>
                      </div>
                      <button onClick={() => setExpanded(isOpen?null:g.appId)}
                        className="p-2 rounded-lg hover:bg-slate-50 transition-colors text-slate-400 hover:text-slate-600">
                        {isOpen ? <ChevronDown className="w-4 h-4"/> : <ChevronRight className="w-4 h-4"/>}
                      </button>
                    </div>
                  </div>
                </div>

                {isOpen && (
                  <div className="border-t border-slate-100 bg-slate-50/30">
                    <div className="px-5 py-2 text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Uploaded Documents</div>
                    <div className="divide-y divide-slate-100">
                      {g.docs.map(d => (
                        <div key={d.id} className="flex items-center gap-3 px-5 py-3 hover:bg-white transition-colors">
                          <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                            <FileText className="w-4 h-4 text-slate-500" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-xs font-semibold text-slate-800">{DOC_LABELS[d.documentType]||d.documentType}</p>
                            <p className="text-xs text-slate-400 truncate">{d.fileName} &middot; {(d.size/1024).toFixed(0)} KB &middot; {new Date(d.uploadedAt).toLocaleDateString('en-IN',{day:'2-digit',month:'short'})}</p>
                          </div>
                          <div className="flex gap-1">
                            <button onClick={() => apiDownload(`/applications/documents/${d.id}/file`, d.fileName)}
                              className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium bg-admin-600 text-white rounded-lg hover:bg-admin-700 transition-colors">
                              <Download className="w-3 h-3"/> Download
                            </button>
                            <button onClick={async () => { try { const t = JSON.parse(localStorage.getItem('instadeed_admin_user')||'{}').token; const r = await fetch('/api/applications/documents/'+d.id+'/file',{headers:t?{Authorization:'Bearer '+t}:{}}); const b = await r.blob(); window.open(URL.createObjectURL(b),'_blank'); } catch {} }}
                              className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-colors">
                              <Eye className="w-3 h-3"/> View
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
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
