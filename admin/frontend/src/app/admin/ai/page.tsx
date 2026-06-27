'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import FormField from '@/components/FormField';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, Brain, Scan, Loader2 } from 'lucide-react';

interface AISettings {
  provider: string;
  model: string;
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
  retryCount: number;
  fallbackModel: string;
  enabled: boolean;
}

interface OCRSettings {
  enabled: boolean;
  supportedDocuments: { type: string; fields: { name: string; type: string; required: boolean }[] }[];
}

export default function AIPage() {
  const [tab, setTab] = useState<'ai' | 'ocr'>('ai');
  const [aiSettings, setAiSettings] = useState<AISettings>({
    provider: 'openai', model: 'gpt-4', temperature: 0.7, maxTokens: 2048,
    systemPrompt: '', retryCount: 2, fallbackModel: 'gpt-3.5-turbo', enabled: true,
  });
  const [ocrSettings, setOcrSettings] = useState<OCRSettings>({ enabled: true, supportedDocuments: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [aiForm, setAiForm] = useState(aiSettings);
  const [ocrForm, setOcrForm] = useState(ocrSettings);

  useEffect(() => { fetchSettings(); }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      const [aiRes, ocrRes] = await Promise.all([
        apiGet<{ data: { settings: AISettings } }>('/admin/ai/settings').catch(() => null),
        apiGet<{ data: { settings: OCRSettings } }>('/admin/ocr/settings').catch(() => null),
      ]);
      if (aiRes?.data?.settings) { setAiSettings(aiRes.data.settings); setAiForm(aiRes.data.settings); }
      if (ocrRes?.data?.settings) { setOcrSettings(ocrRes.data.settings); setOcrForm(ocrRes.data.settings); }
    } catch {} finally { setLoading(false); }
  };

  const saveAI = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try { await apiPut('/admin/ai/settings', aiForm); toast.success('AI settings saved'); } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const saveOCR = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try { await apiPut('/admin/ocr/settings', ocrForm); toast.success('OCR settings saved'); } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  if (loading) return <AdminLayout title="AI Settings"><div className="card p-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div></AdminLayout>;

  return (
    <AdminLayout title="AI & OCR Settings">
      <div className="flex gap-1 bg-slate-100 dark:bg-slate-700 rounded-lg p-1 mb-6 w-fit">
        <button onClick={() => setTab('ai')} className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${tab === 'ai' ? 'bg-white dark:bg-slate-800 shadow-sm text-admin-600 dark:text-admin-400 font-medium' : 'text-slate-500'}`}><Brain className="w-3.5 h-3.5" /> AI Settings</button>
        <button onClick={() => setTab('ocr')} className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${tab === 'ocr' ? 'bg-white dark:bg-slate-800 shadow-sm text-admin-600 dark:text-admin-400 font-medium' : 'text-slate-500'}`}><Scan className="w-3.5 h-3.5" /> OCR Settings</button>
      </div>

      {tab === 'ai' ? (
        <div className="card p-6 max-w-2xl">
          <h3 className="section-title mb-4">AI Configuration</h3>
          <form onSubmit={saveAI} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField type="select" label="Provider" value={aiForm.provider} onChange={e => setAiForm({ ...aiForm, provider: e.target.value })} options={[{ value: 'openai', label: 'OpenAI' }, { value: 'anthropic', label: 'Anthropic' }, { value: 'google', label: 'Google AI' }, { value: 'azure', label: 'Azure OpenAI' }]} />
              <FormField label="Model" value={aiForm.model} onChange={e => setAiForm({ ...aiForm, model: e.target.value })} placeholder="gpt-4" />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="label">Temperature: {aiForm.temperature}</label>
                <input type="range" min="0" max="2" step="0.1" value={aiForm.temperature} onChange={e => setAiForm({ ...aiForm, temperature: parseFloat(e.target.value) })} className="w-full" />
              </div>
              <FormField label="Max Tokens" type="number" value={aiForm.maxTokens} onChange={e => setAiForm({ ...aiForm, maxTokens: parseInt(e.target.value) || 2048 })} />
              <FormField label="Retry Count" type="number" value={aiForm.retryCount} onChange={e => setAiForm({ ...aiForm, retryCount: parseInt(e.target.value) || 2 })} />
            </div>
            <FormField label="Fallback Model" value={aiForm.fallbackModel} onChange={e => setAiForm({ ...aiForm, fallbackModel: e.target.value })} />
            <FormField label="System Prompt" type="textarea" value={aiForm.systemPrompt} onChange={e => setAiForm({ ...aiForm, systemPrompt: e.target.value })} rows={5} />
            <FormField label="Enable AI Features" type="toggle" checked={aiForm.enabled} onChange={v => setAiForm({ ...aiForm, enabled: v })} />
            <button type="submit" disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save AI Settings'}</button>
          </form>
        </div>
      ) : (
        <div className="card p-6 max-w-2xl">
          <h3 className="section-title mb-4">OCR Configuration</h3>
          <form onSubmit={saveOCR} className="space-y-6">
            <FormField label="Enable OCR" type="toggle" checked={ocrForm.enabled} onChange={v => setOcrForm({ ...ocrForm, enabled: v })} />

            <div>
              <label className="label">Supported Documents</label>
              {ocrForm.supportedDocuments.map((doc, idx) => (
                <div key={idx} className="border border-slate-200 dark:border-slate-700 rounded-lg p-4 mb-3">
                  <div className="flex items-center justify-between mb-2">
                    <FormField label="Document Type" value={doc.type} onChange={e => {
                      const docs = [...ocrForm.supportedDocuments];
                      docs[idx].type = e.target.value;
                      setOcrForm({ ...ocrForm, supportedDocuments: docs });
                    }} />
                  </div>
                  <div>
                    <label className="label text-xs">Fields</label>
                    {doc.fields.map((field, fi) => (
                      <div key={fi} className="flex items-center gap-2 mb-1">
                        <input value={field.name} onChange={e => {
                          const docs = [...ocrForm.supportedDocuments];
                          docs[idx].fields[fi].name = e.target.value;
                          setOcrForm({ ...ocrForm, supportedDocuments: docs });
                        }} className="input flex-1 text-sm" placeholder="Field name" />
                        <select value={field.type} onChange={e => {
                          const docs = [...ocrForm.supportedDocuments];
                          docs[idx].fields[fi].type = e.target.value;
                          setOcrForm({ ...ocrForm, supportedDocuments: docs });
                        }} className="select w-28 text-sm">
                          <option value="text">Text</option>
                          <option value="date">Date</option>
                          <option value="number">Number</option>
                        </select>
                      </div>
                    ))}
                    <button type="button" onClick={() => {
                      const docs = [...ocrForm.supportedDocuments];
                      docs[idx].fields.push({ name: '', type: 'text', required: false });
                      setOcrForm({ ...ocrForm, supportedDocuments: docs });
                    }} className="text-xs text-admin-600 mt-1">+ Add Field</button>
                  </div>
                </div>
              ))}
              <button type="button" onClick={() => setOcrForm({ ...ocrForm, supportedDocuments: [...ocrForm.supportedDocuments, { type: '', fields: [] }] })} className="btn-secondary btn-sm">+ Add Document Type</button>
            </div>

            <button type="submit" disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save OCR Settings'}</button>
          </form>
        </div>
      )}
    </AdminLayout>
  );
}
