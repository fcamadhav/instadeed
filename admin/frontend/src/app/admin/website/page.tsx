'use client';

import { useState, useEffect, FormEvent } from 'react';
import AdminLayout from '@/components/AdminLayout';
import FormField from '@/components/FormField';
import Modal from '@/components/Modal';
import { apiGet, apiPut } from '@/lib/api';
import toast from 'react-hot-toast';
import { Save, Globe, Home, Info, HelpCircle, MessageSquare, Mail as MailIcon, Settings, Plus, Trash2, Loader2 } from 'lucide-react';

interface FAQ { question: string; answer: string }
interface Testimonial { name: string; role: string; content: string; avatar: string }

interface WebsiteContent {
  homepageBanner?: { title: string; subtitle: string; ctaText: string; ctaUrl: string };
  hero?: { title: string; subtitle: string; backgroundImage: string };
  about?: { title: string; content: string; mission: string; vision: string };
  faqs?: FAQ[];
  testimonials?: Testimonial[];
  contact?: { email: string; phone: string; address: string; mapEmbedUrl: string };
  footer?: { companyName: string; tagline: string; socialLinks: { platform: string; url: string }[] };
  seo?: { metaTitle: string; metaDescription: string; ogImage: string; googleAnalyticsId: string };
}

const sections = [
  { key: 'homepageBanner', label: 'Homepage Banner', icon: Home },
  { key: 'hero', label: 'Hero', icon: Globe },
  { key: 'about', label: 'About', icon: Info },
  { key: 'faqs', label: 'FAQs', icon: HelpCircle },
  { key: 'testimonials', label: 'Testimonials', icon: MessageSquare },
  { key: 'contact', label: 'Contact', icon: MailIcon },
  { key: 'footer', label: 'Footer', icon: Settings },
  { key: 'seo', label: 'SEO', icon: Globe },
];

export default function WebsitePage() {
  const [activeSection, setActiveSection] = useState('homepageBanner');
  const [content, setContent] = useState<WebsiteContent>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchContent(); }, []);

  const fetchContent = async () => {
    setLoading(true);
    try {
      const res = await apiGet<{ data: { content: WebsiteContent } }>('/admin/website/content');
      if (res.data?.content) setContent(res.data.content);
    } catch { toast.error('Failed to load website content'); } finally { setLoading(false); }
  };

  const updateSection = (section: string, data: any) => {
    setContent(prev => ({ ...prev, [section]: data }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await apiPut('/admin/website/content', content);
      toast.success('Content saved');
    } catch (err: any) { toast.error(err.message); } finally { setSaving(false); }
  };

  const renderSection = () => {
    switch (activeSection) {
      case 'homepageBanner': {
        const data = content.homepageBanner || { title: '', subtitle: '', ctaText: '', ctaUrl: '' };
        return (
          <div className="space-y-4">
            <FormField label="Title" value={data.title} onChange={e => updateSection('homepageBanner', { ...data, title: e.target.value })} />
            <FormField label="Subtitle" value={data.subtitle} onChange={e => updateSection('homepageBanner', { ...data, subtitle: e.target.value })} />
            <div className="grid grid-cols-2 gap-4">
              <FormField label="CTA Text" value={data.ctaText} onChange={e => updateSection('homepageBanner', { ...data, ctaText: e.target.value })} />
              <FormField label="CTA URL" value={data.ctaUrl} onChange={e => updateSection('homepageBanner', { ...data, ctaUrl: e.target.value })} />
            </div>
          </div>
        );
      }
      case 'hero': {
        const data = content.hero || { title: '', subtitle: '', backgroundImage: '' };
        return (
          <div className="space-y-4">
            <FormField label="Title" value={data.title} onChange={e => updateSection('hero', { ...data, title: e.target.value })} />
            <FormField label="Subtitle" type="textarea" value={data.subtitle} onChange={e => updateSection('hero', { ...data, subtitle: e.target.value })} />
            <FormField label="Background Image URL" value={data.backgroundImage} onChange={e => updateSection('hero', { ...data, backgroundImage: e.target.value })} />
          </div>
        );
      }
      case 'about': {
        const data = content.about || { title: '', content: '', mission: '', vision: '' };
        return (
          <div className="space-y-4">
            <FormField label="Title" value={data.title} onChange={e => updateSection('about', { ...data, title: e.target.value })} />
            <FormField label="Content" type="textarea" value={data.content} onChange={e => updateSection('about', { ...data, content: e.target.value })} rows={6} />
            <FormField label="Mission" type="textarea" value={data.mission} onChange={e => updateSection('about', { ...data, mission: e.target.value })} />
            <FormField label="Vision" type="textarea" value={data.vision} onChange={e => updateSection('about', { ...data, vision: e.target.value })} />
          </div>
        );
      }
      case 'faqs': {
        const faqs = content.faqs || [];
        return (
          <div className="space-y-3">
            {faqs.map((faq, i) => (
              <div key={i} className="border border-slate-200 dark:border-slate-700 rounded-lg p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">FAQ #{i + 1}</span>
                  <button onClick={() => updateSection('faqs', faqs.filter((_, j) => j !== i))} className="text-red-400 hover:text-red-600"><Trash2 className="w-4 h-4" /></button>
                </div>
                <FormField label="Question" value={faq.question} onChange={e => {
                  const updated = [...faqs]; updated[i] = { ...updated[i], question: e.target.value }; updateSection('faqs', updated);
                }} />
                <FormField label="Answer" type="textarea" value={faq.answer} onChange={e => {
                  const updated = [...faqs]; updated[i] = { ...updated[i], answer: e.target.value }; updateSection('faqs', updated);
                }} />
              </div>
            ))}
            <button onClick={() => updateSection('faqs', [...faqs, { question: '', answer: '' }])} className="btn-secondary btn-sm"><Plus className="w-3 h-3" /> Add FAQ</button>
          </div>
        );
      }
      case 'testimonials': {
        const testimonials = content.testimonials || [];
        return (
          <div className="space-y-3">
            {testimonials.map((t, i) => (
              <div key={i} className="border border-slate-200 dark:border-slate-700 rounded-lg p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Testimonial #{i + 1}</span>
                  <button onClick={() => updateSection('testimonials', testimonials.filter((_, j) => j !== i))} className="text-red-400 hover:text-red-600"><Trash2 className="w-4 h-4" /></button>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <FormField label="Name" value={t.name} onChange={e => { const u = [...testimonials]; u[i] = { ...u[i], name: e.target.value }; updateSection('testimonials', u); }} />
                  <FormField label="Role" value={t.role} onChange={e => { const u = [...testimonials]; u[i] = { ...u[i], role: e.target.value }; updateSection('testimonials', u); }} />
                </div>
                <FormField label="Content" type="textarea" value={t.content} onChange={e => { const u = [...testimonials]; u[i] = { ...u[i], content: e.target.value }; updateSection('testimonials', u); }} />
                <FormField label="Avatar URL" value={t.avatar} onChange={e => { const u = [...testimonials]; u[i] = { ...u[i], avatar: e.target.value }; updateSection('testimonials', u); }} />
              </div>
            ))}
            <button onClick={() => updateSection('testimonials', [...testimonials, { name: '', role: '', content: '', avatar: '' }])} className="btn-secondary btn-sm"><Plus className="w-3 h-3" /> Add Testimonial</button>
          </div>
        );
      }
      case 'contact': {
        const data = content.contact || { email: '', phone: '', address: '', mapEmbedUrl: '' };
        return (
          <div className="space-y-4">
            <FormField label="Email" value={data.email} onChange={e => updateSection('contact', { ...data, email: e.target.value })} />
            <FormField label="Phone" value={data.phone} onChange={e => updateSection('contact', { ...data, phone: e.target.value })} />
            <FormField label="Address" type="textarea" value={data.address} onChange={e => updateSection('contact', { ...data, address: e.target.value })} />
            <FormField label="Map Embed URL" value={data.mapEmbedUrl} onChange={e => updateSection('contact', { ...data, mapEmbedUrl: e.target.value })} />
          </div>
        );
      }
      case 'footer': {
        const data = content.footer || { companyName: '', tagline: '', socialLinks: [] };
        return (
          <div className="space-y-4">
            <FormField label="Company Name" value={data.companyName} onChange={e => updateSection('footer', { ...data, companyName: e.target.value })} />
            <FormField label="Tagline" type="textarea" value={data.tagline} onChange={e => updateSection('footer', { ...data, tagline: e.target.value })} />
            <div>
              <label className="label">Social Links</label>
              {(data.socialLinks || []).map((link, i) => (
                <div key={i} className="flex items-center gap-2 mb-2">
                  <input value={link.platform} onChange={e => {
                    const links = [...(data.socialLinks || [])]; links[i] = { ...links[i], platform: e.target.value };
                    updateSection('footer', { ...data, socialLinks: links });
                  }} className="input flex-1 text-sm" placeholder="Platform" />
                  <input value={link.url} onChange={e => {
                    const links = [...(data.socialLinks || [])]; links[i] = { ...links[i], url: e.target.value };
                    updateSection('footer', { ...data, socialLinks: links });
                  }} className="input flex-1 text-sm" placeholder="URL" />
                  <button onClick={() => updateSection('footer', { ...data, socialLinks: data.socialLinks.filter((_, j) => j !== i) })} className="text-red-400"><Trash2 className="w-4 h-4" /></button>
                </div>
              ))}
              <button onClick={() => updateSection('footer', { ...data, socialLinks: [...(data.socialLinks || []), { platform: '', url: '' }] })} className="btn-secondary btn-sm"><Plus className="w-3 h-3" /> Add Link</button>
            </div>
          </div>
        );
      }
      case 'seo': {
        const data = content.seo || { metaTitle: '', metaDescription: '', ogImage: '', googleAnalyticsId: '' };
        return (
          <div className="space-y-4">
            <FormField label="Meta Title" value={data.metaTitle} onChange={e => updateSection('seo', { ...data, metaTitle: e.target.value })} />
            <FormField label="Meta Description" type="textarea" value={data.metaDescription} onChange={e => updateSection('seo', { ...data, metaDescription: e.target.value })} />
            <FormField label="OG Image URL" value={data.ogImage} onChange={e => updateSection('seo', { ...data, ogImage: e.target.value })} />
            <FormField label="Google Analytics ID" value={data.googleAnalyticsId} onChange={e => updateSection('seo', { ...data, googleAnalyticsId: e.target.value })} />
          </div>
        );
      }
      default:
        return null;
    }
  };

  if (loading) return <AdminLayout title="Website"><div className="card p-8 text-center"><Loader2 className="w-6 h-6 animate-spin text-admin-600 mx-auto" /></div></AdminLayout>;

  return (
    <AdminLayout title="Website Content">
      <div className="flex flex-col lg:flex-row gap-6">
        <div className="lg:w-56 flex-shrink-0">
          <nav className="card p-1 space-y-0.5">
            {sections.map(s => {
              const Icon = s.icon;
              return (
                <button key={s.key} onClick={() => setActiveSection(s.key)} className={`flex items-center gap-2 w-full px-3 py-2 text-sm rounded-lg text-left transition-colors ${activeSection === s.key ? 'bg-admin-50 dark:bg-admin-900/30 text-admin-700 dark:text-admin-300 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50'}`}>
                  <Icon className="w-4 h-4" /> {s.label}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="flex-1">
          <div className="card p-6">
            <h3 className="section-title mb-4 capitalize">{activeSection.replace(/([A-Z])/g, ' $1').trim()} Settings</h3>
            {renderSection()}
            <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
              <button onClick={handleSave} disabled={saving} className="btn-primary"><Save className="w-4 h-4" /> {saving ? 'Saving...' : 'Save Section'}</button>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}
