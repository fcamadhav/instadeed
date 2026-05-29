import re

hub_file = 'Madhav_Drafting_Hub.html'

with open(hub_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fonts link and add Google Identity Services script in <head>
target_head = """    <!-- Fonts -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&display=swap"
        rel="stylesheet">"""

replacement_head = """    <!-- Fonts -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&family=Libre+Baskerville:wght@700&display=swap"
        rel="stylesheet">
    <!-- Google Identity Services SDK -->
    <script src="https://accounts.google.com/gsi/client" async defer></script>"""

if target_head in content:
    content = content.replace(target_head, replacement_head)
    print("1. Head script & fonts replaced successfully.")
else:
    # Try with different whitespaces
    content = re.sub(
        r'<!-- Fonts -->\s*<link href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.4\.0/css/all\.min\.css" rel="stylesheet">\s*<link\s+href="https://fonts\.googleapis\.com/css2\?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&display=swap"\s+rel="stylesheet">',
        replacement_head,
        content
    )
    print("1. Head script & fonts regex-replaced.")

# 2. Add user state to Home Component
target_state = """        function Home() {
            const [activeTab, setActiveTab] = useState('RENT'); // 'RENT', 'ATS', 'NOIDA_TRANSFER' etc.
            const [activeAuthority, setActiveAuthority] = useState('ALL');"""

replacement_state = """        function Home() {
            const [activeTab, setActiveTab] = useState('RENT'); // 'RENT', 'ATS', 'NOIDA_TRANSFER' etc.
            const [activeAuthority, setActiveAuthority] = useState('ALL');
            const [user, setUser] = useState(null);"""

if target_state in content:
    content = content.replace(target_state, replacement_state)
    print("2. Home state 'user' added successfully.")
else:
    print("Warning: target_state not found.")

# 3. Rebrand default transferee names
transferee_targets = [
    ("transferee1Parent: 'MR. MADHAV MAHESHWARI (Husb)',", "transferee1Parent: 'MR. ROHAN SHARMA (Husb)',"),
    ("transferee2Name: 'MR. MADHAV MAHESHWARI',", "transferee2Name: 'MR. ROHAN SHARMA',"),
    ("transferee2Parent: 'MR. AJAY MAHESHWARI',", "transferee2Parent: 'MR. AJAY SHARMA',")
]

for tgt, rep in transferee_targets:
    if tgt in content:
        content = content.replace(tgt, rep)
        print(f"3. Rebranded {tgt.split(':')[0]} successfully.")
    else:
        print(f"Warning: {tgt} not found.")

# 4. Modify Mount useEffect to load session and parse URL params
target_mount = """            useEffect(() => {
                const saved = localStorage.getItem('madhav_legal_suite_v4_clean');
                if (saved) {
                    try {
                        const parsed = JSON.parse(saved);
                        if (parsed.rent) setRentData({ ...defaultRentData, ...parsed.rent });
                        if (parsed.ats) setAtsData({ ...defaultATSData, ...parsed.ats });
                        if (parsed.reg) setRegData({ ...defaultRegData, ...parsed.reg });
                        if (parsed.tm48) setTm48Data({ ...defaultTM48Data, ...parsed.tm48 });
                        if (parsed.gnida) setGnidaData({ ...defaultGNIDAData, ...parsed.gnida });
                        if (parsed.mutation) setMutationData({ ...defaultMutationData, ...parsed.mutation });
                        if (parsed.tmApp) setTmAppData({ ...defaultTMAppData, ...parsed.tmApp });
                        if (parsed.gnidaRegistry) setGnidaRegistryData(prev => ({ ...prev, ...parsed.gnidaRegistry }));
                        if (parsed.gnidaPtm) setGnidaPtmData(prev => ({ ...prev, ...parsed.gnidaPtm }));
                        if (parsed.noidaTransfer) setNoidaTransferData(prev => ({ ...prev, ...parsed.noidaTransfer }));

                        if (parsed.tab) setActiveTab(parsed.tab);
                    } catch (e) { console.error(e); }
                }
            }, []);"""

replacement_mount = """            useEffect(() => {
                // Read user session
                const sessionStr = localStorage.getItem('instadeed_user_session');
                if (sessionStr) {
                    try {
                        setUser(JSON.parse(sessionStr));
                    } catch (e) { console.error("Error loading session:", e); }
                }

                // Check URL parameter routing
                const params = new URLSearchParams(window.location.search);
                const docParam = params.get('doc');
                let routedTab = null;
                let routedAuth = null;

                if (docParam) {
                    const docLower = docParam.toLowerCase();
                    if (docLower.includes('gnida')) routedAuth = 'GNIDA';
                    else if (docLower.includes('noida')) routedAuth = 'NOIDA';
                    else if (docLower.includes('yeida')) routedAuth = 'YEIDA';
                    else if (docLower.includes('gda')) routedAuth = 'GDA';
                    else if (docLower.includes('gzb')) routedAuth = 'GDA';

                    if (docLower.includes('registered rent') || docLower.includes('reg_rent')) {
                        routedTab = 'REG_RENT';
                        routedAuth = routedAuth || 'ALL';
                    } else if (docLower.includes('rent agreement') || docLower.includes('rent')) {
                        routedTab = 'RENT';
                        routedAuth = routedAuth || 'ALL';
                    } else if (docLower.includes('agreement to sell') || docLower.includes('ats')) {
                        routedTab = 'ATS';
                        routedAuth = routedAuth || 'ALL';
                    } else if (docLower.includes('form tm-48') || docLower.includes('tm48')) {
                        routedTab = 'TM48';
                        routedAuth = routedAuth || 'ALL';
                    } else if (docLower.includes('kya form') || docLower.includes('kya')) {
                        routedTab = 'KYA';
                        routedAuth = routedAuth || 'GNIDA';
                    } else if (docLower.includes('mutation application') || docLower.includes('mutation')) {
                        routedTab = 'MUTATION';
                        routedAuth = routedAuth || 'GNIDA';
                    } else if (docLower.includes('ptm mortgage') || docLower.includes('gnida_ptm')) {
                        routedTab = 'GNIDA_PTM';
                        routedAuth = routedAuth || 'GNIDA';
                    } else if (docLower.includes('tm application') || docLower.includes('tm_app')) {
                        routedTab = 'TM_APP';
                        routedAuth = routedAuth || 'GNIDA';
                    } else if (docLower.includes('transfer deed registry') || docLower.includes('gnida_registry')) {
                        routedTab = 'GNIDA_REGISTRY';
                        routedAuth = routedAuth || 'GNIDA';
                    } else if (docLower.includes('transfer application') || docLower.includes('noida_transfer')) {
                        routedTab = 'NOIDA_TRANSFER';
                        routedAuth = routedAuth || 'NOIDA';
                    } else if (docLower.includes('custom affidavit') || docLower.includes('coming_soon')) {
                        routedTab = 'COMING_SOON';
                        routedAuth = routedAuth || 'ALL';
                    }
                }

                const saved = localStorage.getItem('madhav_legal_suite_v4_clean');
                if (saved) {
                    try {
                        const parsed = JSON.parse(saved);
                        if (parsed.rent) setRentData({ ...defaultRentData, ...parsed.rent });
                        if (parsed.ats) setAtsData({ ...defaultATSData, ...parsed.ats });
                        if (parsed.reg) setRegData({ ...defaultRegData, ...parsed.reg });
                        if (parsed.tm48) setTm48Data({ ...defaultTM48Data, ...parsed.tm48 });
                        if (parsed.gnida) setGnidaData({ ...defaultGNIDAData, ...parsed.gnida });
                        if (parsed.mutation) setMutationData({ ...defaultMutationData, ...parsed.mutation });
                        if (parsed.tmApp) setTmAppData({ ...defaultTMAppData, ...parsed.tmApp });
                        if (parsed.gnidaRegistry) setGnidaRegistryData(prev => ({ ...prev, ...parsed.gnidaRegistry }));
                        if (parsed.gnidaPtm) setGnidaPtmData(prev => ({ ...prev, ...parsed.gnidaPtm }));
                        if (parsed.noidaTransfer) setNoidaTransferData(prev => ({ ...prev, ...parsed.noidaTransfer }));

                        if (docParam) {
                            if (routedTab) setActiveTab(routedTab);
                            if (routedAuth) setActiveAuthority(routedAuth);
                        } else {
                            if (parsed.tab) setActiveTab(parsed.tab);
                            if (parsed.authority) setActiveAuthority(parsed.authority);
                        }
                    } catch (e) { console.error(e); }
                } else {
                    if (docParam) {
                        if (routedTab) setActiveTab(routedTab);
                        if (routedAuth) setActiveAuthority(routedAuth);
                    }
                }
            }, []);"""

if target_mount in content:
    content = content.replace(target_mount, replacement_mount)
    print("4. Mount useEffect modified successfully.")
else:
    print("Warning: target_mount not found.")

# 5. Modify Save useEffect to persist authority
target_save = """            useEffect(() => {
                const suiteData = {
                    rent: rentData,
                    ats: atsData,
                    reg: regData,
                    gnida: gnidaData,
                    mutation: mutationData,
                    tmApp: tmAppData,
                    tm48: tm48Data,
                    gnidaRegistry: gnidaRegistryData,
                    gnidaPtm: gnidaPtmData,
                    noidaTransfer: noidaTransferData,

                    tab: activeTab
                };
                localStorage.setItem('madhav_legal_suite_v4_clean', JSON.stringify(suiteData));
            }, [rentData, atsData, regData, tm48Data, gnidaData, mutationData, tmAppData, gnidaRegistryData, gnidaPtmData, noidaTransferData, activeTab]);"""

replacement_save = """            useEffect(() => {
                const suiteData = {
                    rent: rentData,
                    ats: atsData,
                    reg: regData,
                    gnida: gnidaData,
                    mutation: mutationData,
                    tmApp: tmAppData,
                    tm48: tm48Data,
                    gnidaRegistry: gnidaRegistryData,
                    gnidaPtm: gnidaPtmData,
                    noidaTransfer: noidaTransferData,
                    tab: activeTab,
                    authority: activeAuthority
                };
                localStorage.setItem('madhav_legal_suite_v4_clean', JSON.stringify(suiteData));
            }, [rentData, atsData, regData, tm48Data, gnidaData, mutationData, tmAppData, gnidaRegistryData, gnidaPtmData, noidaTransferData, activeTab, activeAuthority]);"""

if target_save in content:
    content = content.replace(target_save, replacement_save)
    print("5. Save useEffect modified successfully.")
else:
    print("Warning: target_save not found.")

# 6. Rebrand file download name
target_download = "link.download = `Madhav_${activeTab}_${name}.json`;"
replacement_download = "link.download = `Instadeed_${activeTab}_${name}.json`;"

if target_download in content:
    content = content.replace(target_download, replacement_download)
    print("6. Rebranded download name prefix successfully.")
else:
    print("Warning: target_download not found.")

# 7. Replace massive Base64 logo in header sidebar
target_logo_regex = r'<div className="flex items-center h-10">\s*<img src="data:image/png;base64,[^"]+" className="h-8 object-contain" alt="INSTADEED" />\s*</div>'

replacement_logo = """<div className="flex items-center h-10">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190 35" className="h-8 w-auto">
                                            <g transform="translate(2, 2)">
                                                <path d="M3 1 C 1.5 1, 1 1.5, 1 3 L 1 27 C 1 28.5, 1.5 29, 3 29 L 19 29 C 20.5 29, 21 28.5, 21 27 L 21 9 L 13 1 L 3 1 Z" fill="none" stroke="#8B0000" strokeWidth="2" strokeLinejoin="round"/>
                                                <path d="M13 1 L 13 9 L 21 9" fill="none" stroke="#8B0000" strokeWidth="2" strokeLinejoin="round"/>
                                                <circle cx="15" cy="21" r="3.5" fill="#D8C7A5" />
                                                <circle cx="15" cy="21" r="2" fill="#8B0000" />
                                                <line x1="5" y1="7" x2="10" y2="7" stroke="#94A3B8" strokeWidth="1.5" strokeLinecap="round"/>
                                                <line x1="5" y1="12" x2="17" y2="12" stroke="#94A3B8" strokeWidth="1.5" strokeLinecap="round"/>
                                                <line x1="5" y1="17" x2="10" y2="17" stroke="#94A3B8" strokeWidth="1.5" strokeLinecap="round"/>
                                            </g>
                                            <text x="32" y="24" fontFamily="'Libre Baskerville', serif" fontWeight="700" fontSize="19" letterSpacing="0.5">
                                                <tspan fill="#0f172a">INSTA</tspan>
                                                <tspan fill="#8B0000">DEED</tspan>
                                            </text>
                                        </svg>
                                    </div>
                                    {user ? (
                                        <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-full py-1 pl-1 pr-3 shadow-sm text-xs text-slate-700">
                                            <img src={user.picture} alt={user.name} className="w-6 h-6 rounded-full" />
                                            <span className="font-semibold truncate max-w-[80px]">{user.name.split(' ')[0]}</span>
                                            <button onClick={() => {
                                                localStorage.removeItem('instadeed_user_session');
                                                setUser(null);
                                                alert("Signed out successfully.");
                                            }} className="text-slate-400 hover:text-rose-600 transition ml-1" title="Sign Out">
                                                <i className="fa-solid fa-right-from-bracket"></i>
                                            </button>
                                        </div>
                                    ) : (
                                        <button onClick={() => {
                                            const mockUser = {
                                                name: "Demo Signee",
                                                email: "signee@instadeed.com",
                                                picture: "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
                                            };
                                            localStorage.setItem('instadeed_user_session', JSON.stringify(mockUser));
                                            setUser(mockUser);
                                            alert("Signed in successfully as " + mockUser.name);
                                        }} className="text-[10px] uppercase font-bold text-slate-500 hover:text-indigo-600 border border-slate-200 rounded-full px-2.5 py-1 transition bg-slate-50" title="Sign In (Mock)">
                                            Sign In
                                        </button>
                                    )}"""

new_content, count = re.subn(target_logo_regex, replacement_logo, content)
if count > 0:
    content = new_content
    print(f"7. Logo and User Profile Widget integrated successfully ({count} replacement made).")
else:
    print("Warning: target_logo_regex not matched.")

# 8. Rebrand Advocate Madhav Maheshwari details in document previews
# Rebrand line 3596
content = content.replace(
    '<div className="font-bold text-lg">Advocate Madhav Maheshwari</div>',
    '<div className="font-bold text-lg">Advocate Rohan Sharma</div>'
)
print("8a. Rebranded Advocate Madhav Maheshwari in line 3596.")

# Rebrand line 3941
content = content.replace(
    'Advocate Madhav Maheshwari (8899999321)',
    'Advocate Rohan Sharma (8899999321)'
)
print("8b. Rebranded Advocate Madhav Maheshwari in line 3941.")

# Rebrand line 5044 (TM-48 body text)
target_tm48_body = 'do hereby authorize <span className="font-bold">Advocate Madhav Maheshwari</span>, 1842, -Bluebell, Gaur Saundaryam Sector-Techzone-04, Greater Noida West, Gautam Buddha Nagar, Uttar Pradesh India, to act jointly and severally as my attorneys for registrations, oppositions, objections, assignments, rectifications, renewals and all such matters on my behalf and request that all notices, requisitions and communications relating thereto may be sent to Advocate Madhav Maheshwari at the address listed above. Advocate Madhav Maheshwari is authorized to appoint any person or persons'
replacement_tm48_body = 'do hereby authorize <span className="font-bold">Advocate Rohan Sharma</span>, 123, Legal Plaza, Sector-62, Noida, Gautam Buddha Nagar, Uttar Pradesh, India, to act jointly and severally as my attorneys for registrations, oppositions, objections, assignments, rectifications, renewals and all such matters on my behalf and request that all notices, requisitions and communications relating thereto may be sent to Advocate Rohan Sharma at the address listed above. Advocate Rohan Sharma is authorized to appoint any person or persons'

if target_tm48_body in content:
    content = content.replace(target_tm48_body, replacement_tm48_body)
    print("8c. Rebranded TM-48 body text advocate authorization.")
else:
    # Try regex matching to be safe
    print("Warning: target_tm48_body not matched exactly.")

# Rebrand lines 5052-5057 (TM-48 address footer)
target_tm48_address = """                                                    Advocate Madhav Maheshwari<br />
                                                    1842, BlueBell, Gaur Saundaryam<br />
                                                    Sector-Techzone-04, Greater Noida West,<br />
                                                    Gautam Buddha Nagar, Uttar Pradesh.<br />
                                                    Phone Number: +91 8899999321<br />
                                                    Email Address: fcamadhav@gmail.com"""

replacement_tm48_address = """                                                    Advocate Rohan Sharma<br />
                                                    123, Legal Plaza, Sector-62,<br />
                                                    Noida, Gautam Buddha Nagar, Uttar Pradesh.<br />
                                                    Phone Number: +91 9999999999<br />
                                                    Email Address: attorney@instadeed.com"""

if target_tm48_address in content:
    content = content.replace(target_tm48_address, replacement_tm48_address)
    print("8d. Rebranded TM-48 footer address details successfully.")
else:
    # Try a looser replacement just in case of whitespace differences
    content = re.sub(
        r'Advocate Madhav Maheshwari\s*<br\s*/>\s*1842,\s*BlueBell,\s*Gaur\s*Saundaryam\s*<br\s*/>\s*Sector-Techzone-04,\s*Greater\s*Noida\s*West,\s*<br\s*/>\s*Gautam\s*Buddha\s*Nagar,\s*Uttar\s*Pradesh\.\s*<br\s*/>\s*Phone\s*Number:\s*\+91\s*8899999321\s*<br\s*/>\s*Email\s*Address:\s*fcamadhav@gmail\.com',
        replacement_tm48_address,
        content
    )
    print("8d. Rebranded TM-48 footer address details via regex.")

# Save modified content back
with open(hub_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll replacements processed and written back to Madhav_Drafting_Hub.html!")
