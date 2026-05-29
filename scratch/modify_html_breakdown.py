file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the space between widgets closing div and Search & Filters
# We want to find:
#                                 </div>
#                             </div>
#                         )}
# 
#                         {/* Search & Filters */}
# 
# And replace with:
#                                 </div>
#                             </div>
#                         )}
# 
#                         {/* Agreement Type Breakdown */}
#                         ...
# 
#                         {/* Search & Filters */}

target = """                                </div>
                            </div>
                        )}

                        {/* Search & Filters */}"""

breakdown_code = """                                </div>
                            </div>
                        )}

                        {/* Agreement Type Breakdown */}
                        <div className="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm space-y-4">
                            <div>
                                <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                                    <i className="fa-solid fa-list-check text-indigo-600"></i>
                                    Agreement Formats Performance (Today vs. Queue)
                                </h3>
                                <p className="text-[11px] text-slate-400 font-medium">Real-time status breakdown per document type</p>
                            </div>
                            
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="bg-slate-50 border-b border-slate-100 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                                            <th className="px-4 py-2.5">Agreement Type</th>
                                            <th className="px-4 py-2.5 text-center">Today's Orders</th>
                                            <th className="px-4 py-2.5 text-center">Pending Queue</th>
                                            <th className="px-4 py-2.5 text-center">Total Drafted</th>
                                            <th className="px-4 py-2.5 text-right">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-50 text-xs">
                                        {[
                                            { type: 'RENT', label: 'Rent Agreement', icon: 'fa-file-signature', color: 'blue' },
                                            { type: 'ATS', label: 'Agreement to Sell', icon: 'fa-file-contract', color: 'purple' },
                                            { type: 'REG_RENT', label: 'Registered Rent Agreement', icon: 'fa-stamp', color: 'indigo' },
                                            { type: 'MUTATION', label: 'Mutation Form', icon: 'fa-file-pen', color: 'emerald' },
                                            { type: 'GNIDA', label: 'GNIDA KYC / KYA', icon: 'fa-id-card', color: 'yellow' },
                                            { type: 'GNIDA_REGISTRY', label: 'GNIDA Registry Format', icon: 'fa-book', color: 'cyan' },
                                            { type: 'GNIDA_PTM', label: 'Permission to Mortgage', icon: 'fa-file-contract', color: 'rose' },
                                            { type: 'TM48', label: 'TM-48 Authority', icon: 'fa-trademark', color: 'orange' }
                                        ].map(item => {
                                            const details = crmAnalytics?.agreement_details?.[item.type] || { today: 0, pending: 0, total: 0 };
                                            return (
                                                <tr key={item.type} className="hover:bg-slate-50/50 transition">
                                                    <td className="px-4 py-3 flex items-center gap-2.5">
                                                        <div className={`w-7 h-7 rounded-lg bg-${item.color}-50 text-${item.color}-600 flex items-center justify-center`}>
                                                            <i className={`fa-solid ${item.icon} text-xs`}></i>
                                                        </div>
                                                        <span className="font-bold text-slate-700">{item.label}</span>
                                                    </td>
                                                    <td className="px-4 py-3 text-center">
                                                        <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
                                                            details.today > 0 ? 'bg-emerald-50 text-emerald-700 font-extrabold animate-pulse' : 'bg-slate-50 text-slate-400'
                                                        }`}>
                                                            {details.today}
                                                        </span>
                                                    </td>
                                                    <td className="px-4 py-3 text-center">
                                                        <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
                                                            details.pending > 0 ? 'bg-amber-50 text-amber-700' : 'bg-slate-50 text-slate-400'
                                                        }`}>
                                                            {details.pending}
                                                        </span>
                                                    </td>
                                                    <td className="px-4 py-3 text-center font-bold text-slate-600">
                                                        {details.total}
                                                    </td>
                                                    <td className="px-4 py-3 text-right">
                                                        <button
                                                            onClick={() => { setActiveTab(item.type); }}
                                                            className="px-2 py-1 bg-slate-50 border border-slate-200 hover:bg-indigo-50 hover:border-indigo-100 hover:text-indigo-600 rounded-lg text-[10px] font-bold text-slate-600 transition cursor-pointer"
                                                        >
                                                            New Draft
                                                        </button>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Search & Filters */}"""

if target in content:
    content = content.replace(target, breakdown_code)
    print("Replaced successfully with LF line endings.")
else:
    target_rn = target.replace('\n', '\r\n')
    breakdown_code_rn = breakdown_code.replace('\n', '\r\n')
    if target_rn in content:
        content = content.replace(target_rn, breakdown_code_rn)
        print("Replaced successfully with CRLF line endings.")
    else:
        print("Target pattern not found in file!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished modify_html_breakdown execution.")
