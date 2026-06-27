'use client';

import { useState, useEffect } from 'react';
import AdminLayout from '@/components/AdminLayout';
import { apiGet } from '@/lib/api';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';

export default function RentAgreementCalendarPage() {
  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [events, setEvents] = useState<Record<string, any[]>>({});
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchCalendar(); }, [year, month]);

  const fetchCalendar = async () => {
    setLoading(true);
    try {
      const r = await apiGet<any>(`/admin/rent-agreements/calendar?year=${year}&month=${month}`);
      const grouped: Record<string, any[]> = {};
      for (const a of r.data.agreements) {
        const d = new Date(a.endDate).toISOString().split('T')[0];
        if (!grouped[d]) grouped[d] = [];
        grouped[d].push(a);
      }
      setEvents(grouped);
    } catch {}
    setLoading(false);
  };

  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDay = new Date(year, month - 1, 1).getDay();
  const today = new Date().toISOString().split('T')[0];

  const prev = () => { if (month === 1) { setYear(y => y - 1); setMonth(12); } else setMonth(m => m - 1); };
  const next = () => { if (month === 12) { setYear(y => y + 1); setMonth(1); } else setMonth(m => m + 1); };

  const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];

  return (
    <AdminLayout title="Rent Agreement Calendar">
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Rent Agreement Calendar</h1>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-6">
            <button onClick={prev} className="btn-secondary btn-sm p-2"><ChevronLeft className="w-4 h-4" /></button>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">{monthNames[month - 1]} {year}</h2>
            <button onClick={next} className="btn-secondary btn-sm p-2"><ChevronRight className="w-4 h-4" /></button>
          </div>

          <div className="grid grid-cols-7 gap-1">
            {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(d => (
              <div key={d} className="text-center text-xs font-semibold text-slate-500 py-2">{d}</div>
            ))}
            {Array.from({ length: firstDay }).map((_, i) => <div key={`e${i}`} />)}
            {Array.from({ length: daysInMonth }).map((_, i) => {
              const d = i + 1;
              const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
              const dayEvents = events[dateStr] || [];
              const isToday = dateStr === today;
              const hasExpired = dayEvents.some(a => a.renewalStatus !== 'RENEWED' && new Date(a.endDate) < new Date());
              return (
                <button key={d} onClick={() => setSelectedDate(selectedDate === dateStr ? null : dateStr)}
                  className={`p-2 rounded-lg text-sm transition-colors relative ${
                    isToday ? 'bg-admin-100 dark:bg-admin-900/30 ring-2 ring-admin-600' : 'hover:bg-slate-100 dark:hover:bg-slate-700'
                  } ${selectedDate === dateStr ? 'ring-2 ring-admin-600' : ''}`}>
                  <span className={isToday ? 'font-bold text-admin-700 dark:text-admin-300' : 'text-slate-700 dark:text-slate-300'}>{d}</span>
                  {dayEvents.length > 0 && (
                    <div className={`absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full ${
                      hasExpired ? 'bg-red-500' : 'bg-orange-400'
                    }`} />
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {selectedDate && (
          <div className="card p-4">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-3">
              Expiring on {new Date(selectedDate).toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </h3>
            {(events[selectedDate] || []).length > 0 ? (
              <div className="space-y-2">
                {events[selectedDate].map((a: any) => (
                  <div key={a.id} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg">
                    <div>
                      <div className="text-sm font-medium text-slate-900 dark:text-white">{a.agreementId} - {a.customerName}</div>
                      <div className="text-xs text-slate-500">Ends: {new Date(a.endDate).toLocaleDateString('en-IN')}</div>
                    </div>
                    <span className={`badge ${a.renewalStatus === 'RENEWED' ? 'badge-green' : 'badge-orange'}`}>{a.renewalStatus}</span>
                  </div>
                ))}
              </div>
            ) : <p className="text-sm text-slate-500">No agreements expiring on this date.</p>}
          </div>
        )}
      </div>
    </AdminLayout>
  );
}
