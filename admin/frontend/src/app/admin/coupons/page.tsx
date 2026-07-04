'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import DataTable, { Column } from '@/components/DataTable';
import Modal from '@/components/Modal';
import FormField from '@/components/FormField';
import { apiGet, apiPost, apiPut, apiDelete } from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Copy, Search, X, Check, Percent, IndianRupee, Calendar, Tag, Users } from 'lucide-react';

interface Coupon { id: string; code: string; type: string; value: number; minOrder: number; maxUses: number; usedCount: number; expiryDate: string; status: boolean; applicableServices: string[]; applicableCategories: string[]; }
interface Service { id: string; name: string }
interface Category { id: string; name: string }

const emptyForm = { code:'', name:'', description:'', type:'percentage' as const, value:0, maxDiscount:0, minOrder:0, maxOrder:0, maxUses:0, maxUsesPerCustomer:1, currentUsage:0, startDate:'', endDate:'', firstOrderOnly:false, newCustomerOnly:false, autoApply:false, stackWithOthers:false, isActive:true, showOnWebsite:true, applicableServices:[] as string[], applicableCategories:[] as string[], excludeDiscounted:false, excludeGST:false, excludeFees:false };

export default function CouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<string|null>(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string,string>>({});
  const [deleteConfirm, setDeleteConfirm] = useState<string|null>(null);
  const [svcSearch, setSvcSearch] = useState('');
  const [catSearch, setCatSearch] = useState('');

  useEffect(()=>{fetchData();},[page]);

  const fetchData = async () => { setLoading(true); try { const [cp, sv, ct] = await Promise.all([apiGet<{data:{coupons:Coupon[],pagination:{totalPages:number}}}>(`/admin/coupons?page=${page}&limit=10`).catch(()=>null), apiGet<{data:{services:Service[]}}>('/admin/services?limit=500').catch(()=>null), apiGet<{data:{categories:Category[]}}>('/admin/categories?limit=500').catch(()=>null)]); if(cp?.data){setCoupons(cp.data.coupons||[]);setTotalPages(cp.data.pagination?.totalPages||1)} if(sv?.data)setServices(sv.data.services||[]); if(ct?.data)setCategories(ct.data.categories||[]); } catch{} finally{setLoading(false)} };

  const openCreate = () => { setEditing(null); setForm(emptyForm); setErrors({}); setModalOpen(true); };
  const openEdit = (c:Coupon) => { setEditing(c.id); setForm({...emptyForm, code:c.code, type:c.type as any, value:c.value, minOrder:c.minOrder, maxUses:c.maxUses, endDate:c.expiryDate?new Date(c.expiryDate).toISOString().split('T')[0]:'', isActive:c.status, applicableServices:c.applicableServices||[], applicableCategories:c.applicableCategories||[]}); setErrors({}); setModalOpen(true); };

  const genCode = () => { const c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; let r=''; for(let i=0;i<6;i++)r+=c[Math.floor(Math.random()*c.length)]; setForm({...form,code:r}); };

  const validate = () => {
    const e:Record<string,string>={};
    if(!form.code.trim())e.code='Required';
    if(!form.value||form.value<=0)e.value='Must be positive';
    if(form.type==='percentage'&&form.value>100)e.value='Cannot exceed 100%';
    if(form.type==='percentage'&&!form.maxDiscount&&form.maxDiscount!==0)e.maxDiscount='Set a cap for safety';
    setErrors(e);
    return Object.keys(e).length===0;
  };

  const handleSave = async (ev:FormEvent) => { ev.preventDefault(); if(!validate())return; setSaving(true);
    try { const payload:any={code:form.code,type:form.type,value:form.value,minOrder:form.minOrder||0,maxUses:form.maxUses||0,expiryDate:form.endDate||null,status:form.isActive,applicableServices:form.applicableServices,applicableCategories:form.applicableCategories};
      if(editing) await apiPut(`/admin/coupons/${editing}`,payload); else await apiPost('/admin/coupons',payload);
      toast.success(editing?'Updated':'Created'); setModalOpen(false); fetchData();
    } catch(err:any) { toast.error(err.message||'Failed'); } finally { setSaving(false); }
  };

  const handleDelete = async (id:string) => { try { await apiDelete(`/admin/coupons/${id}`); toast.success('Deleted'); setDeleteConfirm(null); fetchData(); } catch(err:any) { toast.error(err.message||'Failed'); } };

  const toggleSvc = (id:string) => { setForm(f=>({...f,applicableServices:f.applicableServices.includes(id)?f.applicableServices.filter(x=>x!==id):[...f.applicableServices,id]})); };
  const toggleCat = (id:string) => { setForm(f=>({...f,applicableCategories:f.applicableCategories.includes(id)?f.applicableCategories.filter(x=>x!==id):[...f.applicableCategories,id]})); };

  const filteredSvcs = services.filter(s=>s.name.toLowerCase().includes(svcSearch.toLowerCase()));
  const filteredCats = categories.filter(c=>c.name.toLowerCase().includes(catSearch.toLowerCase()));
  const selectedSvcs = services.filter(s=>form.applicableServices.includes(s.id));
  const selectedCats = categories.filter(c=>form.applicableCategories.includes(c.id));

  const discountDisplay = form.type==='percentage'?`${form.value}%${form.maxDiscount>0?` (Max ₹${form.maxDiscount.toLocaleString('en-IN')})`:''}`:`₹${form.value.toLocaleString('en-IN')}`;

  const columns: Column<Coupon>[] = [
    { key:'code', label:'Code', render:c=><span className="font-mono font-bold text-sm text-admin-600">{c.code}</span> },
    { key:'type', label:'Discount', render:c=>c.type==='percentage'?<span className="badge-blue">{c.value}%</span>:<span className="badge-green">₹{c.value}</span> },
    { key:'minOrder', label:'Min Order', render:c=>`₹${(c.minOrder||0).toLocaleString('en-IN')}` },
    { key:'maxUses', label:'Uses', render:c=><span className="text-xs">{c.usedCount||0}/{c.maxUses||'∞'}</span> },
    { key:'expiryDate', label:'Expires', render:c=>c.expiryDate?new Date(c.expiryDate).toLocaleDateString('en-IN'):'—' },
    { key:'status', label:'Status', render:c=>c.status?<span className="badge-green">Active</span>:<span className="badge-slate">Inactive</span> },
    { key:'actions', label:'', render:c=>(<div className="flex gap-1">
      <button onClick={e=>{e.stopPropagation();navigator.clipboard.writeText(c.code);toast.success('Copied')}} className="btn-ghost btn-sm p-1.5"><Copy className="w-3 h-3"/></button>
      <button onClick={e=>{e.stopPropagation();openEdit(c)}} className="btn-ghost btn-sm p-1.5"><Edit2 className="w-3 h-3"/></button>
      <button onClick={e=>{e.stopPropagation();setDeleteConfirm(c.id)}} className="btn-ghost btn-sm p-1.5 text-red-500"><Trash2 className="w-3 h-3"/></button>
    </div>)},
  ];

  return (
    <AdminLayout title="Coupons">
      <div className="flex items-center justify-between mb-4"><p className="text-sm text-slate-500">Manage discount coupons and offers</p><button onClick={openCreate} className="btn-primary btn-sm"><Plus className="w-4 h-4"/>Add Coupon</button></div>
      <DataTable columns={columns} data={coupons} loading={loading} page={page} totalPages={totalPages} onPageChange={setPage} keyExtractor={c=>c.id} onRowClick={openEdit} emptyMessage="No coupons yet"/>

      <Modal open={modalOpen} onClose={()=>setModalOpen(false)} title={editing?'Edit Coupon':'Add Coupon'} size="xl"
        footer={<><button onClick={()=>setModalOpen(false)} className="btn-secondary">Cancel</button><button onClick={handleSave} disabled={saving} className="btn-primary">{saving?'Saving...':'Save Coupon'}</button></>}>
        <form onSubmit={handleSave} className="space-y-5">
          {/* Basic */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><Tag className="w-4 h-4 text-admin-600"/>Basic Information</h4>
            <div className="grid grid-cols-3 gap-3">
              <div className="col-span-2 flex items-end gap-2">
                <div className="flex-1"><FormField label="Coupon Code*" value={form.code} onChange={e=>setForm({...form,code:e.target.value.toUpperCase()})} error={errors.code}/></div>
                <button type="button" onClick={genCode} className="btn-secondary btn-sm mb-1">Generate</button>
              </div>
              <FormField label="Coupon Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="e.g. Festival Offer"/>
            </div>
            <div className="mt-2"><FormField label="Description" value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Optional"/></div>
          </div>

          {/* Discount */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><Percent className="w-4 h-4 text-admin-600"/>Discount</h4>
            <div className="grid grid-cols-4 gap-3">
              <FormField type="select" label="Type" value={form.type} onChange={e=>setForm({...form,type:e.target.value as any})} options={[{value:'percentage',label:'Percentage'},{value:'fixed',label:'Fixed Amount'}]}/>
              <FormField label={form.type==='percentage'?'Discount %':'Amount (₹)'} type="number" value={form.value} onChange={e=>setForm({...form,value:parseFloat(e.target.value)||0})} error={errors.value}/>
              {form.type==='percentage'&&<FormField label="Max Discount (₹)" type="number" value={form.maxDiscount} onChange={e=>setForm({...form,maxDiscount:parseFloat(e.target.value)||0})} helperText="Caps the discount amount"/>}
              <FormField label="Min Order (₹)" type="number" value={form.minOrder} onChange={e=>setForm({...form,minOrder:parseFloat(e.target.value)||0})}/>
            </div>
          </div>

          {/* Usage Limits */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><Users className="w-4 h-4 text-admin-600"/>Usage Limits</h4>
            <div className="grid grid-cols-4 gap-3">
              <FormField label="Max Uses" type="number" value={form.maxUses} onChange={e=>setForm({...form,maxUses:parseInt(e.target.value)||0})} helperText="0=unlimited"/>
              <FormField label="Per Customer" type="number" value={form.maxUsesPerCustomer} onChange={e=>setForm({...form,maxUsesPerCustomer:parseInt(e.target.value)||1})}/>
              <FormField label="First Order Only" type="toggle" checked={form.firstOrderOnly} onChange={v=>setForm({...form,firstOrderOnly:v})}/>
              <FormField label="New Customers Only" type="toggle" checked={form.newCustomerOnly} onChange={v=>setForm({...form,newCustomerOnly:v})}/>
            </div>
          </div>

          {/* Validity */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2"><Calendar className="w-4 h-4 text-admin-600"/>Validity</h4>
            <div className="grid grid-cols-3 gap-3">
              <FormField label="Start Date" type="date" value={form.startDate} onChange={e=>setForm({...form,startDate:e.target.value})}/>
              <FormField label="End Date" type="date" value={form.endDate} onChange={e=>setForm({...form,endDate:e.target.value})}/>
            </div>
          </div>

          {/* Applicable To — searchable multi-select */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3">Applicable To</h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label text-xs">Services</label>
                <div className="border border-slate-200 rounded-lg">
                  <div className="p-2 border-b"><div className="relative"><Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400"/><input type="text" placeholder="Search services..." value={svcSearch} onChange={e=>setSvcSearch(e.target.value)} className="w-full pl-8 pr-2 py-1.5 text-xs border-0 focus:outline-none"/>{svcSearch&&<button onClick={()=>setSvcSearch('')} className="absolute right-2 top-1/2 -translate-y-1/2"><X className="w-3 h-3 text-slate-400"/></button>}</div></div>
                  <div className="max-h-36 overflow-y-auto p-1 space-y-0.5">
                    {filteredSvcs.map(s=>(<button key={s.id} type="button" onClick={()=>toggleSvc(s.id)} className={`w-full text-left px-2 py-1.5 rounded text-xs flex items-center gap-2 ${form.applicableServices.includes(s.id)?'bg-admin-50 text-admin-700':'hover:bg-slate-50 text-slate-600'}`}>{form.applicableServices.includes(s.id)?<Check className="w-3 h-3"/>:<span className="w-3 h-3"/>}{s.name}</button>))}
                    {filteredSvcs.length===0&&<p className="text-xs text-slate-400 p-2">No services</p>}
                  </div>
                  {selectedSvcs.length>0&&<div className="border-t p-2 flex flex-wrap gap-1">{selectedSvcs.map(s=><span key={s.id} className="inline-flex items-center gap-1 text-[10px] bg-admin-100 text-admin-700 px-1.5 py-0.5 rounded">{s.name}<button type="button" onClick={()=>toggleSvc(s.id)}><X className="w-2.5 h-2.5"/></button></span>)}</div>}
                </div>
              </div>
              <div>
                <label className="label text-xs">Categories</label>
                <div className="border border-slate-200 rounded-lg">
                  <div className="p-2 border-b"><div className="relative"><Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400"/><input type="text" placeholder="Search categories..." value={catSearch} onChange={e=>setCatSearch(e.target.value)} className="w-full pl-8 pr-2 py-1.5 text-xs border-0 focus:outline-none"/>{catSearch&&<button onClick={()=>setCatSearch('')} className="absolute right-2 top-1/2 -translate-y-1/2"><X className="w-3 h-3 text-slate-400"/></button>}</div></div>
                  <div className="max-h-36 overflow-y-auto p-1 space-y-0.5">
                    {filteredCats.map(c=>(<button key={c.id} type="button" onClick={()=>toggleCat(c.id)} className={`w-full text-left px-2 py-1.5 rounded text-xs flex items-center gap-2 ${form.applicableCategories.includes(c.id)?'bg-admin-50 text-admin-700':'hover:bg-slate-50 text-slate-600'}`}>{form.applicableCategories.includes(c.id)?<Check className="w-3 h-3"/>:<span className="w-3 h-3"/>}{c.name}</button>))}
                    {filteredCats.length===0&&<p className="text-xs text-slate-400 p-2">No categories</p>}
                  </div>
                  {selectedCats.length>0&&<div className="border-t p-2 flex flex-wrap gap-1">{selectedCats.map(c=><span key={c.id} className="inline-flex items-center gap-1 text-[10px] bg-admin-100 text-admin-700 px-1.5 py-0.5 rounded">{c.name}<button type="button" onClick={()=>toggleCat(c.id)}><X className="w-2.5 h-2.5"/></button></span>)}</div>}
                </div>
              </div>
            </div>
          </div>

          {/* Exclusions & Settings */}
          <div>
            <h4 className="text-sm font-bold text-slate-800 mb-3">Exclusions & Settings</h4>
            <div className="grid grid-cols-3 gap-3">
              <FormField label="Exclude Discounted" type="toggle" checked={form.excludeDiscounted} onChange={v=>setForm({...form,excludeDiscounted:v})}/>
              <FormField label="Exclude GST/Stamp" type="toggle" checked={form.excludeGST} onChange={v=>setForm({...form,excludeGST:v})}/>
              <FormField label="Exclude Fees" type="toggle" checked={form.excludeFees} onChange={v=>setForm({...form,excludeFees:v})}/>
            </div>
            <div className="grid grid-cols-4 gap-3 mt-3">
              <FormField label="Stackable" type="toggle" checked={form.stackWithOthers} onChange={v=>setForm({...form,stackWithOthers:v})}/>
              <FormField label="Auto Apply" type="toggle" checked={form.autoApply} onChange={v=>setForm({...form,autoApply:v})}/>
              <FormField label="Active" type="toggle" checked={form.isActive} onChange={v=>setForm({...form,isActive:v})}/>
              <FormField label="Show on Website" type="toggle" checked={form.showOnWebsite} onChange={v=>setForm({...form,showOnWebsite:v})}/>
            </div>
          </div>

          {/* Preview */}
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Coupon Preview</h4>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-admin-600 text-white flex items-center justify-center font-bold text-sm">{form.code||'CODE'}</div>
              <div className="flex-1">
                <p className="font-bold text-slate-900">{form.name||form.code||'New Coupon'}</p>
                <p className="text-sm text-slate-500">{discountDisplay}{form.minOrder>0?` · Min order ₹${form.minOrder.toLocaleString('en-IN')}`:''}{form.endDate?` · Until ${new Date(form.endDate).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})}`:''}</p>
                {selectedSvcs.length>0&&<p className="text-xs text-slate-400 mt-1">Applicable: {selectedSvcs.map(s=>s.name).join(', ')}</p>}
              </div>
            </div>
          </div>
        </form>
      </Modal>

      <Modal open={!!deleteConfirm} onClose={()=>setDeleteConfirm(null)} title="Delete Coupon" size="sm" footer={<><button onClick={()=>setDeleteConfirm(null)} className="btn-secondary">Cancel</button><button onClick={()=>deleteConfirm&&handleDelete(deleteConfirm)} className="btn-danger">Delete</button></>}>
        <p className="text-sm text-slate-600">This cannot be undone.</p>
      </Modal>
    </AdminLayout>
  );
}
