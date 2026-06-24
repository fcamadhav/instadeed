import sys
import os

def main():
    jsx_file = "test_script.jsx"
    
    if not os.path.exists(jsx_file):
        print(f"Error: {jsx_file} not found.")
        return
        
    with open(jsx_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = "const renderCrmDashboard = () => {"
    end_tag = "const shareDocTypes = ["
    
    start_idx = content.find(start_tag)
    if start_idx == -1:
        print("Error: Could not find start tag.")
        return
        
    end_idx = content.find(end_tag, start_idx)
    if end_idx == -1:
        print("Error: Could not find end tag.")
        return
        
    # We want to replace from start_idx up to end_idx.
    # The new function will be inserted, followed by a newline and then the end_tag.
    
    new_code = """const renderCrmDashboard = () => {
                if (!isAdminLoggedIn) {
                    return (
                        <div className="w-full max-w-md mx-auto my-12 px-6 animate-in fade-in duration-200">
                            <div className="bg-white rounded-2xl border shadow-sm p-8 text-center" style={{ borderColor: C.line }}>
                                <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-sm" style={{ color: C.accent, backgroundColor: C.accentSoft }}>
                                    <i className="fa-solid fa-shield-halved text-2xl"></i>
                                </div>
                                <h2 className="text-xl font-extrabold mb-1" style={{ color: C.ink }}>Admin Access</h2>
                                <p className="text-xs mb-6" style={{ color: C.muted }}>Sign in with your admin email to access the control panel</p>
                                <button onClick={() => setShowLogin(true)} className="w-full py-3 text-white rounded-xl font-bold text-sm transition shadow-lg cursor-pointer crm-btn-primary" style={{ backgroundColor: C.accent }}>
                                    <i className="fa-solid fa-right-to-bracket mr-1.5"></i> Sign In
                                </button>
                            </div>
                        </div>
                    );
                }

                // nav items
                const navItems = [
                    { key: "dashboard", label: "Dashboard", icon: "fa-chart-line", action: () => { setCrmView('dashboard'); fetchCrmOrders(); fetchCrmAnalytics(); fetchCrmCustomers(); } },
                    { key: "orders", label: "Agreements", icon: "fa-file-signature", action: () => { setCrmView('orders'); fetchCrmOrders(); } },
                    { key: "customers", label: "Customers", icon: "fa-users", action: () => { setCrmView('customers'); fetchCrmCustomers(); } },
                    { key: "users", label: "Users", icon: "fa-user-plus", action: () => { setCrmView('users'); fetchCrmUsers(); } },
                    { key: "kanban", label: "Pipeline", icon: "fa-columns", action: () => { setCrmView('kanban'); fetchCrmOrders(); } },
                    { key: "coupons", label: "Coupons", icon: "fa-tags", action: () => { setCrmView('coupons'); fetchCrmCoupons(); } },
                    { key: "invoices", label: "Invoices", icon: "fa-file-invoice-dollar", action: () => { setCrmView('invoices'); fetchCrmInvoices(); } },
                    { key: "notifications", label: "Alerts", icon: "fa-bell", action: () => { setCrmView('notifications'); fetchCrmNotifications(); fetchExpiringRentals(); } },
                    { key: "activity", label: "Activity Logs", icon: "fa-shoe-prints", action: () => { setCrmView('activity'); loadTrackedEvents(); fetchCrmAudit(); } },
                    { key: "analytics", label: "Reports", icon: "fa-chart-pie", action: () => { setCrmView('analytics'); fetchCrmAnalyticsExtras(); } },
                    { key: "staff", label: "Staff", icon: "fa-user-tie", action: () => { setCrmView('staff'); fetchCrmStaff(); } },
                ];

                // sub view rendering functions
                const renderDashboardView = () => {
                    const stats = [
                        { label: "Today's Orders", value: crmAnalytics?.today_orders || 0, icon: "fa-calendar-day", tint: C.info },
                        { label: "Total Orders", value: crmAnalytics?.total_orders || 0, icon: "fa-folder", tint: C.muted },
                        { label: "Completed Orders", value: (crmAnalytics?.status_breakdown?.COMPLETED || 0) + (crmAnalytics?.status_breakdown?.SIGNED || 0), icon: "fa-circle-check", tint: C.success },
                        { label: "Total Revenue", value: `₹${(crmAnalytics?.total_revenue || 0).toLocaleString('en-IN')}`, icon: "fa-indian-rupee-sign", tint: C.accent },
                    ];

                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Dashboard</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Real-time overview of document drafting volume and sales</p>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
                                {stats.map(s => (
                                    <div key={s.label} className="crm-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <div>
                                            <div style={{ fontSize: '11px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>{s.label}</div>
                                            <div style={{ fontSize: '26px', fontWeight: 800, color: C.ink, marginTop: '4px' }}>{s.value}</div>
                                        </div>
                                        <div style={{ width: '40px', height: '40px', borderRadius: '10px', backgroundColor: s.tint + '15', color: s.tint, display: 'grid', placeItems: 'center' }}>
                                            <i className={`fa-solid ${s.icon} text-lg`}></i>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {expiringRentals && (expiringRentals.expiring.length > 0 || expiringRentals.expired.length > 0) && (
                                <div className="crm-card" style={{ borderLeft: `4px solid ${C.gold}`, backgroundColor: '#FAF6EE' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                        <i className="fa-solid fa-clock" style={{ color: C.gold }}></i>
                                        <span style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}>Rent Agreement Expiry Alert</span>
                                    </div>
                                    <p style={{ fontSize: '12px', color: C.muted }}>
                                        There are {expiringRentals.expiring.length} agreements expiring soon and {expiringRentals.expired.length} agreements already expired.
                                    </p>
                                    <button onClick={() => { setCrmView('notifications'); fetchExpiringRentals(); }} className="crm-btn-ghost" style={{ marginTop: '10px', padding: '6px 12px', fontSize: '11px' }}>
                                        View Alerts
                                    </button>
                                </div>
                            )}

                            <div className="crm-table-container">
                                <div style={{ padding: '16px 20px', borderBottom: `1px solid ${C.line}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <span style={{ fontWeight: 800, color: C.ink, fontSize: '14px' }}>Recent Agreements</span>
                                    <button onClick={() => setCrmView('orders')} className="crm-btn-ghost" style={{ padding: '6px 12px', fontSize: '11px' }}>View All</button>
                                </div>
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Client Name</th>
                                                <th>Format Type</th>
                                                <th>Amount</th>
                                                <th>Status</th>
                                                <th style={{ textAlign: 'right' }}>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmOrders.slice(0, 5).map(order => (
                                                <tr key={order.id}>
                                                    <td style={{ fontWeight: 700 }}>
                                                        <div>{order.customer_name}</div>
                                                        <div style={{ fontSize: '10px', color: C.muted, fontWeight: 500 }}>{order.id}</div>
                                                    </td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, color: C.muted }}>{order.agreement_type}</span>
                                                    </td>
                                                    <td style={{ fontWeight: 800 }}>₹{order.amount}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{
                                                            backgroundColor: order.status === 'COMPLETED' || order.status === 'SIGNED' ? '#E8F5E9' : order.status === 'PENDING_PAYMENT' ? '#FFF3E0' : '#E3F2FD',
                                                            color: order.status === 'COMPLETED' || order.status === 'SIGNED' ? '#2E7D32' : order.status === 'PENDING_PAYMENT' ? '#E65100' : '#1565C0'
                                                        }}>{order.status}</span>
                                                    </td>
                                                    <td style={{ textAlign: 'right' }}>
                                                        <button onClick={() => setCrmSelectedOrderForDetail(order)} className="crm-btn-ghost" style={{ padding: '5px 10px', fontSize: '11px' }}>
                                                            Detail <i className="fa-solid fa-chevron-right"></i>
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                            {crmOrders.length === 0 && (
                                                <tr><td colSpan="5" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No orders found</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderOrdersView = () => {
                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Agreements DB</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Search, track, assign staff and generate e-signatures for drafted agreements</p>
                            </div>

                            {/* Filters bar */}
                            <div className="crm-card flex flex-col sm:flex-row gap-3" style={{ padding: '16px', display: 'flex', gap: '12px' }}>
                                <div style={{ flex: 1, position: 'relative' }}>
                                    <i className="fa-solid fa-magnifying-glass" style={{ position: 'absolute', left: '14px', top: '14px', color: C.muted, fontSize: '12px' }}></i>
                                    <input
                                        type="text"
                                        placeholder="Search by client name, phone, email, or order ID..."
                                        value={crmSearch}
                                        onChange={(e) => setCrmSearch(e.target.value)}
                                        className="crm-input w-full"
                                        style={{ paddingLeft: '36px' }}
                                    />
                                </div>
                                <div style={{ display: 'flex', gap: '10px' }}>
                                    <button
                                        onClick={() => setCrmFilterToday(!crmFilterToday)}
                                        className={`crm-btn-ghost ${crmFilterToday ? 'active' : ''}`}
                                        style={{
                                            backgroundColor: crmFilterToday ? C.accentSoft : 'transparent',
                                            color: crmFilterToday ? C.accent : C.ink,
                                            borderColor: crmFilterToday ? C.accent : C.line
                                        }}
                                    >
                                        <i className="fa-solid fa-calendar-day"></i> Today
                                    </button>
                                    <select
                                        value={crmFilterStatus}
                                        onChange={(e) => setCrmFilterStatus(e.target.value)}
                                        className="crm-select"
                                    >
                                        <option value="">All Statuses</option>
                                        <option value="PENDING_PAYMENT">Pending Payment</option>
                                        <option value="PAID">Paid / Ready</option>
                                        <option value="DRAFTED">Drafted</option>
                                        <option value="COMPLETED">Completed</option>
                                        <option value="SIGNED">Signed</option>
                                    </select>
                                    <select
                                        value={crmFilterType}
                                        onChange={(e) => setCrmFilterType(e.target.value)}
                                        className="crm-select"
                                    >
                                        <option value="">All Formats</option>
                                        <option value="RENT">Rent Agreement</option>
                                        <option value="ATS">Agreement to Sell</option>
                                        <option value="REG_RENT">Registered Rent</option>
                                        <option value="MUTATION">Mutation Form</option>
                                        <option value="GNIDA">GNIDA KYC</option>
                                        <option value="GNIDA_REGISTRY">GNIDA Registry</option>
                                        <option value="GNIDA_PTM">Permission to Mortgage</option>
                                        <option value="TM48">TM-48 Auth</option>
                                    </select>
                                </div>
                            </div>

                            {/* Orders Table */}
                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Order Details</th>
                                                <th>Client Contact</th>
                                                <th>Agreement</th>
                                                <th>Source</th>
                                                <th>Amount</th>
                                                <th>Cloud Vault</th>
                                                <th>Status</th>
                                                <th style={{ textAlign: 'right' }}>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmOrders.length === 0 ? (
                                                <tr>
                                                    <td colSpan="8" style={{ padding: '40px', textAlign: 'center', color: C.muted }}>
                                                        <i className="fa-solid fa-folder-open text-2xl mb-2 block opacity-40"></i>
                                                        No matching agreements found in database
                                                    </td>
                                                </tr>
                                            ) : (
                                                crmOrders.map((order) => (
                                                    <tr key={order.id}>
                                                        <td>
                                                            <div className="font-bold text-slate-800">{order.id}</div>
                                                            <div style={{ fontSize: '10px', color: C.muted }}>
                                                                {new Date(order.created_at).toLocaleString('en-IN')}
                                                            </div>
                                                        </td>
                                                        <td>
                                                            <div className="font-bold text-slate-800">{order.customer_name}</div>
                                                            <div style={{ fontSize: '10px', color: C.muted }}>{order.customer_phone}</div>
                                                            <div style={{ fontSize: '10px', color: C.muted }}>{order.customer_email}</div>
                                                        </td>
                                                        <td>
                                                            <span className="crm-badge" style={{ backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, color: C.muted }}>{order.agreement_type}</span>
                                                        </td>
                                                        <td>
                                                            <span style={{ fontSize: '11px', color: C.muted }}>
                                                                <i className={order.source === 'OFFLINE_WALKIN' ? 'fa-solid fa-store mr-1' : 'fa-solid fa-globe mr-1'}></i>
                                                                {order.source === 'OFFLINE_WALKIN' ? 'Walk-in' : 'Online'}
                                                            </span>
                                                        </td>
                                                        <td style={{ fontWeight: 800 }}>₹{order.amount}</td>
                                                        <td>
                                                            {order.cloud_url ? (
                                                                <a 
                                                                    href={order.cloud_url} 
                                                                    target="_blank" 
                                                                    rel="noopener noreferrer"
                                                                    className="crm-btn-ghost"
                                                                    style={{ padding: '5px 10px', fontSize: '11px', color: C.success, borderColor: '#C2E7D9', backgroundColor: '#E8F5E9' }}
                                                                >
                                                                    <i className="fa-solid fa-cloud mr-1"></i> View Vault
                                                                </a>
                                                            ) : (
                                                                <button
                                                                    onClick={async () => {
                                                                        try {
                                                                            const r = await fetch(`${API_BASE}/orders/${order.id}/upload`, { method: 'POST' });
                                                                            if (r.ok) { addToast("Uploaded to cloud!", 'success'); fetchCrmOrders(); }
                                                                        } catch (err) { addToast("Upload failed", 'error'); }
                                                                    }}
                                                                    className="crm-btn-ghost"
                                                                    style={{ padding: '5px 10px', fontSize: '11px' }}
                                                                >
                                                                    <i className="fa-solid fa-cloud-arrow-up mr-1"></i> Upload
                                                                </button>
                                                            )}
                                                        </td>
                                                        <td>
                                                            <select
                                                                value={order.status}
                                                                onChange={(e) => handleUpdateStatus(order.id, e.target.value)}
                                                                className="crm-select"
                                                                style={{
                                                                    padding: '4px 10px',
                                                                    fontSize: '11px',
                                                                    fontWeight: 700,
                                                                    borderRadius: '20px',
                                                                    border: 'none',
                                                                    backgroundColor: order.status === 'COMPLETED' || order.status === 'SIGNED' ? '#E8F5E9' : order.status === 'PENDING_PAYMENT' ? '#FFF3E0' : '#E3F2FD',
                                                                    color: order.status === 'COMPLETED' || order.status === 'SIGNED' ? '#2E7D32' : order.status === 'PENDING_PAYMENT' ? '#E65100' : '#1565C0'
                                                                }}
                                                            >
                                                                <option value="PENDING_PAYMENT">Pending Payment</option>
                                                                <option value="PAID">Paid / Ready</option>
                                                                <option value="DRAFTED">Drafted</option>
                                                                <option value="COMPLETED">Completed</option>
                                                                <option value="SIGNED">Signed</option>
                                                            </select>
                                                        </td>
                                                        <td style={{ textAlign: 'right' }}>
                                                            <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                                                                <button onClick={() => setCrmSelectedOrderForDetail(order)} className="crm-btn-ghost" style={{ padding: '6px' }} title="Detail view"><i className="fa-solid fa-circle-info text-blue-600"></i></button>
                                                                <button onClick={async () => {
                                                                    try {
                                                                        await fetch(`${API_BASE}/orders/${order.id}/favorite`, { method: 'PUT' });
                                                                        fetchCrmOrders();
                                                                    } catch(e) {}
                                                                }} className="crm-btn-ghost" style={{ padding: '6px' }} title="Star"><i className="fa-solid fa-star" style={{ color: order.is_favorite ? '#D97706' : '#D1D5DB' }}></i></button>
                                                                {order.form_data && (
                                                                    <button
                                                                        onClick={() => {
                                                                            const tPayload = order.form_data;
                                                                            setActiveTab(tPayload.type);
                                                                            const setters = { RENT: setRentData, ATS: setAtsData, MUTATION: setMutationData, GNIDA: setGnidaData, TM48: setTm48Data, TM_APP: setTmAppData, GNIDA_REGISTRY: setGnidaRegistryData, GNIDA_PTM: setGnidaPtmData };
                                                                            if (setters[tPayload.type]) setters[tPayload.type](tPayload.payload);
                                                                            else setRegData(tPayload.payload);
                                                                            addToast("Draft loaded into editing form fields!", 'success');
                                                                        }}
                                                                        className="crm-btn-ghost"
                                                                        style={{ padding: '6px', color: '#1E3A8A', backgroundColor: '#EFF6FF' }}
                                                                        title="Load into Editor"
                                                                    >
                                                                        <i className="fa-solid fa-file-pen"></i>
                                                                    </button>
                                                                )}
                                                                {(order.status === 'PAID' || order.status === 'DRAFTED' || order.status === 'COMPLETED') && (
                                                                    <button
                                                                        onClick={() => {
                                                                            setLeegalityOrderId(order.id);
                                                                            setLeegalitySignee({ name: order.customer_name || '', email: order.customer_email || '', phone: order.customer_phone || '' });
                                                                            setLeegalityResult(null);
                                                                            setShowLeegalityModal(true);
                                                                        }}
                                                                        className="crm-btn-ghost"
                                                                        style={{ padding: '6px', color: '#312E81', backgroundColor: '#EEF2F6' }}
                                                                        title="e-Sign"
                                                                    >
                                                                        <i className="fa-solid fa-fingerprint"></i>
                                                                    </button>
                                                                )}
                                                                <button onClick={async () => {
                                                                    if (!confirm('Are you sure you want to delete order ' + order.id + '?')) return;
                                                                    try {
                                                                        const r = await fetch(`${API_BASE}/orders/${order.id}`, { method: 'DELETE', headers: getAuthHeaders() });
                                                                        if (r.ok) { addToast('Deleted order', 'success'); fetchCrmOrders(); }
                                                                    } catch(e) { addToast('Delete failed', 'error'); }
                                                                }} className="crm-btn-ghost" style={{ padding: '6px', color: '#DC2626' }} title="Delete"><i className="fa-solid fa-trash-can"></i></button>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                ))
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderCustomersView = () => {
                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Customers</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Directory of customer transactions, total lifetime value and documents history</p>
                            </div>

                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Client Name</th>
                                                <th>Phone</th>
                                                <th>Email</th>
                                                <th style={{ textAlign: 'center' }}>Total Orders</th>
                                                <th style={{ textAlign: 'right' }}>Total LTV</th>
                                                <th>Last Transaction Date</th>
                                                <th>Staged Documents</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmCustomers.map((c, i) => (
                                                <tr key={i}>
                                                    <td style={{ fontWeight: 700 }}>{c.name}</td>
                                                    <td>{c.phone}</td>
                                                    <td>{c.email}</td>
                                                    <td style={{ textAlign: 'center' }}><span className="crm-badge" style={{ backgroundColor: '#E0F2FE', color: '#0369A1' }}>{c.order_count}</span></td>
                                                    <td style={{ textAlign: 'right', fontWeight: 800 }}>₹{parseFloat(c.total_spent).toFixed(0)}</td>
                                                    <td>{new Date(c.last_order).toLocaleString('en-IN')}</td>
                                                    <td style={{ fontSize: '10px', color: C.muted, maxW: '150px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c.orders_breakdown}</td>
                                                </tr>
                                            ))}
                                            {crmCustomers.length === 0 && (
                                                <tr><td colSpan="7" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No customers found</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderUsersView = () => {
                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>User Registrations</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Manage registered customer login accounts, security status, and review active sessions</p>
                            </div>

                            {/* Search & Sort */}
                            <div className="crm-card flex flex-col sm:flex-row gap-3" style={{ padding: '16px', display: 'flex', gap: '12px' }}>
                                <div style={{ flex: 1, position: 'relative' }}>
                                    <i className="fa-solid fa-magnifying-glass" style={{ position: 'absolute', left: '14px', top: '14px', color: C.muted, fontSize: '12px' }}></i>
                                    <input type="text" placeholder="Search user accounts by name or email..." value={crmUsersSearch} onChange={(e) => setCrmUsersSearch(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') fetchCrmUsers(); }} className="crm-input w-full" style={{ paddingLeft: '36px' }} />
                                </div>
                                <div style={{ display: 'flex', gap: '10px' }}>
                                    <select value={crmUsersSortBy} onChange={(e) => { setCrmUsersSortBy(e.target.value); setTimeout(fetchCrmUsers, 0); }} className="crm-select">
                                        <option value="created_at">Registered Date</option>
                                        <option value="name">Name</option>
                                        <option value="email">Email</option>
                                        <option value="last_login">Last Login</option>
                                        <option value="role">Role</option>
                                    </select>
                                    <button onClick={() => { setCrmUsersSortOrder(prev => prev === 'desc' ? 'asc' : 'desc'); setTimeout(fetchCrmUsers, 0); }} className="crm-btn-ghost">
                                        <i className={`fa-solid fa-arrow-${crmUsersSortOrder === 'desc' ? 'down' : 'up'}`}></i> {crmUsersSortOrder === 'desc' ? 'Newest' : 'Oldest'}
                                    </button>
                                </div>
                            </div>

                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Name</th>
                                                <th>Email</th>
                                                <th>Role</th>
                                                <th>Status</th>
                                                <th>Registered</th>
                                                <th>Last Login</th>
                                                <th style={{ textAlign: 'right' }}>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmUsers.map((u, i) => (
                                                <tr key={u.id} className="cursor-pointer" onClick={async () => {
                                                    try {
                                                        const res = await fetch(`${API_BASE}/api/admin/users/${u.id}`, { headers: getAuthHeaders() });
                                                        if (res.ok) { const d = await res.json(); setCrmSelectedUser(d); }
                                                    } catch(e) { addToast('Failed to load user details', 'error'); }
                                                }}>
                                                    <td style={{ fontWeight: 700 }}>{u.name}</td>
                                                    <td>{u.email}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: u.role === 'admin' ? '#FEF3C7' : '#EFF6FF', color: u.role === 'admin' ? '#B45309' : '#1D4ED8' }}>{u.role}</span>
                                                    </td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: u.is_active ? '#E8F5E9' : '#FEE2E2', color: u.is_active ? '#2E7D32' : '#DC2626' }}>{u.is_active ? 'Active' : 'Inactive'}</span>
                                                    </td>
                                                    <td style={{ color: C.muted }}>{u.created_at ? new Date(u.created_at).toLocaleString('en-IN') : '-'}</td>
                                                    <td style={{ color: C.muted }}>{u.last_login ? new Date(u.last_login).toLocaleString('en-IN') : '-'}</td>
                                                    <td style={{ textAlign: 'right' }} onClick={e => e.stopPropagation()}>
                                                        <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                                                            {u.role !== 'admin' && (
                                                                <button
                                                                    onClick={async () => {
                                                                        if (!confirm(u.is_active ? 'Deactivate this user?' : 'Activate this user?')) return;
                                                                        try {
                                                                            const res = await fetch(`${API_BASE}/api/admin/users/${u.id}`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ is_active: u.is_active ? 0 : 1 }) });
                                                                            if (res.ok) { addToast(u.is_active ? 'User deactivated' : 'User activated', 'success'); fetchCrmUsers(); }
                                                                        } catch (e) { addToast('Failed to update user', 'error'); }
                                                                    }}
                                                                    className="crm-btn-ghost"
                                                                    style={{ padding: '6px', color: u.is_active ? '#B91C1C' : '#047857' }}
                                                                    title={u.is_active ? 'Deactivate' : 'Activate'}
                                                                >
                                                                    <i className={`fa-solid ${u.is_active ? 'fa-ban' : 'fa-check'}`}></i>
                                                                </button>
                                                            )}
                                                            {u.role !== 'admin' && (
                                                                <button
                                                                    onClick={async () => {
                                                                        try {
                                                                            const res = await fetch(`${API_BASE}/api/admin/users/${u.id}`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ role: u.role === 'user' ? 'admin' : 'user' }) });
                                                                            if (res.ok) { addToast(`Role updated`, 'success'); fetchCrmUsers(); }
                                                                        } catch (e) { addToast('Failed to update role', 'error'); }
                                                                    }}
                                                                    className="crm-btn-ghost"
                                                                    style={{ padding: '6px' }}
                                                                    title="Toggle admin role"
                                                                >
                                                                    <i className="fa-solid fa-shield-halved"></i>
                                                                </button>
                                                            )}
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))}
                                            {crmUsers.length === 0 && (
                                                <tr><td colSpan="7" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No user accounts found</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderKanbanView = () => {
                    const columns = [
                        { key: 'PENDING_PAYMENT', label: 'Pending Payment', badge: 'bg-amber-100 text-amber-700' },
                        { key: 'PAID', label: 'Paid', badge: 'bg-blue-100 text-blue-700' },
                        { key: 'DRAFTED', label: 'Drafting', badge: 'bg-indigo-100 text-indigo-700' },
                        { key: 'UNDER_REVIEW', label: 'Under Review', badge: 'bg-purple-100 text-purple-700' },
                        { key: 'STAMPING', label: 'Stamping', badge: 'bg-cyan-100 text-cyan-700' },
                        { key: 'NOTARIZATION', label: 'Notarization', badge: 'bg-teal-100 text-teal-700' },
                        { key: 'DISPATCHED', label: 'Dispatched', badge: 'bg-emerald-100 text-emerald-700' },
                    ];

                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Order Pipeline</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Drag-and-drop workflow tracking or quick status stage progression</p>
                            </div>

                            <div style={{ display: 'flex', gap: '14px', overflowX: 'auto', paddingBottom: '16px' }}>
                                {columns.map(column => {
                                    const colOrders = crmOrders.filter(o => o.status === column.key);
                                    return (
                                        <div key={column.key} style={{ minWidth: '220px', width: '220px', flexShrink: 0, backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, borderRadius: '14px', padding: '14px' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                                                <span style={{ fontWeight: 800, fontSize: '10px', textTransform: 'uppercase', color: C.muted }}>{column.label}</span>
                                                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${column.badge}`}>{colOrders.length}</span>
                                            </div>
                                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: 'calc(100vh - 280px)', overflowY: 'auto' }}>
                                                {colOrders.map(o => (
                                                    <div key={o.id} className="crm-card" style={{ padding: '12px', fontSize: '11px', cursor: 'pointer' }} onClick={() => setCrmSelectedOrderForDetail(o)}>
                                                        <div style={{ fontWeight: 'bold', color: C.ink }}>{o.customer_name}</div>
                                                        <div style={{ color: C.muted, marginTop: '2px' }}>{o.agreement_type}</div>
                                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
                                                            <span style={{ fontWeight: 800 }}>₹{o.amount}</span>
                                                            <span style={{ fontSize: '9px', color: C.muted }}>{o.created_at?.slice(0, 10)}</span>
                                                        </div>
                                                    </div>
                                                ))}
                                                {colOrders.length === 0 && (
                                                    <div style={{ textAlign: 'center', padding: '20px 0', fontSize: '11px', color: C.muted, fontStyle: 'italic' }}>No agreements</div>
                                                )}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    );
                };

                const renderCouponsView = () => {
                    return (
                        <div className="space-y-6">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Coupons</h2>
                                    <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Manage marketing discounts, flat price deductions and coupon parameters</p>
                                </div>
                                <button onClick={async () => {
                                    try {
                                        const code = prompt('Enter coupon code:'); if (!code) return;
                                        const type = prompt('Type (percentage/flat):', 'percentage');
                                        const value = parseFloat(prompt('Value (e.g. 10 for 10% or 500 for flat ₹):') || '0');
                                        const maxUses = parseInt(prompt('Max usage limit (0 = unlimited):') || '0');
                                        const minAmount = parseFloat(prompt('Minimum order amount (0 = none):') || '0');
                                        const expires = prompt('Expiry date (YYYY-MM-DD, leave blank for none):') || '';
                                        const res = await fetch(`${API_BASE}/api/admin/coupons`, {
                                            method: 'POST',
                                            headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
                                            body: JSON.stringify({ code: code.toUpperCase(), type, value, max_uses: maxUses, min_amount: minAmount, expires_at: expires })
                                        });
                                        if (res.ok) { addToast('Coupon created successfully', 'success'); fetchCrmCoupons(); }
                                        else { const d = await res.json(); addToast(d.detail || 'Failed to create coupon', 'error'); }
                                    } catch(e) { addToast('Error creating coupon', 'error'); }
                                }} className="crm-btn-primary">
                                    <i className="fa-solid fa-plus"></i> Add Coupon
                                </button>
                            </div>

                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Coupon Code</th>
                                                <th>Discount Type</th>
                                                <th>Value</th>
                                                <th>Uses</th>
                                                <th>Min Order</th>
                                                <th>Expires</th>
                                                <th>Status</th>
                                                <th style={{ textAlign: 'right' }}>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmCoupons.map((c, i) => (
                                                <tr key={c.id}>
                                                    <td style={{ fontWeight: 800, color: C.accent }}>{c.code}</td>
                                                    <td><span className="crm-badge" style={{ backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, color: C.muted }}>{c.type}</span></td>
                                                    <td style={{ fontWeight: 800 }}>{c.type === 'percentage' ? `${c.value}%` : `₹${c.value}`}</td>
                                                    <td>{c.current_uses}{c.max_uses > 0 ? ` / ${c.max_uses}` : ' / ∞'}</td>
                                                    <td>{c.min_amount > 0 ? `₹${c.min_amount}` : '-'}</td>
                                                    <td style={{ color: C.muted }}>{c.expires_at || '-'}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: c.is_active ? '#E8F5E9' : '#FEE2E2', color: c.is_active ? '#2E7D32' : '#DC2626' }}>{c.is_active ? 'Active' : 'Inactive'}</span>
                                                    </td>
                                                    <td style={{ textAlign: 'right' }}>
                                                        <button onClick={async () => {
                                                            if (!confirm('Delete this coupon?')) return;
                                                            try {
                                                                await fetch(`${API_BASE}/api/admin/coupons/${c.id}`, { method: 'DELETE', headers: getAuthHeaders() });
                                                                fetchCrmCoupons();
                                                                addToast('Coupon deleted', 'success');
                                                            } catch(e) { addToast('Delete failed', 'error'); }
                                                        }} className="crm-btn-ghost" style={{ padding: '6px', color: '#DC2626' }}><i className="fa-solid fa-trash-can"></i></button>
                                                    </td>
                                                </tr>
                                            ))}
                                            {crmCoupons.length === 0 && (
                                                <tr><td colSpan="8" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No coupons configured</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderInvoicesView = () => {
                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Invoices & Taxation</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Billing compliance records, corporate GST reports and payment settlements</p>
                            </div>

                            {crmInvoiceGstReport && (
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Taxable Sales</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.ink, marginTop: '4px' }}>₹{crmInvoiceGstReport.summary?.total_sales?.toFixed(2)}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>GST (18% collected)</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.gold, marginTop: '4px' }}>₹{crmInvoiceGstReport.summary?.total_gst?.toFixed(2)}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Invoices Generated</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.info, marginTop: '4px' }}>{crmInvoiceGstReport.summary?.invoice_count || 0}</div>
                                    </div>
                                </div>
                            )}

                            {crmInvoiceGstReport?.daily_gst && crmInvoiceGstReport.daily_gst.length > 0 && (
                                <div className="crm-card space-y-3">
                                    <h4 style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}><i className="fa-solid fa-chart-bar" style={{ color: C.gold, marginRight: '6px' }}></i> Daily GST Collection (Last 30 days)</h4>
                                    <div style={{ overflowX: 'auto', maxHeight: '180px', overflowY: 'auto' }}>
                                        <table className="crm-table">
                                            <thead>
                                                <tr>
                                                    <th>Date</th>
                                                    <th style={{ textAlign: 'right' }}>GST Collected</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {crmInvoiceGstReport.daily_gst.map((d, i) => (
                                                    <tr key={i}>
                                                        <td style={{ color: C.muted }}>{d.date}</td>
                                                        <td style={{ textAlign: 'right', fontWeight: 700 }}>₹{d.gst.toFixed(2)}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            )}

                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Invoice #</th>
                                                <th>Customer</th>
                                                <th>Order ID</th>
                                                <th style={{ textAlign: 'right' }}>Base Amount</th>
                                                <th style={{ textAlign: 'right' }}>GST (18%)</th>
                                                <th style={{ textAlign: 'right' }}>Total Billing</th>
                                                <th>Status</th>
                                                <th>Date</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmInvoices.map((inv) => (
                                                <tr key={inv.id}>
                                                    <td style={{ fontWeight: 800 }}>{inv.invoice_number}</td>
                                                    <td style={{ fontWeight: 700 }}>{inv.customer_name || '-'}</td>
                                                    <td style={{ color: C.muted }}>{inv.order_id?.slice(0, 14)}..</td>
                                                    <td style={{ textAlign: 'right' }}>₹{inv.amount?.toFixed(2)}</td>
                                                    <td style={{ textAlign: 'right', color: C.gold }}>₹{inv.gst_amount?.toFixed(2)}</td>
                                                    <td style={{ textAlign: 'right', fontWeight: 800 }}>₹{inv.total?.toFixed(2)}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: inv.status === 'PAID' ? '#E8F5E9' : '#FFF3E0', color: inv.status === 'PAID' ? '#2E7D32' : '#E65100' }}>{inv.status}</span>
                                                    </td>
                                                    <td style={{ color: C.muted }}>{inv.created_at ? new Date(inv.created_at).toLocaleString('en-IN') : '-'}</td>
                                                </tr>
                                            ))}
                                            {crmInvoices.length === 0 && (
                                                <tr><td colSpan="8" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No compliance invoices issued yet</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderNotificationsView = () => {
                    return (
                        <div className="space-y-6">
                            <div style={{ display: 'flex', justify: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Alerts & Broadcasts</h2>
                                    <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Broadcasting system notifications or warnings to phone/email users</p>
                                </div>
                                <button onClick={async () => {
                                    try {
                                        const recipient = prompt('Recipient (email/phone number):'); if (!recipient) return;
                                        const title = prompt('Alert Title:'); if (!title) return;
                                        const msg = prompt('Detailed message:'); if (!msg) return;
                                        const type = prompt('Type (info/warning/success):', 'info');
                                        await fetch(`${API_BASE}/api/admin/notifications`, {
                                            method: 'POST',
                                            headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
                                            body: JSON.stringify({ recipient, title, message: msg, type })
                                        });
                                        fetchCrmNotifications(); addToast('Notification broadcast sent', 'success');
                                    } catch(e) { addToast('Broadcast failed', 'error'); }
                                }} className="crm-btn-primary">
                                    <i className="fa-solid fa-paper-plane"></i> Broadcast Alert
                                </button>
                            </div>

                            <div className="crm-card space-y-4">
                                <div style={{ fontWeight: 800, fontSize: '14px', color: C.ink, borderBottom: `1px solid ${C.line}`, paddingBottom: '12px' }}>Expiring Rentals Alerts</div>
                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                                    <div>
                                        <div style={{ fontSize: '11px', color: '#B91C1C', fontWeight: 800, textTransform: 'uppercase', marginBottom: '8px' }}><i className="fa-solid fa-circle-exclamation"></i> Expired ({expiringRentals?.expired?.length || 0})</div>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '200px', overflowY: 'auto' }}>
                                            {expiringRentals?.expired?.map(r => (
                                                <div key={r.order_id} style={{ padding: '10px', border: '1px solid #FEE2E2', backgroundColor: '#FEF2F2', borderRadius: '8px', fontSize: '11px' }}>
                                                    <div style={{ fontWeight: 'bold' }}>{r.name}</div>
                                                    <div style={{ color: C.muted }}>Phone: {r.phone} • Expired: {r.expiry_date}</div>
                                                </div>
                                            ))}
                                            {(!expiringRentals || expiringRentals.expired.length === 0) && (
                                                <div style={{ fontStyle: 'italic', color: C.muted, fontSize: '11px' }}>No expired agreements</div>
                                            )}
                                        </div>
                                    </div>
                                    <div>
                                        <div style={{ fontSize: '11px', color: '#D97706', fontWeight: 800, textTransform: 'uppercase', marginBottom: '8px' }}><i className="fa-solid fa-triangle-exclamation"></i> Expiring Soon ({expiringRentals?.expiring?.length || 0})</div>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '200px', overflowY: 'auto' }}>
                                            {expiringRentals?.expiring?.map(r => (
                                                <div key={r.order_id} style={{ padding: '10px', border: '1px solid #FEF3C7', backgroundColor: '#FFFBEB', borderRadius: '8px', fontSize: '11px' }}>
                                                    <div style={{ fontWeight: 'bold' }}>{r.name}</div>
                                                    <div style={{ color: C.muted }}>Phone: {r.phone} • Expiry: {r.expiry_date} ({r.days_left} days left)</div>
                                                </div>
                                            ))}
                                            {(!expiringRentals || expiringRentals.expiring.length === 0) && (
                                                <div style={{ fontStyle: 'italic', color: C.muted, fontSize: '11px' }}>No expiring agreements</div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="crm-card" style={{ padding: 0 }}>
                                <div style={{ padding: '16px 20px', borderBottom: `1px solid ${C.line}`, fontWeight: 800, fontSize: '14px', color: C.ink }}>System Broadcast Log ({crmNotifications.length})</div>
                                <div style={{ display: 'flex', flexDirection: 'column', divideY: true, maxHeight: '350px', overflowY: 'auto' }}>
                                    {crmNotifications.map((n) => (
                                        <div key={n.id} style={{ padding: '14px 20px', borderBottom: `1px solid ${C.line}`, display: 'flex', gap: '12px' }}>
                                            <div style={{ width: '32px', height: '32px', borderRadius: '8px', backgroundColor: n.type === 'warning' ? '#FEF3C7' : n.type === 'success' ? '#E8F5E9' : '#EFF6FF', color: n.type === 'warning' ? '#B45309' : n.type === 'success' ? '#2E7D32' : '#1D4ED8', display: 'grid', placeItems: 'center', flexShrink: 0 }}>
                                                <i className={`fa-solid ${n.type === 'warning' ? 'fa-triangle-exclamation' : n.type === 'success' ? 'fa-circle-check' : 'fa-info'}`}></i>
                                            </div>
                                            <div style={{ flex: 1, minWidth: 0 }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                    <span style={{ fontWeight: 'bold', fontSize: '12px', color: C.ink }}>{n.title}</span>
                                                    <span style={{ fontSize: '10px', color: C.muted }}>{n.created_at ? new Date(n.created_at).toLocaleString('en-IN') : ''}</span>
                                                </div>
                                                <p style={{ fontSize: '11px', color: C.muted, marginTop: '2px' }}>{n.message}</p>
                                                <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginTop: '6px', fontSize: '10px', color: C.muted }}>
                                                    <span>Recipient: {n.recipient}</span>
                                                    <span className="crm-badge" style={{ backgroundColor: n.status === 'sent' ? '#E8F5E9' : '#F3F4F6', color: n.status === 'sent' ? '#2E7D32' : C.muted }}>{n.status}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                    {crmNotifications.length === 0 && (
                                        <div style={{ padding: '30px', textAlign: 'center', color: C.muted, fontSize: '12px' }}>No broadcast records found</div>
                                    )}
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderActivityView = () => {
                    return (
                        <div className="space-y-6">
                            <div>
                                <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Telemetry Logs</h2>
                                <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Audit trails of user form progress steps, template selections, and payments</p>
                            </div>

                            {trackedEventStats && (
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Total Form Hits</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.ink, marginTop: '4px' }}>{trackedEventStats.total_events}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Active Sessions</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.info, marginTop: '4px' }}>{trackedEventStats.unique_sessions}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Top Event Action</span>
                                        <div style={{ fontSize: '16px', fontWeight: 800, color: C.ink, marginTop: '8px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {trackedEventStats.event_breakdown && Object.entries(trackedEventStats.event_breakdown).sort((a,b) => b[1]-a[1])[0]?.[0] || '-'}
                                        </div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Most Popular Page</span>
                                        <div style={{ fontSize: '16px', fontWeight: 800, color: C.ink, marginTop: '8px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                            {trackedEventStats.page_views && Object.entries(trackedEventStats.page_views).sort((a,b) => b[1]-a[1])[0]?.[0] || '-'}
                                        </div>
                                    </div>
                                </div>
                            )}

                            <div className="crm-table-container">
                                <div style={{ padding: '16px 20px', borderBottom: `1px solid ${C.line}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <span style={{ fontWeight: 800, color: C.ink, fontSize: '14px' }}>User Events Log ({trackedEvents.length})</span>
                                    <button onClick={loadTrackedEvents} className="crm-btn-ghost" style={{ padding: '6px 12px', fontSize: '11px' }}><i className="fa-solid fa-rotate mr-1"></i> Refresh</button>
                                </div>
                                <div style={{ overflowX: 'auto', maxHeight: '400px', overflowY: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr style={{ position: 'sticky', top: 0, zIndex: 10 }}>
                                                <th>Timestamp</th>
                                                <th>Action Event</th>
                                                <th>Format / Page</th>
                                                <th>Context Details</th>
                                                <th>Session ID</th>
                                                <th>User ID</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {trackedEvents.map((ev, i) => (
                                                <tr key={ev.id || i}>
                                                    <td style={{ color: C.muted, fontSize: '11px', whiteSpace: 'nowrap' }}>{new Date(ev.timestamp).toLocaleString('en-IN')}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{
                                                            backgroundColor: ev.event === 'page_view' ? '#F3F4F6' : ev.event === 'payment_complete' || ev.event === 'payment_initiated' ? '#E8F5E9' : '#EFF6FF',
                                                            color: ev.event === 'page_view' ? C.muted : ev.event === 'payment_complete' || ev.event === 'payment_initiated' ? '#2E7D32' : '#1D4ED8'
                                                        }}>
                                                            <i className={`fa-solid ${
                                                                ev.event === 'page_view' ? 'fa-eye' :
                                                                ev.event === 'payment_complete' ? 'fa-check-circle' :
                                                                ev.event === 'pdf_download' ? 'fa-file-pdf' : 'fa-circle-dot'
                                                            } mr-1`}></i>
                                                            {ev.event}
                                                        </span>
                                                    </td>
                                                    <td style={{ fontWeight: 700 }}>{ev.page}</td>
                                                    <td style={{ color: C.muted, maxW: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{ev.detail}</td>
                                                    <td style={{ color: C.muted, fontSize: '11px' }}>{ev.session_id?.slice(0, 16)}..</td>
                                                    <td style={{ color: C.muted }}>{ev.user_id || '-'}</td>
                                                </tr>
                                            ))}
                                            {trackedEvents.length === 0 && (
                                                <tr><td colSpan="6" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No user actions logged yet</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                const renderAnalyticsView = () => {
                    return (
                        <div className="space-y-6">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Conversion Funnels</h2>
                                    <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Analyse document checkout pipelines, form progress dropout ratios and geography</p>
                                </div>
                                <button onClick={fetchCrmAnalyticsExtras} className="crm-btn-ghost">
                                    <i className="fa-solid fa-arrows-rotate mr-1"></i> Refresh Data
                                </button>
                            </div>

                            {/* Conversion Funnel */}
                            {crmFunnelData && (
                                <div className="crm-card space-y-4">
                                    <h4 style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}><i className="fa-solid fa-filter" style={{ color: C.accent, marginRight: '6px' }}></i> Conversion Funnel</h4>
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                        {[
                                            { key: 'total_started', label: 'Started Form', color: '#D1D5DB' },
                                            { key: 'pending_payment', label: 'Payment Pending', color: '#FCD34D' },
                                            { key: 'paid', label: 'Paid Orders', color: '#60A5FA' },
                                            { key: 'drafted', label: 'Drafted/Saved', color: '#818CF8' },
                                            { key: 'completed', label: 'Done Drafting', color: '#34D399' },
                                            { key: 'signed', label: 'Digitally Signed', color: '#059669' },
                                        ].map(stage => {
                                            const count = crmFunnelData[stage.key] || 0;
                                            const maxCount = crmFunnelData.total_started || 1;
                                            const pct = Math.round((count / maxCount) * 100);
                                            return (
                                                <div key={stage.key} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                                    <span style={{ width: '120px', fontSize: '11px', fontWeight: 700, color: C.muted, textAlign: 'right' }}>{stage.label}</span>
                                                    <div style={{ flex: 1, height: '24px', backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, borderRadius: '6px', overflow: 'hidden' }}>
                                                        <div style={{ height: '100%', backgroundColor: stage.color, width: `${pct}%`, transition: 'width 0.5s ease-out' }}></div>
                                                    </div>
                                                    <span style={{ width: '80px', fontSize: '12px', fontWeight: 800, color: C.ink }}>{count} ({pct}%)</span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            )}

                            {crmAbandonedData && (
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Abandoned Saved Drafts</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.gold, marginTop: '4px' }}>{crmAbandonedData.total_drafts}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Unpaid Checkout Dropouts</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: '#DC2626', marginTop: '4px' }}>{crmAbandonedData.unpaid_orders}</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Dropout Percentage</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.accent, marginTop: '4px' }}>{crmAbandonedData.abandoned_rate}%</div>
                                    </div>
                                    <div className="crm-card">
                                        <span style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Unsaved Today's hits</span>
                                        <div style={{ fontSize: '24px', fontWeight: 800, color: C.ink, marginTop: '4px' }}>{crmAbandonedData.today_drafts}</div>
                                    </div>
                                </div>
                            )}

                            {/* Dropoff step analytics */}
                            {crmDropoffData && (
                                <div className="crm-card space-y-4">
                                    <h4 style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}><i className="fa-solid fa-person-walking-arrow-right" style={{ color: '#E11D48', marginRight: '6px' }}></i> Form Section Dropout Steps</h4>
                                    <div style={{ overflowX: 'auto' }}>
                                        <table className="crm-table">
                                            <thead>
                                                <tr>
                                                    <th>Form Step / Accordion Section</th>
                                                    <th style={{ textAlign: 'center' }}>Users Reached</th>
                                                    <th style={{ textAlign: 'center' }}>Users Bounced</th>
                                                    <th style={{ textAlign: 'center' }}>Bounce Rate %</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {crmDropoffData.dropoff.map((d, i) => (
                                                    <tr key={i}>
                                                        <td style={{ fontWeight: 700 }}>{d.step.replace('_', ' ')}</td>
                                                        <td style={{ textAlign: 'center', fontWeight: 'bold' }}>{d.count}</td>
                                                        <td style={{ textAlign: 'center', color: '#DC2626' }}>{d.lost}</td>
                                                        <td style={{ textAlign: 'center' }}>
                                                            <span className="crm-badge" style={{
                                                                backgroundColor: d.loss_percentage > 30 ? '#FEE2E2' : d.loss_percentage > 10 ? '#FFFBEB' : '#E8F5E9',
                                                                color: d.loss_percentage > 30 ? '#DC2626' : d.loss_percentage > 10 ? '#D97706' : '#2E7D32'
                                                            }}>{d.loss_percentage}%</span>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            )}

                            {crmHeatmapData && crmHeatmapData.locations && crmHeatmapData.locations.length > 0 && (
                                <div className="crm-card space-y-3">
                                    <h4 style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}><i className="fa-solid fa-map-location-dot" style={{ color: C.success, marginRight: '6px' }}></i> Geographic Distribution</h4>
                                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
                                        {crmHeatmapData.locations.map((loc, i) => (
                                            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, padding: '10px 14px', borderRadius: '8px' }}>
                                                <span style={{ fontWeight: 700, fontSize: '12px' }}><i className="fa-solid fa-location-dot" style={{ color: C.muted, marginRight: '6px' }}></i> {loc.location}</span>
                                                <span className="crm-badge" style={{ backgroundColor: C.accentSoft, color: C.accent }}>{loc.count}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Audit trail loading */}
                            <div className="space-y-4">
                                <div style={{ display: 'flex', justify: 'space-between', alignItems: 'center' }}>
                                    <h4 style={{ fontWeight: 800, fontSize: '13px', color: C.ink }}><i className="fa-solid fa-clipboard-list" style={{ color: C.muted, marginRight: '6px' }}></i> API Audit Trail</h4>
                                    <button onClick={fetchCrmAudit} className="crm-btn-ghost" style={{ padding: '6px 12px', fontSize: '11px' }}>Load Audit logs</button>
                                </div>
                                {crmAuditData && (
                                    <div className="crm-table-container" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                                        <table className="crm-table">
                                            <thead>
                                                <tr>
                                                    <th>Timestamp</th>
                                                    <th>Method</th>
                                                    <th>API Path</th>
                                                    <th style={{ textAlign: 'center' }}>Status</th>
                                                    <th>Operator</th>
                                                    <th style={{ textAlign: 'right' }}>Time Taken</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {crmAuditData.entries?.slice(0, 50).map((e, i) => (
                                                    <tr key={e.id || i}>
                                                        <td style={{ color: C.muted, fontSize: '11px' }}>{new Date(e.timestamp).toLocaleString('en-IN')}</td>
                                                        <td>
                                                            <span className="crm-badge" style={{
                                                                backgroundColor: e.method === 'POST' ? '#E8F5E9' : e.method === 'GET' ? '#E3F2FD' : '#FFF3E0',
                                                                color: e.method === 'POST' ? '#2E7D32' : e.method === 'GET' ? '#1565C0' : '#E65100'
                                                            }}>{e.method}</span>
                                                        </td>
                                                        <td style={{ fontWeight: 600, maxW: '220px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{e.path}</td>
                                                        <td style={{ textAlign: 'center' }}>
                                                            <span style={{ fontWeight: 700, color: e.status_code < 300 ? '#2E7D32' : '#DC2626' }}>{e.status_code}</span>
                                                        </td>
                                                        <td style={{ color: C.muted }}>{e.user_name || e.user_id?.slice(0,8) || '-'}</td>
                                                        <td style={{ textAlign: 'right', color: C.muted }}>{e.duration_ms}ms</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                };

                const renderStaffView = () => {
                    return (
                        <div className="space-y-6">
                            <div style={{ display: 'flex', justify: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <h2 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: C.ink }}>Staff & Assignments</h2>
                                    <p style={{ margin: '4px 0 0', fontSize: 13, color: C.muted }}>Manage attorney credentials, staff roles and direct docket assignments</p>
                                </div>
                                <button onClick={() => {
                                    const n = prompt('Enter staff member name:'); if (!n) return;
                                    const e = prompt('Enter login email:'); if (!e) return;
                                    const r = prompt('Enter role (attorney/support/finance):', 'support'); if (!r) return;
                                    fetch(`${API_BASE}/api/admin/staff`, {
                                        method: 'POST',
                                        headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
                                        body: JSON.stringify({ name: n, email: e, role: r, password: 'staff123' })
                                    }).then(res => {
                                        if (res.ok) { addToast('Staff created successfully (Password: staff123)', 'success'); fetchCrmStaff(); }
                                        else { res.json().then(d => addToast(d.detail || 'Error adding staff', 'error')); }
                                    }).catch(() => addToast('Failed to add staff', 'error'));
                                }} className="crm-btn-primary">
                                    <i className="fa-solid fa-plus"></i> Add Staff Member
                                </button>
                            </div>

                            <div className="crm-table-container">
                                <div style={{ overflowX: 'auto' }}>
                                    <table className="crm-table">
                                        <thead>
                                            <tr>
                                                <th>Name</th>
                                                <th>Email</th>
                                                <th>Role</th>
                                                <th>Status</th>
                                                <th>Joined</th>
                                                <th>Last Active</th>
                                                <th style={{ textAlign: 'right' }}>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {crmStaff.map((s) => (
                                                <tr key={s.id}>
                                                    <td style={{ fontWeight: 700 }}>{s.name}</td>
                                                    <td>{s.email}</td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: '#FAF6EE', border: `1px solid ${C.line}`, color: C.muted }}>{s.role}</span>
                                                    </td>
                                                    <td>
                                                        <span className="crm-badge" style={{ backgroundColor: s.is_active ? '#E8F5E9' : '#FEE2E2', color: s.is_active ? '#2E7D32' : '#DC2626' }}>{s.is_active ? 'Active' : 'Inactive'}</span>
                                                    </td>
                                                    <td style={{ color: C.muted }}>{s.created_at ? new Date(s.created_at).toLocaleString('en-IN') : '-'}</td>
                                                    <td style={{ color: C.muted }}>{s.last_login ? new Date(s.last_login).toLocaleString('en-IN') : '-'}</td>
                                                    <td style={{ textAlign: 'right' }}>
                                                        <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                                                            <button onClick={async () => {
                                                                const newRole = prompt('Update role (attorney/support/finance/admin):', s.role);
                                                                if (newRole) {
                                                                    await fetch(`${API_BASE}/api/admin/staff/${s.id}`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ role: newRole }) });
                                                                    fetchCrmStaff();
                                                                    addToast('Role updated', 'success');
                                                                }
                                                            }} className="crm-btn-ghost" style={{ padding: '6px' }} title="Change Role"><i className="fa-solid fa-shield"></i></button>
                                                            <button onClick={async () => {
                                                                const nowActive = s.is_active ? 0 : 1;
                                                                await fetch(`${API_BASE}/api/admin/staff/${s.id}`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ is_active: nowActive }) });
                                                                fetchCrmStaff();
                                                                addToast(nowActive ? 'Staff activated' : 'Staff deactivated', 'success');
                                                            }} className="crm-btn-ghost" style={{ padding: '6px', color: s.is_active ? '#DC2626' : '#047857' }} title={s.is_active ? 'Deactivate' : 'Activate'}><i className={`fa-solid ${s.is_active ? 'fa-ban' : 'fa-check'}`}></i></button>
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))}
                                            {crmStaff.length === 0 && (
                                                <tr><td colSpan="7" style={{ padding: '30px', textAlign: 'center', color: C.muted }}>No staff registered</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    );
                };

                return (
                    <div className="crm-admin-container">
                        <style>{`
                            .crm-admin-container {
                                display: flex;
                                min-height: 100vh;
                                width: 100%;
                                background-color: ${C.paper};
                                color: ${C.ink};
                                font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
                            }
                            .crm-sidebar {
                                width: 250px;
                                border-right: 1px solid ${C.line};
                                background-color: ${C.panel};
                                padding: 24px 16px;
                                position: sticky;
                                top: 0;
                                height: 100vh;
                                display: flex;
                                flex-direction: column;
                                justify-content: space-between;
                                flex-shrink: 0;
                                z-index: 50;
                            }
                            .crm-navbtn {
                                display: flex;
                                align-items: center;
                                gap: 12px;
                                width: 100%;
                                padding: 10px 14px;
                                margin-bottom: 6px;
                                border: none;
                                border-radius: 10px;
                                background: transparent;
                                color: ${C.ink};
                                font-weight: 500;
                                font-size: 13px;
                                text-align: left;
                                transition: all 0.2s ease;
                                cursor: pointer;
                            }
                            .crm-navbtn:hover {
                                background-color: ${C.accentSoft};
                                color: ${C.accent};
                            }
                            .crm-navbtn.active {
                                background-color: ${C.accentSoft};
                                color: ${C.accent};
                                font-weight: 700;
                            }
                            .crm-card {
                                background: ${C.panel};
                                border: 1px solid ${C.line};
                                border-radius: 14px;
                                padding: 20px;
                                box-shadow: 0 4px 12px rgba(30, 27, 22, 0.02);
                                transition: all 0.2s ease;
                            }
                            .crm-card:hover {
                                box-shadow: 0 6px 18px rgba(30, 27, 22, 0.04);
                            }
                            .crm-table-container {
                                background: ${C.panel};
                                border: 1px solid ${C.line};
                                border-radius: 14px;
                                overflow: hidden;
                                box-shadow: 0 4px 12px rgba(30, 27, 22, 0.02);
                            }
                            .crm-table {
                                width: 100%;
                                border-collapse: collapse;
                                font-size: 13px;
                            }
                            .crm-table th {
                                background-color: #FAF6EE;
                                border-bottom: 1px solid ${C.line};
                                padding: 12px 16px;
                                font-weight: 700;
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                color: ${C.muted};
                            }
                            .crm-table td {
                                padding: 14px 16px;
                                border-bottom: 1px solid ${C.line};
                                color: ${C.ink};
                                vertical-align: middle;
                            }
                            .crm-table tr:last-child td {
                                border-bottom: none;
                            }
                            .crm-table tr:hover td {
                                background-color: ${C.paper};
                            }
                            .crm-btn-primary {
                                display: inline-flex;
                                align-items: center;
                                gap: 8px;
                                padding: 10px 18px;
                                background-color: ${C.accent};
                                color: #ffffff;
                                border: none;
                                border-radius: 10px;
                                font-size: 13px;
                                font-weight: 700;
                                transition: all 0.2s ease;
                                cursor: pointer;
                                box-shadow: 0 4px 12px rgba(154, 59, 46, 0.2);
                            }
                            .crm-btn-primary:hover {
                                background-color: #7D2E24;
                                box-shadow: 0 6px 16px rgba(154, 59, 46, 0.3);
                            }
                            .crm-btn-ghost {
                                display: inline-flex;
                                align-items: center;
                                gap: 6px;
                                padding: 8px 14px;
                                background-color: ${C.panel};
                                color: ${C.ink};
                                border: 1px solid ${C.line};
                                border-radius: 10px;
                                font-size: 12px;
                                font-weight: 700;
                                transition: all 0.2s ease;
                                cursor: pointer;
                            }
                            .crm-btn-ghost:hover {
                                background-color: ${C.paper};
                                border-color: ${C.muted};
                            }
                            .crm-badge {
                                display: inline-flex;
                                align-items: center;
                                gap: 6px;
                                padding: 4px 10px;
                                border-radius: 20px;
                                font-size: 11px;
                                font-weight: 700;
                            }
                            .crm-input, .crm-select {
                                padding: 10px 14px;
                                border: 1px solid ${C.line};
                                border-radius: 10px;
                                font-size: 13px;
                                background-color: ${C.panel};
                                color: ${C.ink};
                                outline: none;
                                transition: all 0.2s ease;
                            }
                            .crm-input:focus, .crm-select:focus {
                                border-color: ${C.accent};
                                box-shadow: 0 0 0 3px ${C.accentSoft};
                            }
                        `}</style>

                        {/* SIDEBAR */}
                        <aside className="crm-sidebar">
                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '0 8px 24px', borderBottom: `1px solid ${C.line}` }}>
                                    <div style={{ width: '34px', height: '34px', borderRadius: '8px', background: C.accent, display: 'grid', placeItems: 'center', color: '#fff' }}>
                                        <i className="fa-solid fa-file-signature text-base"></i>
                                    </div>
                                    <div>
                                        <div style={{ fontWeight: 800, fontSize: '15px', letterSpacing: '-0.2px', color: C.ink }}>DeedDesk</div>
                                        <div style={{ fontSize: '10px', color: C.muted, fontWeight: 700, textTransform: 'uppercase' }}>Admin Console</div>
                                    </div>
                                </div>

                                <div style={{ marginTop: '20px' }}>
                                    {navItems.map(item => {
                                        const active = crmView === item.key;
                                        return (
                                            <button
                                                key={item.key}
                                                className={`crm-navbtn ${active ? 'active' : ''}`}
                                                onClick={item.action}
                                            >
                                                <i className={`fa-solid ${item.icon}`} style={{ width: '18px', textAlign: 'center' }}></i>
                                                <span>{item.label}</span>
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>

                            <div style={{ borderTop: `1px solid ${C.line}`, paddingTop: '16px' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px', padding: '0 8px' }}>
                                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: C.accentSoft, color: C.accent, display: 'grid', placeItems: 'center', fontWeight: 'bold', fontSize: '13px' }}>
                                        AD
                                    </div>
                                    <div style={{ minWidth: 0, flex: 1 }}>
                                        <div style={{ fontWeight: 'bold', fontSize: '12px', color: C.ink, textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>Admin Console</div>
                                        <div style={{ fontSize: '10px', color: C.muted }}>Super User</div>
                                    </div>
                                </div>
                                <button
                                    onClick={() => {
                                        localStorage.removeItem('instadeed_admin');
                                        localStorage.removeItem('instadeed_token');
                                        setIsAdminLoggedIn(false);
                                        setActiveTab('HOME');
                                    }}
                                    className="crm-btn-ghost w-full"
                                    style={{ justifyContent: 'center', color: '#B91C1C', borderColor: '#FEE2E2', backgroundColor: '#FEF2F2' }}
                                >
                                    <i className="fa-solid fa-right-from-bracket"></i>
                                    <span>Sign Out</span>
                                </button>
                            </div>
                        </aside>

                        {/* MAIN SECTION */}
                        <main style={{ flex: 1, padding: '32px 40px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '28px' }}>
                            {crmView === 'dashboard' && renderDashboardView()}
                            {crmView === 'orders' && renderOrdersView()}
                            {crmView === 'customers' && renderCustomersView()}
                            {crmView === 'users' && renderUsersView()}
                            {crmView === 'kanban' && renderKanbanView()}
                            {crmView === 'coupons' && renderCouponsView()}
                            {crmView === 'invoices' && renderInvoicesView()}
                            {crmView === 'notifications' && renderNotificationsView()}
                            {crmView === 'activity' && renderActivityView()}
                            {crmView === 'analytics' && renderAnalyticsView()}
                            {crmView === 'staff' && renderStaffView()}
                        </main>

                        {/* Order Detail Modal */}
                        {crmSelectedOrderForDetail && (
                            <div className="fixed inset-0 bg-black/60 z-[9999] flex items-center justify-center p-4 backdrop-blur-sm" onClick={() => setCrmSelectedOrderForDetail(null)}>
                                <div className="bg-white w-full max-w-3xl rounded-2xl border border-slate-100 shadow-lg max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
                                    <div className="p-6">
                                        <div className="flex items-center justify-between mb-6">
                                            <h3 className="font-extrabold text-slate-800 text-lg flex items-center gap-2">
                                                <i className="fa-solid fa-file-circle-info text-blue-600"></i>
                                                Order Detail
                                            </h3>
                                            <button onClick={() => setCrmSelectedOrderForDetail(null)} className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-red-50 text-slate-400 hover:text-red-500 transition text-sm cursor-pointer border-0">
                                                <i className="fa-solid fa-xmark"></i>
                                            </button>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Order ID</span><span className="font-bold text-slate-800">{crmSelectedOrderForDetail.id}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Customer</span><span className="font-bold text-slate-800">{crmSelectedOrderForDetail.customer_name}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Phone</span><span className="text-slate-600">{crmSelectedOrderForDetail.customer_phone}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Email</span><span className="text-slate-600">{crmSelectedOrderForDetail.customer_email}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Agreement</span><span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full font-bold text-[10px]">{crmSelectedOrderForDetail.agreement_type}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Amount</span><span className="font-black text-slate-800">₹{crmSelectedOrderForDetail.amount}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Source</span><span className="text-slate-600">{crmSelectedOrderForDetail.source}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Status</span>
                                                <select value={crmSelectedOrderForDetail.status} onChange={async (e) => { try { const newStatus = e.target.value; await fetch(`${API_BASE}/api/orders/${crmSelectedOrderForDetail.id}/status`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ status: newStatus }) }); setCrmSelectedOrderForDetail({...crmSelectedOrderForDetail, status: newStatus}); fetchCrmOrders(); addToast('Status updated', 'success'); } catch(e) { addToast('Failed to update status', 'error'); } }} className="px-2 py-1 border border-slate-200 rounded-lg text-xs font-bold text-slate-700 focus:outline-none cursor-pointer bg-white">
                                                    {['PENDING_PAYMENT','PAID','DRAFTED','UNDER_REVIEW','STAMPING','NOTARIZATION','DISPATCHED','COMPLETED','SIGNED','REFUNDED'].map(s => (
                                                        <option key={s} value={s}>{s.replace('_',' ')}</option>
                                                    ))}
                                                </select>
                                            </div>
                                            <div className="col-span-2"><span className="text-[10px] uppercase font-bold text-slate-400 block">Created</span><span className="text-slate-500">{crmSelectedOrderForDetail.created_at}</span></div>
                                        </div>

                                        {/* Assign Staff */}
                                        <div className="border-t border-slate-100 pt-4 mb-4">
                                            <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-user-plus text-indigo-500"></i> Assign Staff</h4>
                                            <div className="flex gap-2">
                                                <select id={`staff-select-${crmSelectedOrderForDetail.id}`} className="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-xs focus:outline-none bg-white">
                                                    <option value="">Select staff...</option>
                                                    {crmStaff.map(s => <option key={s.id} value={s.id}>{s.name} ({s.role})</option>)}
                                                </select>
                                                <select id={`staff-role-${crmSelectedOrderForDetail.id}`} className="px-3 py-2 border border-slate-200 rounded-lg text-xs focus:outline-none bg-white">
                                                    <option value="attorney">Attorney</option>
                                                    <option value="support">Support</option>
                                                    <option value="finance">Finance</option>
                                                </select>
                                                <button onClick={async () => {
                                                    try {
                                                        const sidEl = document.getElementById(`staff-select-${crmSelectedOrderForDetail.id}`);
                                                        const roleEl = document.getElementById(`staff-role-${crmSelectedOrderForDetail.id}`);
                                                        if (!sidEl || !roleEl) return;
                                                        const sid = sidEl.value;
                                                        const role = roleEl.value;
                                                        if (!sid) return;
                                                        await fetch(`${API_BASE}/api/admin/orders/${crmSelectedOrderForDetail.id}/assign`, { method: 'PUT', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ staff_id: sid, role }) });
                                                        addToast('Staff assigned', 'success');
                                                    } catch(e) { addToast('Failed to assign staff', 'error'); }
                                                }} className="px-3 py-2 bg-blue-600 text-white rounded-lg text-xs font-bold hover:bg-blue-700 cursor-pointer border-0"><i className="fa-solid fa-check mr-1"></i> Assign</button>
                                            </div>
                                        </div>

                                        {/* Notes */}
                                        <div className="border-t border-slate-100 pt-4 mb-4">
                                            <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-note-sticky text-amber-500"></i> Internal Notes</h4>
                                            <div id={`notes-container-${crmSelectedOrderForDetail.id}`} className="text-xs text-slate-500 mb-2">Loading notes...</div>
                                            <div className="flex gap-2">
                                                <input id={`note-input-${crmSelectedOrderForDetail.id}`} type="text" placeholder="Add a note..." className="crm-input flex-1" />
                                                <button onClick={async () => {
                                                    try {
                                                        const noteInput = document.getElementById(`note-input-${crmSelectedOrderForDetail.id}`);
                                                        if (!noteInput) return;
                                                        const note = noteInput.value;
                                                        if (!note) return;
                                                        await fetch(`${API_BASE}/api/admin/orders/${crmSelectedOrderForDetail.id}/notes`, { method: 'POST', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ note }) });
                                                        noteInput.value = '';
                                                        const res = await fetch(`${API_BASE}/api/admin/orders/${crmSelectedOrderForDetail.id}/notes`, { headers: getAuthHeaders() });
                                                        if (res.ok) { const d = await res.json(); const container = document.getElementById(`notes-container-${crmSelectedOrderForDetail.id}`); if (container) { container.innerText = ''; d.notes.forEach(n => { const div = document.createElement('div'); div.className = 'py-1.5 border-b border-slate-50 last:border-0'; const span = document.createElement('span'); span.className = 'font-bold text-slate-700'; span.textContent = (n.author_name || 'Unknown') + ': '; div.appendChild(span); div.appendChild(document.createTextNode(n.note + ' ')); const time = document.createElement('span'); time.className = 'text-[8px] text-slate-400'; time.textContent = new Date(n.created_at).toLocaleString('en-IN'); div.appendChild(time); container.appendChild(div); }); } }
                                                        addToast('Note added', 'success');
                                                    } catch(e) { addToast('Failed to add note', 'error'); }
                                                }} className="px-3 py-2 bg-amber-600 text-white rounded-lg text-xs font-bold hover:bg-amber-700 cursor-pointer border-0"><i className="fa-solid fa-plus"></i></button>
                                            </div>
                                        </div>

                                        {/* Refund */}
                                        <div className="border-t border-slate-100 pt-4">
                                            <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-rotate-left text-rose-500"></i> Refund / Cancel</h4>
                                            <div className="flex gap-2">
                                                <input id={`refund-amount-${crmSelectedOrderForDetail.id}`} type="number" placeholder="Amount" defaultValue={crmSelectedOrderForDetail.amount} className="crm-input w-32" />
                                                <input id={`refund-reason-${crmSelectedOrderForDetail.id}`} type="text" placeholder="Reason" className="crm-input flex-1" />
                                                <button onClick={async () => {
                                                    try {
                                                        if (!confirm('Process refund?')) return;
                                                        const amountEl = document.getElementById(`refund-amount-${crmSelectedOrderForDetail.id}`);
                                                        const reasonEl = document.getElementById(`refund-reason-${crmSelectedOrderForDetail.id}`);
                                                        if (!amountEl || !reasonEl) return;
                                                        const amount = amountEl.value;
                                                        const reason = reasonEl.value;
                                                        const res = await fetch(`${API_BASE}/api/admin/orders/${crmSelectedOrderForDetail.id}/refund`, { method: 'POST', headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' }, body: JSON.stringify({ amount: parseFloat(amount), reason }) });
                                                        if (res.ok) { addToast('Refund processed', 'success'); fetchCrmOrders(); setCrmSelectedOrderForDetail(null); } else { addToast('Failed', 'error'); }
                                                    } catch(e) { addToast('Failed to process refund', 'error'); }
                                                }} className="px-3 py-2 bg-rose-600 text-white rounded-lg text-xs font-bold hover:bg-rose-700 cursor-pointer border-0">Process Refund</button>
                                            </div>
                                        </div>

                                        {/* Version History */}
                                        <div className="border-t border-slate-100 pt-4 mt-4">
                                            <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-clock-rotate-left text-purple-500"></i> Document Versions</h4>
                                            <button onClick={async () => {
                                                try {
                                                    const res = await fetch(`${API_BASE}/api/admin/orders/${crmSelectedOrderForDetail.id}/versions`, { headers: getAuthHeaders() });
                                                    if (res.ok) { const d = await res.json(); const versionsContainer = document.getElementById(`versions-${crmSelectedOrderForDetail.id}`); if (versionsContainer) { versionsContainer.innerText = ''; d.versions.forEach(v => { const div = document.createElement('div'); div.className = 'py-1.5 border-b border-slate-50 text-xs'; const vspan = document.createElement('span'); vspan.className = 'font-bold text-purple-700'; vspan.textContent = 'v' + v.version + ' by ' + (v.author_name || 'Unknown') + ' · ' + (v.change_summary || 'No summary') + ' · '; div.appendChild(vspan); div.appendChild(document.createTextNode(new Date(v.created_at).toLocaleString('en-IN'))); versionsContainer.appendChild(div); }); } }
                                                } catch(e) { addToast('Failed to load versions', 'error'); }
                                            }} className="px-3 py-1.5 bg-purple-50 text-purple-700 rounded-lg text-[10px] font-bold hover:bg-purple-100 cursor-pointer mb-2 border-0">Load Versions</button>
                                            <div id={`versions-${crmSelectedOrderForDetail.id}`} className="text-xs text-slate-500 max-h-[150px] overflow-y-auto"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* User Detail Modal */}
                        {crmSelectedUser && (
                            <div className="fixed inset-0 bg-black/60 z-[9999] flex items-center justify-center p-4 backdrop-blur-sm" onClick={() => setCrmSelectedUser(null)}>
                                <div className="bg-white w-full max-w-3xl rounded-2xl border border-slate-100 shadow-lg max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
                                    <div className="p-6">
                                        <div className="flex items-center justify-between mb-6">
                                            <h3 className="font-extrabold text-slate-800 text-lg flex items-center gap-2">
                                                <i className="fa-solid fa-user-circle text-blue-600"></i>
                                                {crmSelectedUser.name}
                                            </h3>
                                            <button onClick={() => setCrmSelectedUser(null)} className="w-8 h-8 flex items-center justify-center rounded-full bg-slate-50 hover:bg-red-50 text-slate-400 hover:text-red-500 transition text-sm cursor-pointer border-0">
                                                <i className="fa-solid fa-xmark"></i>
                                            </button>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Email</span><span className="font-bold text-slate-800">{crmSelectedUser.email}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Phone</span><span className="text-slate-600">{crmSelectedUser.phone || '-'}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Role</span><span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full font-bold text-[10px]">{crmSelectedUser.role}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Location</span><span className="text-slate-600">{crmSelectedUser.location || '-'}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Registered</span><span className="text-slate-500">{crmSelectedUser.created_at ? new Date(crmSelectedUser.created_at).toLocaleString('en-IN') : '-'}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Last Login</span><span className="text-slate-500">{crmSelectedUser.last_login ? new Date(crmSelectedUser.last_login).toLocaleString('en-IN') : '-'}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Total Orders</span><span className="font-black text-slate-800">{crmSelectedUser.order_count || 0}</span></div>
                                            <div><span className="text-[10px] uppercase font-bold text-slate-400 block">Lifetime Value</span><span className="font-black text-emerald-600">₹{(crmSelectedUser.total_spent || 0).toFixed(0)}</span></div>
                                        </div>
                                        {/* Login History */}
                                        {crmSelectedUser.login_history && crmSelectedUser.login_history.length > 0 && (
                                            <div className="border-t border-slate-100 pt-4 mb-4">
                                                <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-clock-rotate-left text-slate-400"></i> Login History ({crmSelectedUser.login_history.length})</h4>
                                                <div className="max-h-[200px] overflow-y-auto text-xs space-y-1.5">
                                                    {crmSelectedUser.login_history.map((lh, i) => (
                                                        <div key={lh.id || i} className="flex justify-between py-1.5 px-3 bg-slate-50 rounded-lg">
                                                            <span className="text-slate-500">{lh.timestamp ? new Date(lh.timestamp).toLocaleString('en-IN') : '-'}</span>
                                                            <span className="text-slate-400 text-[9px] truncate max-w-[200px]">{lh.ip_address} · {lh.user_agent?.slice(0, 40)}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                        {/* Drafts */}
                                        {crmSelectedUser.drafts && crmSelectedUser.drafts.length > 0 && (
                                            <div className="border-t border-slate-100 pt-4">
                                                <h4 className="font-bold text-slate-700 text-xs flex items-center gap-2 mb-3"><i className="fa-solid fa-pen-to-square text-amber-500"></i> Saved Drafts ({crmSelectedUser.drafts.length})</h4>
                                                <div className="space-y-1.5 text-xs">
                                                    {crmSelectedUser.drafts.map((d) => (
                                                        <div key={d.id} className="flex justify-between py-1.5 px-3 bg-amber-50 rounded-lg">
                                                            <span className="font-bold text-slate-700">{d.doc_type}</span>
                                                            <span className="text-slate-400">{d.updated_at ? new Date(d.updated_at).toLocaleString('en-IN') : '-'}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                );
            };"""
            
    # Find start and replace up to end_idx.
    # Note: we need to replace starting from start_idx up to the end tag.
    # So the chunk to replace is: content[start_idx:end_idx]
    # We replace it with new_code + "\n            "
    
    target_text = content[start_idx:end_idx]
    
    print(f"Replacing code from offset {start_idx} to {end_idx}...")
    
    updated_content = content[:start_idx] + new_code + "\n            " + content[end_idx:]
    
    with open(jsx_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print("Function replaced successfully!")

if __name__ == '__main__':
    main()
