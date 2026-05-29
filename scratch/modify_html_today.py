file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State variable
target_state = "            const [crmSearch, setCrmSearch] = useState('');"
rep_state = "            const [crmSearch, setCrmSearch] = useState('');\n            const [crmFilterToday, setCrmFilterToday] = useState(false);"

# 2. fetchCrmOrders
target_fetch = """                    if (crmFilterType) url += `agreement_type=${crmFilterType}&`;
                    if (crmSearch) url += `search=${encodeURIComponent(crmSearch)}&`;"""

rep_fetch = """                    if (crmFilterType) url += `agreement_type=${crmFilterType}&`;
                    if (crmFilterToday) url += `today=true&`;
                    if (crmSearch) url += `search=${encodeURIComponent(crmSearch)}&`;"""

# 3. useEffect
target_effect = "            }, [activeTab, crmFilterStatus, crmFilterType, crmSearch, isAdminLoggedIn]);"
rep_effect = "            }, [activeTab, crmFilterStatus, crmFilterType, crmFilterToday, crmSearch, isAdminLoggedIn]);"

# 4. Analytics Grid & Widget Card
target_grid = """                        {/* Analytics widgets */}
                        {crmAnalytics && (
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-[100px]">
                                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Total Orders</span>"""

rep_grid = """                        {/* Analytics widgets */}
                        {crmAnalytics && (
                            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                                <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-[100px] hover:border-amber-200 transition-colors">
                                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Today's Orders</span>
                                    <div className="flex items-baseline justify-between mt-2">
                                        <span className="text-2xl font-black text-amber-600">{crmAnalytics.today_orders || 0}</span>
                                        <i className="fa-solid fa-calendar-day bg-amber-50 text-amber-600 p-2 rounded-lg text-xs"></i>
                                    </div>
                                </div>
                                <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between h-[100px]">
                                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Total Orders</span>"""

# 5. Filter Button
target_filter = """                            <div className="flex gap-2">
                                <select
                                    value={crmFilterStatus}
                                    onChange={(e) => setCrmFilterStatus(e.target.value)}"""

rep_filter = """                            <div className="flex gap-2">
                                <button
                                    onClick={() => setCrmFilterToday(!crmFilterToday)}
                                    className={`px-3.5 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer border ${
                                        crmFilterToday
                                            ? 'bg-amber-600 border-amber-600 text-white shadow-sm'
                                            : 'bg-slate-50 border-slate-100 text-slate-600 hover:bg-slate-100'
                                    }`}
                                >
                                    <i className="fa-solid fa-calendar-day"></i>
                                    Today Only
                                </button>
                                <select
                                    value={crmFilterStatus}
                                    onChange={(e) => setCrmFilterStatus(e.target.value)}"""

# Replace carriage return differences safely
def safe_replace(text, target, rep):
    if target in text:
        return text.replace(target, rep)
    target_rn = target.replace('\n', '\r\n')
    rep_rn = rep.replace('\n', '\r\n')
    if target_rn in text:
        return text.replace(target_rn, rep_rn)
    print(f"Failed to find target block: {target[:50]}...")
    return text

content = safe_replace(content, target_state, rep_state)
content = safe_replace(content, target_fetch, rep_fetch)
content = safe_replace(content, target_effect, rep_effect)
content = safe_replace(content, target_grid, rep_grid)
content = safe_replace(content, target_filter, rep_filter)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Today's orders modification script completed.")
