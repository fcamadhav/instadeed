import re

file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def safe_replace(text, target, rep):
    if target in text:
        return text.replace(target, rep)
    target_rn = target.replace('\n', '\r\n')
    rep_rn = rep.replace('\n', '\r\n')
    if target_rn in text:
        return text.replace(target_rn, rep_rn)
    print(f"FAILED TO REPLACE BLOCK: {repr(target[:80])}...")
    return text

# 1. State variable declarations (idempotent check)
if 'gnidaPackageDocs' not in content:
    target_state = "            const [activeTab, setActiveTab] = useState('HOME'); // 'RENT', 'ATS', 'NOIDA_TRANSFER' etc."
    rep_state = """            const [activeTab, setActiveTab] = useState('HOME'); // 'RENT', 'ATS', 'NOIDA_TRANSFER' etc.
            const [gnidaPackageDocs, setGnidaPackageDocs] = useState({
                kya: true,
                tm: true,
                mutation: true,
                registry: true,
                ptm: true
            });
            const [gnidaPackageData, setGnidaPackageData] = useState(defaultGnidaPackageData);
            const [librarySearch, setLibrarySearch] = useState('');
            const [libraryFilter, setLibraryFilter] = useState('ALL');
            const [viewOnlyMode, setViewOnlyMode] = useState(false);
            const [viewOrderId, setViewOrderId] = useState('');"""
    content = safe_replace(content, target_state, rep_state)

# 2. Add defaultGnidaPackageData right before defaultATSData (idempotent check)
if 'defaultGnidaPackageData =' not in content:
    target_ats_def = "            const defaultATSData = {"
    rep_ats_def = """            const defaultGnidaPackageData = {
                // Property
                projectName: 'GAUR SAUNDARYAM',
                towerName: 'BLUE BELL',
                floor: '17th',
                flatNo: '1842',
                parking: 'One Covered Car Parking',
                superAreaSqFt: '1595',
                superAreaSqMtr: '148.18',
                plotNo: 'GH-05C',
                sector: 'TechZone-IV',
                block: '',
                plotSize: '1595',
                allotmentNo: 'ALLOT-887766',
                allotmentDate: '2024-05-10',
                schemeName: 'Residential Flat Scheme',
                schemeCode: 'RFS-01',
                
                // Seller (Transferor)
                transferorCount: '2',
                transferor1Name: 'MR. D. SAM SUNDAR',
                transferor1Parent: 'MR. PRAKASA RAO',
                transferor1Pan: 'AMWPD7168G',
                transferor1Aadhar: '2290 4493 9878',
                transferor1Phone: '9876543210',
                transferor1Email: 'transferor1@example.com',
                transferor1Address: 'A-50/2, A - BLOCK, DDA SFS FLATS, PVR ANUPAM, SAKET, DELHI-110017',
                transferor1Age: '45',
                
                transferor2Name: 'MRS. MRIDULA KAKARLA',
                transferor2Parent: 'MR. D. SAM SUNDAR (Husb)',
                transferor2Pan: 'CDQPK7887N',
                transferor2Aadhar: '5059 3158 0682',
                transferor2Phone: '',
                transferor2Email: '',
                transferor2Address: '',
                transferor2Age: '40',
                
                // Buyer (Transferee)
                transfereeCount: '2',
                transferee1Name: 'MRS. ISHA ARORA',
                transferee1Parent: 'MR. ROHAN SHARMA (Husb)',
                transferee1Pan: 'BHZPA7056D',
                transferee1Aadhar: '9499 8191 6571',
                transferee1Phone: '9999988888',
                transferee1Email: 'transferee1@example.com',
                transferee1Address: 'FLAT NO. J-23077, 14TH AVENUE GAUR CITY-2, GREATER NOIDA WEST, SECTOR-16C, UTTAR PRADESH 201009',
                transferee1Age: '32',
                
                transferee2Name: 'MR. ROHAN SHARMA',
                transferee2Parent: 'MR. AJAY SHARMA',
                transferee2Pan: 'DTEPM4364K',
                transferee2Aadhar: '8823 7664 3135',
                transferee2Phone: '9999977777',
                transferee2Email: 'transferee2@example.com',
                transferee2Address: '',
                transferee2Age: '35',
                
                // Transfer Details
                tmNo: 'Gr. Noida/Property/BRS/2024/1854',
                tmDate: '2024-10-24',
                circleRate: '32,000',
                saleConsideration: '1,67,00,000',
                stampDutyPaidOn: '1,67,00,000',
                totalStampDuty: '8,35,000',
                transferDate: '2024-10-28',
                leaseDate: '2011-05-10',
                subLeaseDate: '2017-09-16',
                
                // Mutation Extra
                subRegistrar: 'Sadar, Greater Noida',
                jildNo: '456',
                regPageFrom: '12',
                regPageTo: '36',
                regSerialNo: '9876',
                regDate: '2024-10-29',
                
                // PTM Extra
                mortgagingAgencyName: 'State Bank of India',
                mortgagingAgencyAddress: 'G. Noida Commercial Branch, Sector Alpha-1',
                ptmPinCode: '201308',
                ptmAcknowledgementNo: 'PTM-9988-ACK',
                ptmReceivingDate: '2024-11-02',
                
                // TM App Extra
                formSlNo: 'SL-2024-00192',
                dateOfIssue: '2024-10-25',
                processingFeeDraftNo: '112233',
                processingFeeDate: '2024-10-25',
                processingFeeBank: 'HDFC Bank',
                transferChargeDraftNo: '445566',
                transferChargeDate: '2024-10-25',
                transferChargeAmount: '97,500',
                transferChargeBank: 'ICICI Bank',
                
                // Witnesses
                witness1Name: 'Mr. Witness One',
                witness1Address: 'Sector Beta-2, Greater Noida',
                witness1Phone: '9812345678',
                witness1Father: 'Father Witness One',
                witness1Aadhar: '1111 2222 3333',
                witness1Id: 'AADHAR',
                
                witness2Name: 'Mr. Witness Two',
                witness2Address: 'Sector Gamma-1, Greater Noida',
                witness2Phone: '9812345679',
                witness2AddressSame: true,
                witness2Father: 'Father Witness Two',
                witness2Aadhar: '4444 5555 6666',
                witness2Id: 'AADHAR',
                
                place: 'Greater Noida',
                dated: new Date().toISOString().split('T')[0],
                signDate: new Date().toISOString().split('T')[0]
            };

            const defaultATSData = {"""
    content = safe_replace(content, target_ats_def, rep_ats_def)

# 3. Add useEffect hook to sync gnidaPackageData to individual document states (idempotent check)
if 'setGnidaRegistryData(prev => ({' in content and 'projectName: p.projectName,' in content:
    pass
else:
    target_sync_hook = "            // Auto-calculate ATS Financials"
    rep_sync_hook = """            // Sync GNIDA Package Data to individual template states
            useEffect(() => {
                if (activeTab !== 'GNIDA_PACKAGE' || !gnidaPackageData) return;
                
                const p = gnidaPackageData;
                
                // 1. Sync to Registry Data
                setGnidaRegistryData(prev => ({
                    ...prev,
                    projectName: p.projectName,
                    towerName: p.towerName,
                    floor: p.floor,
                    flatNo: p.flatNo,
                    parking: p.parking,
                    superAreaSqFt: p.superAreaSqFt,
                    superAreaSqMtr: p.superAreaSqMtr,
                    plotNo: p.plotNo,
                    sector: p.sector,
                    block: p.block,
                    tmNo: p.tmNo,
                    tmDate: p.tmDate,
                    circleRate: p.circleRate,
                    saleConsideration: p.saleConsideration,
                    stampDutyPaidOn: p.stampDutyPaidOn,
                    totalStampDuty: p.totalStampDuty,
                    transferDate: p.transferDate,
                    leaseDate: p.leaseDate,
                    subLeaseDate: p.subLeaseDate,
                    
                    transferorCount: p.transferorCount,
                    transferor1Name: p.transferor1Name,
                    transferor1Parent: p.transferor1Parent,
                    transferor1Pan: p.transferor1Pan,
                    transferor1Aadhar: p.transferor1Aadhar,
                    transferor1Address: p.transferor1Address,
                    transferor2Name: p.transferor2Name,
                    transferor2Parent: p.transferor2Parent,
                    transferor2Pan: p.transferor2Pan,
                    transferor2Aadhar: p.transferor2Aadhar,
                    
                    transfereeCount: p.transfereeCount,
                    transferee1Name: p.transferee1Name,
                    transferee1Parent: p.transferee1Parent,
                    transferee1Pan: p.transferee1Pan,
                    transferee1Aadhar: p.transferee1Aadhar,
                    transferee1Address: p.transferee1Address,
                    transferee2Name: p.transferee2Name,
                    transferee2Parent: p.transferee2Parent,
                    transferee2Pan: p.transferee2Pan,
                    transferee2Aadhar: p.transferee2Aadhar,
                    
                    witness1: p.witness1Name,
                    witness2: p.witness2Name
                }));
                
                // 2. Sync to KYA (gnidaData)
                setGnidaData(prev => ({
                    ...prev,
                    allotteeName: p.transferee1Name,
                    fatherSpouseName: p.transferee1Parent,
                    schemeName: p.schemeName,
                    schemeCode: p.schemeCode,
                    allotmentNo: p.allotmentNo,
                    propertyNo: p.flatNo || p.plotNo,
                    block: p.block,
                    sector: p.sector,
                    allotmentDate: p.allotmentDate,
                    plotSize: p.superAreaSqFt || p.plotSize,
                    
                    allottee1Name: p.transferee1Name,
                    allottee2Name: p.transferee2Name,
                    
                    corrAddress1: p.transferee1Address ? p.transferee1Address.slice(0, 30) : '',
                    corrAddress2: p.transferee1Address ? p.transferee1Address.slice(30, 60) : '',
                    corrAddress3: p.transferee1Address ? p.transferee1Address.slice(60, 90) : '',
                    
                    permAddress1: p.transferee1Address ? p.transferee1Address.slice(0, 30) : '',
                    permAddress2: p.transferee1Address ? p.transferee1Address.slice(30, 60) : '',
                    permAddress3: p.transferee1Address ? p.transferee1Address.slice(60, 90) : '',
                    
                    allottee1Mobile: p.transferee1Phone,
                    allottee2Mobile: p.transferee2Phone,
                    allottee1Email: p.transferee1Email,
                    allottee2Email: p.transferee2Email,
                    
                    allottee1PAN: p.transferee1Pan,
                    allottee2PAN: p.transferee2Pan,
                    allottee1Aadhar: p.transferee1Aadhar,
                    allottee2Aadhar: p.transferee2Aadhar
                }));
                
                // 3. Sync to Mutation Data
                setMutationData(prev => ({
                    ...prev,
                    applicantName: p.transferee1Name,
                    flatNo: p.flatNo,
                    block: p.block,
                    project: p.projectName,
                    plotNo: p.plotNo,
                    sector: p.sector,
                    transferMemoNo: p.tmNo,
                    transferMemoDate: p.tmDate,
                    subRegistrar: p.subRegistrar,
                    jildNo: p.jildNo,
                    regPageFrom: p.regPageFrom,
                    regPageTo: p.regPageTo,
                    regSerialNo: p.regSerialNo,
                    regDate: p.regDate,
                    place: p.place,
                    dated: p.dated
                }));
                
                // 4. Sync to TM App Data
                setTmAppData(prev => ({
                    ...prev,
                    formSlNo: p.formSlNo,
                    dateOfIssue: p.dateOfIssue,
                    
                    transferorName: p.transferor1Name,
                    transferorAge: p.transferor1Age,
                    transferorParentName: p.transferor1Parent,
                    transferorAddress: p.transferor1Address,
                    
                    schemeName: p.schemeName,
                    allotmentNo: p.allotmentNo,
                    plotNo: p.plotNo || p.flatNo,
                    block: p.block,
                    sector: p.sector,
                    area: p.superAreaSqFt || p.plotSize,
                    
                    transfereeName: p.transferee1Name,
                    transfereeAge: p.transferee1Age,
                    transfereeParentName: p.transferee1Parent,
                    transfereeAddress: p.transferee1Address,
                    
                    processingFeeDraftNo: p.processingFeeDraftNo,
                    processingFeeDate: p.processingFeeDate,
                    processingFeeBank: p.processingFeeBank,
                    transferChargeDraftNo: p.transferChargeDraftNo,
                    transferChargeDate: p.transferChargeDate,
                    transferChargeAmount: p.transferChargeAmount,
                    transferChargeBank: p.transferChargeBank
                }));
                
                // 5. Sync to PTM Data
                setGnidaPtmData(prev => ({
                    ...prev,
                    schemeName: p.schemeName,
                    schemeCode: p.schemeCode,
                    plotSize: p.superAreaSqFt || p.plotSize,
                    block: p.block,
                    plotNo: p.plotNo || p.flatNo,
                    allotmentNo: p.allotmentNo,
                    allotteeName: p.transferee1Name,
                    mortgagingAgencyName: p.mortgagingAgencyName,
                    mortgagingAgencyAddress: p.mortgagingAgencyAddress,
                    pinCode: p.ptmPinCode,
                    applicationDate: p.dated,
                    acknowledgementNo: p.ptmAcknowledgementNo,
                    receivingDate: p.ptmReceivingDate
                }));
            }, [gnidaPackageData, activeTab]);

            // Auto-calculate ATS Financials"""
    content = safe_replace(content, target_sync_hook, rep_sync_hook)

# 4. JSON Auto-save support for gnidaPackage (idempotent check)
if 'gnidaPackage: gnidaPackageData' not in content:
    target_save = """                    ecommRP: ecommRPData,
                    tab: activeTab,
                    authority: activeAuthority"""
    
    rep_save = """                    ecommRP: ecommRPData,
                    gnidaPackage: gnidaPackageData,
                    gnidaPackageDocs: gnidaPackageDocs,
                    tab: activeTab,
                    authority: activeAuthority"""
    content = safe_replace(content, target_save, rep_save)
    
    target_save_deps = """}, [rentData, atsData, regData, tm48Data, gnidaData, mutationData, tmAppData, gnidaRegistryData, gnidaPtmData, noidaTransferData, ecommTCData, ecommPPData, ecommRPData, activeTab, activeAuthority]);"""
    rep_save_deps = """}, [rentData, atsData, regData, tm48Data, gnidaData, mutationData, tmAppData, gnidaRegistryData, gnidaPtmData, noidaTransferData, ecommTCData, ecommPPData, ecommRPData, gnidaPackageData, gnidaPackageDocs, activeTab, activeAuthority]);"""
    content = safe_replace(content, target_save_deps, rep_save_deps)

# 5. LocalStorage initialization checks (idempotent check)
if 'parsed.gnidaPackage' not in content:
    target_load = """                        if (parsed.ecommRP) setEcommRPData(prev => ({ ...prev, ...parsed.ecommRP }));"""
    rep_load = """                        if (parsed.ecommRP) setEcommRPData(prev => ({ ...prev, ...parsed.ecommRP }));
                        if (parsed.gnidaPackage) setGnidaPackageData(prev => ({ ...prev, ...parsed.gnidaPackage }));
                        if (parsed.gnidaPackageDocs) setGnidaPackageDocs(prev => ({ ...prev, ...parsed.gnidaPackageDocs }));"""
    content = safe_replace(content, target_load, rep_load)

# 6. saveDefault, loadDefault, clearAllData, downloadJSON, uploadJSON support (idempotent checks)
if 'activeTab === \'GNIDA_PACKAGE\'' not in content:
    content = safe_replace(content, 
                           "else if (activeTab === 'ECOMM_RP') currentData = ecommRPData;",
                           "else if (activeTab === 'ECOMM_RP') currentData = ecommRPData;\n                else if (activeTab === 'GNIDA_PACKAGE') currentData = gnidaPackageData;")
                           
    content = safe_replace(content,
                           "else if (activeTab === 'ECOMM_RP') setEcommRPData(parsed);",
                           "else if (activeTab === 'ECOMM_RP') setEcommRPData(parsed);\n                        else if (activeTab === 'GNIDA_PACKAGE') setGnidaPackageData(parsed);")

    content = safe_replace(content,
                           "else if (activeTab === 'ECOMM_RP') { currentData = ecommRPData; name = ecommRPData.companyName || 'Draft'; }",
                           "else if (activeTab === 'ECOMM_RP') { currentData = ecommRPData; name = ecommRPData.companyName || 'Draft'; }\n                else if (activeTab === 'GNIDA_PACKAGE') { currentData = gnidaPackageData; name = (gnidaPackageData.transferee1Name || 'Package') + '_5_in_1'; }")

    content = safe_replace(content,
                           "else if (activeTab === 'ECOMM_RP') setEcommRPData(prev => ({ ...prev, ...loaded }));",
                           "else if (activeTab === 'ECOMM_RP') setEcommRPData(prev => ({ ...prev, ...loaded }));\n                        else if (activeTab === 'GNIDA_PACKAGE') setGnidaPackageData(prev => ({ ...prev, ...loaded }));")

    content = safe_replace(content,
                           "setEcommRPData(defaultEcommRPData);",
                           "setEcommRPData(defaultEcommRPData);\n                    setGnidaPackageData(defaultGnidaPackageData);")

# 7. Document name title auto-calculation hook
if 'else if (activeTab === \'GNIDA_PACKAGE\') name = buildDocumentName' not in content:
    target_doc_name = "else if (activeTab === 'ECOMM_RP') name = buildDocumentName('', ecommRPData.companyName, 'Refund Policy');"
    rep_doc_name = "else if (activeTab === 'ECOMM_RP') name = buildDocumentName('', ecommRPData.companyName, 'Refund Policy');\n                else if (activeTab === 'GNIDA_PACKAGE') name = buildDocumentName(gnidaPackageData.flatNo, gnidaPackageData.transferee1Name, 'GNIDA_5in1_Package');"
    content = safe_replace(content, target_doc_name, rep_doc_name)

# 8. Add GNIDA 5-in-1 Package button at the top of the GNIDA selection grid (idempotent check)
if 'GNIDA 5-in-1 Package' not in content:
    target_gnida_grid = """                                {(activeAuthority === 'GNIDA') && (
                                    <>
                                        <button
                                            onClick={() => setActiveTab('KYA')}"""
                                            
    rep_gnida_grid = """                                {(activeAuthority === 'GNIDA') && (
                                    <>
                                        <button
                                            onClick={() => setActiveTab('GNIDA_PACKAGE')}
                                            className={`group col-span-2 flex flex-row items-center gap-3 p-3 rounded-xl border text-left transition-all duration-200 cursor-pointer ${
                                                activeTab === 'GNIDA_PACKAGE'
                                                    ? 'bg-gradient-to-r from-indigo-500/10 to-blue-500/10 border-indigo-500 shadow-sm ring-1 ring-indigo-100 text-indigo-700'
                                                    : 'bg-white border-slate-100 text-slate-700 hover:border-indigo-100 hover:bg-indigo-50/30'
                                            }`}
                                        >
                                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
                                                activeTab === 'GNIDA_PACKAGE' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100/80'
                                            }`}>
                                                <i className="fa-solid fa-cubes text-sm"></i>
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="font-extrabold text-[12px] leading-tight flex items-center gap-1.5">
                                                    GNIDA 5-in-1 Package
                                                    <span className="px-1.5 py-0.5 bg-indigo-100 text-indigo-800 rounded font-black text-[8px] uppercase tracking-wider scale-90">Hot</span>
                                                </span>
                                                <span className="text-[10px] text-slate-400 font-normal leading-none mt-0.5">Fill all 5 documents in a single form</span>
                                            </div>
                                        </button>
                                        
                                        <button
                                            onClick={() => setActiveTab('KYA')}"""
    content = safe_replace(content, target_gnida_grid, rep_gnida_grid)

# 9. Inject the sidebar inputs form for GNIDA_PACKAGE (idempotent check)
if 'activeTab === \'GNIDA_PACKAGE\'' not in content:
    target_inputs_crm = """                            {activeTab === 'CRM' && ("""
    
    # We will build the entire inputs block with checkboxes and sections matching the project form style
    inputs_block = """                            {activeTab === 'GNIDA_PACKAGE' && (
                                <div className="space-y-6">
                                    {/* Document Selection Box */}
                                    <div className="bg-slate-50 border border-slate-200/60 p-4 rounded-xl space-y-3">
                                        <h3 className="font-extrabold text-slate-800 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
                                            <i className="fa-solid fa-cubes text-indigo-600"></i> Select Documents to Generate
                                        </h3>
                                        <div className="grid grid-cols-1 gap-2 text-xs font-bold text-slate-600">
                                            <label className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-lg cursor-pointer transition">
                                                <input type="checkbox" checked={gnidaPackageDocs.kya} onChange={(e) => setGnidaPackageDocs(prev => ({ ...prev, kya: e.target.checked }))} className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer" />
                                                <span>Know Your Allottee (KYA)</span>
                                            </label>
                                            <label className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-lg cursor-pointer transition">
                                                <input type="checkbox" checked={gnidaPackageDocs.tm} onChange={(e) => setGnidaPackageDocs(prev => ({ ...prev, tm: e.target.checked }))} className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer" />
                                                <span>Transfer Memo (TM) App</span>
                                            </label>
                                            <label className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-lg cursor-pointer transition">
                                                <input type="checkbox" checked={gnidaPackageDocs.mutation} onChange={(e) => setGnidaPackageDocs(prev => ({ ...prev, mutation: e.target.checked }))} className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer" />
                                                <span>Property Mutation Form</span>
                                            </label>
                                            <label className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-lg cursor-pointer transition">
                                                <input type="checkbox" checked={gnidaPackageDocs.registry} onChange={(e) => setGnidaPackageDocs(prev => ({ ...prev, registry: e.target.checked }))} className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer" />
                                                <span>Flat Registry Format</span>
                                            </label>
                                            <label className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-lg cursor-pointer transition">
                                                <input type="checkbox" checked={gnidaPackageDocs.ptm} onChange={(e) => setGnidaPackageDocs(prev => ({ ...prev, ptm: e.target.checked }))} className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer" />
                                                <span>Permission to Mortgage (PTM)</span>
                                            </label>
                                        </div>
                                    </div>

                                    {/* SECTION 1: Property & Authority Details */}
                                    <Section title="Property & Authority" icon="fa-building-columns" color="indigo" isOpen={true}>
                                        <Input label="Project Name" name="projectName" value={gnidaPackageData.projectName} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, projectName: e.target.value }))} />
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Flat No." name="flatNo" value={gnidaPackageData.flatNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, flatNo: e.target.value }))} />
                                            <Input label="Tower" name="towerName" value={gnidaPackageData.towerName} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, towerName: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Floor" name="floor" value={gnidaPackageData.floor} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, floor: e.target.value }))} />
                                            <Input label="Parking Slot" name="parking" value={gnidaPackageData.parking} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, parking: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Super Area (Sq.Ft)" name="superAreaSqFt" value={gnidaPackageData.superAreaSqFt} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, superAreaSqFt: e.target.value }))} />
                                            <Input label="Super Area (Sq.Mtr)" name="superAreaSqMtr" value={gnidaPackageData.superAreaSqMtr} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, superAreaSqMtr: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Plot No." name="plotNo" value={gnidaPackageData.plotNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, plotNo: e.target.value }))} />
                                            <Input label="Sector" name="sector" value={gnidaPackageData.sector} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, sector: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Block" name="block" value={gnidaPackageData.block} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, block: e.target.value }))} />
                                            <Input label="Allotment No." name="allotmentNo" value={gnidaPackageData.allotmentNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, allotmentNo: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Allotment Date" name="allotmentDate" value={gnidaPackageData.allotmentDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, allotmentDate: e.target.value }))} type="date" />
                                            <Input label="Plot Size" name="plotSize" value={gnidaPackageData.plotSize} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, plotSize: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Scheme Name" name="schemeName" value={gnidaPackageData.schemeName} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, schemeName: e.target.value }))} />
                                            <Input label="Scheme Code" name="schemeCode" value={gnidaPackageData.schemeCode} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, schemeCode: e.target.value }))} />
                                        </div>
                                    </Section>

                                    {/* SECTION 2: Seller Details */}
                                    <Section title="Seller (Transferor)" icon="fa-user-minus" color="rose" isOpen={false}>
                                        <div className="mb-4">
                                            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1.5">No. of Sellers</label>
                                            <div className="flex gap-2 bg-slate-100 p-1 rounded-xl">
                                                {['1', '2'].map(val => (
                                                    <button key={val} onClick={() => setGnidaPackageData(prev => ({ ...prev, transferorCount: val }))} className={`flex-1 text-center py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${gnidaPackageData.transferorCount === val ? 'bg-white text-rose-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}>{val}</button>
                                                ))}
                                            </div>
                                        </div>
                                        
                                        <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Seller 1</div>
                                            <Input label="Full Name" name="transferor1Name" value={gnidaPackageData.transferor1Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Name: e.target.value }))} />
                                            <Input label="Father/Husband" name="transferor1Parent" value={gnidaPackageData.transferor1Parent} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Parent: e.target.value }))} />
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="PAN" name="transferor1Pan" value={gnidaPackageData.transferor1Pan} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Pan: e.target.value }))} />
                                                <Input label="Aadhaar" name="transferor1Aadhar" value={gnidaPackageData.transferor1Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Aadhar: e.target.value }))} />
                                            </div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Age" name="transferor1Age" value={gnidaPackageData.transferor1Age} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Age: e.target.value }))} />
                                                <Input label="Phone" name="transferor1Phone" value={gnidaPackageData.transferor1Phone} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Phone: e.target.value }))} />
                                            </div>
                                            <Input label="Email" name="transferor1Email" value={gnidaPackageData.transferor1Email} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Email: e.target.value }))} />
                                            <Input label="Address" name="transferor1Address" value={gnidaPackageData.transferor1Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor1Address: e.target.value }))} />
                                        </div>

                                        {gnidaPackageData.transferorCount === '2' && (
                                            <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl mt-4">
                                                <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Seller 2</div>
                                                <Input label="Full Name" name="transferor2Name" value={gnidaPackageData.transferor2Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Name: e.target.value }))} />
                                                <Input label="Father/Husband" name="transferor2Parent" value={gnidaPackageData.transferor2Parent} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Parent: e.target.value }))} />
                                                <div className="grid grid-cols-2 gap-2">
                                                    <Input label="PAN" name="transferor2Pan" value={gnidaPackageData.transferor2Pan} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Pan: e.target.value }))} />
                                                    <Input label="Aadhaar" name="transferor2Aadhar" value={gnidaPackageData.transferor2Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Aadhar: e.target.value }))} />
                                                </div>
                                                <div className="grid grid-cols-2 gap-2">
                                                    <Input label="Age" name="transferor2Age" value={gnidaPackageData.transferor2Age} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Age: e.target.value }))} />
                                                    <Input label="Phone" name="transferor2Phone" value={gnidaPackageData.transferor2Phone} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Phone: e.target.value }))} />
                                                </div>
                                                <Input label="Email" name="transferor2Email" value={gnidaPackageData.transferor2Email} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Email: e.target.value }))} />
                                                <Input label="Address" name="transferor2Address" value={gnidaPackageData.transferor2Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferor2Address: e.target.value }))} />
                                            </div>
                                        )}
                                    </Section>

                                    {/* SECTION 3: Buyer Details */}
                                    <Section title="Buyer (Transferee)" icon="fa-user-plus" color="emerald" isOpen={false}>
                                        <div className="mb-4">
                                            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1.5">No. of Buyers</label>
                                            <div className="flex gap-2 bg-slate-100 p-1 rounded-xl">
                                                {['1', '2'].map(val => (
                                                    <button key={val} onClick={() => setGnidaPackageData(prev => ({ ...prev, transfereeCount: val }))} className={`flex-1 text-center py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${gnidaPackageData.transfereeCount === val ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}>{val}</button>
                                                ))}
                                            </div>
                                        </div>
                                        
                                        <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Buyer 1</div>
                                            <Input label="Full Name" name="transferee1Name" value={gnidaPackageData.transferee1Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Name: e.target.value }))} />
                                            <Input label="Father/Husband" name="transferee1Parent" value={gnidaPackageData.transferee1Parent} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Parent: e.target.value }))} />
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="PAN" name="transferee1Pan" value={gnidaPackageData.transferee1Pan} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Pan: e.target.value }))} />
                                                <Input label="Aadhaar" name="transferee1Aadhar" value={gnidaPackageData.transferee1Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Aadhar: e.target.value }))} />
                                            </div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Age" name="transferee1Age" value={gnidaPackageData.transferee1Age} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Age: e.target.value }))} />
                                                <Input label="Phone" name="transferee1Phone" value={gnidaPackageData.transferee1Phone} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Phone: e.target.value }))} />
                                            </div>
                                            <Input label="Email" name="transferee1Email" value={gnidaPackageData.transferee1Email} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Email: e.target.value }))} />
                                            <Input label="Address" name="transferee1Address" value={gnidaPackageData.transferee1Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee1Address: e.target.value }))} />
                                        </div>

                                        {gnidaPackageData.transfereeCount === '2' && (
                                            <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl mt-4">
                                                <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Buyer 2</div>
                                                <Input label="Full Name" name="transferee2Name" value={gnidaPackageData.transferee2Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Name: e.target.value }))} />
                                                <Input label="Father/Husband" name="transferee2Parent" value={gnidaPackageData.transferee2Parent} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Parent: e.target.value }))} />
                                                <div className="grid grid-cols-2 gap-2">
                                                    <Input label="PAN" name="transferee2Pan" value={gnidaPackageData.transferee2Pan} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Pan: e.target.value }))} />
                                                    <Input label="Aadhaar" name="transferee2Aadhar" value={gnidaPackageData.transferee2Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Aadhar: e.target.value }))} />
                                                </div>
                                                <div className="grid grid-cols-2 gap-2">
                                                    <Input label="Age" name="transferee2Age" value={gnidaPackageData.transferee2Age} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Age: e.target.value }))} />
                                                    <Input label="Phone" name="transferee2Phone" value={gnidaPackageData.transferee2Phone} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Phone: e.target.value }))} />
                                                </div>
                                                <Input label="Email" name="transferee2Email" value={gnidaPackageData.transferee2Email} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Email: e.target.value }))} />
                                                <Input label="Address" name="transferee2Address" value={gnidaPackageData.transferee2Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferee2Address: e.target.value }))} />
                                            </div>
                                        )}
                                    </Section>

                                    {/* SECTION 4: Financials & Registration Details */}
                                    <Section title="Financials & Registry" icon="fa-file-invoice-dollar" color="purple" isOpen={false}>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Sale Price (INR)" name="saleConsideration" value={gnidaPackageData.saleConsideration} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, saleConsideration: e.target.value }))} />
                                            <Input label="Stamp duty base" name="stampDutyPaidOn" value={gnidaPackageData.stampDutyPaidOn} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, stampDutyPaidOn: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Total Stamp Duty" name="totalStampDuty" value={gnidaPackageData.totalStampDuty} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, totalStampDuty: e.target.value }))} />
                                            <Input label="Circle Rate (Sq.M)" name="circleRate" value={gnidaPackageData.circleRate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, circleRate: e.target.value }))} />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Transfer Memo No." name="tmNo" value={gnidaPackageData.tmNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, tmNo: e.target.value }))} />
                                            <Input label="Transfer Memo Date" name="tmDate" value={gnidaPackageData.tmDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, tmDate: e.target.value }))} type="date" />
                                        </div>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Transfer Date" name="transferDate" value={gnidaPackageData.transferDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferDate: e.target.value }))} type="date" />
                                            <Input label="Lease Date" name="leaseDate" value={gnidaPackageData.leaseDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, leaseDate: e.target.value }))} type="date" />
                                        </div>
                                        <Input label="Sub-Lease Date" name="subLeaseDate" value={gnidaPackageData.subLeaseDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, subLeaseDate: e.target.value }))} type="date" />
                                        
                                        <div className="p-3 bg-slate-50/50 border border-slate-100 rounded-xl space-y-3 mt-4">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider"><i className="fa-solid fa-stamp mr-1"></i> Mutation Specifics</div>
                                            <Input label="Sub Registrar Office" name="subRegistrar" value={gnidaPackageData.subRegistrar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, subRegistrar: e.target.value }))} />
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Jild No." name="jildNo" value={gnidaPackageData.jildNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, jildNo: e.target.value }))} />
                                                <Input label="Reg Serial No." name="regSerialNo" value={gnidaPackageData.regSerialNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, regSerialNo: e.target.value }))} />
                                            </div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Page From" name="regPageFrom" value={gnidaPackageData.regPageFrom} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, regPageFrom: e.target.value }))} />
                                                <Input label="Page To" name="regPageTo" value={gnidaPackageData.regPageTo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, regPageTo: e.target.value }))} />
                                            </div>
                                            <Input label="Registration Date" name="regDate" value={gnidaPackageData.regDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, regDate: e.target.value }))} type="date" />
                                        </div>
                                        
                                        <div className="p-3 bg-slate-50/50 border border-slate-100 rounded-xl space-y-3 mt-4">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider"><i className="fa-solid fa-file-shield mr-1"></i> Mortgage Specifics</div>
                                            <Input label="Mortgaging Bank" name="mortgagingAgencyName" value={gnidaPackageData.mortgagingAgencyName} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, mortgagingAgencyName: e.target.value }))} />
                                            <Input label="Bank Address" name="mortgagingAgencyAddress" value={gnidaPackageData.mortgagingAgencyAddress} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, mortgagingAgencyAddress: e.target.value }))} />
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Bank Pin Code" name="ptmPinCode" value={gnidaPackageData.ptmPinCode} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, ptmPinCode: e.target.value }))} />
                                                <Input label="PTM Ack No." name="ptmAcknowledgementNo" value={gnidaPackageData.ptmAcknowledgementNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, ptmAcknowledgementNo: e.target.value }))} />
                                            </div>
                                            <Input label="PTM Receiving Date" name="ptmReceivingDate" value={gnidaPackageData.ptmReceivingDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, ptmReceivingDate: e.target.value }))} type="date" />
                                        </div>

                                        <div className="p-3 bg-slate-50/50 border border-slate-100 rounded-xl space-y-3 mt-4">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider"><i className="fa-solid fa-right-left mr-1"></i> Transfer Memo Specifics</div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Form Serial No." name="formSlNo" value={gnidaPackageData.formSlNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, formSlNo: e.target.value }))} />
                                                <Input label="Date of Issue" name="dateOfIssue" value={gnidaPackageData.dateOfIssue} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, dateOfIssue: e.target.value }))} type="date" />
                                            </div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Processing Fee DD" name="processingFeeDraftNo" value={gnidaPackageData.processingFeeDraftNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, processingFeeDraftNo: e.target.value }))} />
                                                <Input label="Fee DD Date" name="processingFeeDate" value={gnidaPackageData.processingFeeDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, processingFeeDate: e.target.value }))} type="date" />
                                            </div>
                                            <Input label="Fee DD Bank" name="processingFeeBank" value={gnidaPackageData.processingFeeBank} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, processingFeeBank: e.target.value }))} />
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Transfer Charge DD" name="transferChargeDraftNo" value={gnidaPackageData.transferChargeDraftNo} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferChargeDraftNo: e.target.value }))} />
                                                <Input label="Charge DD Date" name="transferChargeDate" value={gnidaPackageData.transferChargeDate} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferChargeDate: e.target.value }))} type="date" />
                                            </div>
                                            <div className="grid grid-cols-2 gap-2">
                                                <Input label="Charge DD Bank" name="transferChargeBank" value={gnidaPackageData.transferChargeBank} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferChargeBank: e.target.value }))} />
                                                <Input label="Charge Amount" name="transferChargeAmount" value={gnidaPackageData.transferChargeAmount} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, transferChargeAmount: e.target.value }))} />
                                            </div>
                                        </div>
                                    </Section>

                                    {/* SECTION 5: Witnesses & Dates Details */}
                                    <Section title="Witnesses & Sign Dates" icon="fa-signature" color="orange" isOpen={false}>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Input label="Place of Execution" name="place" value={gnidaPackageData.place} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, place: e.target.value }))} />
                                            <Input label="Execution Date" name="dated" value={gnidaPackageData.dated} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, dated: e.target.value }))} type="date" />
                                        </div>
                                        
                                        <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl mt-4">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Witness 1</div>
                                            <Input label="Full Name" name="witness1Name" value={gnidaPackageData.witness1Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness1Name: e.target.value }))} />
                                            <Input label="Father's Name" name="witness1Father" value={gnidaPackageData.witness1Father} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness1Father: e.target.value }))} />
                                            <Input label="Aadhaar No." name="witness1Aadhar" value={gnidaPackageData.witness1Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness1Aadhar: e.target.value }))} />
                                            <Input label="Address" name="witness1Address" value={gnidaPackageData.witness1Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness1Address: e.target.value }))} />
                                        </div>

                                        <div className="space-y-3 p-3 bg-slate-50/50 border border-slate-100 rounded-xl mt-4">
                                            <div className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">Witness 2</div>
                                            <Input label="Full Name" name="witness2Name" value={gnidaPackageData.witness2Name} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness2Name: e.target.value }))} />
                                            <Input label="Father's Name" name="witness2Father" value={gnidaPackageData.witness2Father} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness2Father: e.target.value }))} />
                                            <Input label="Aadhaar No." name="witness2Aadhar" value={gnidaPackageData.witness2Aadhar} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness2Aadhar: e.target.value }))} />
                                            <Input label="Address" name="witness2Address" value={gnidaPackageData.witness2Address} onChange={(e) => setGnidaPackageData(prev => ({ ...prev, witness2Address: e.target.value }))} />
                                        </div>
                                    </Section>
                                </div>
                            )}
                            {activeTab === 'CRM' && ("""
    content = safe_replace(content, target_inputs_crm, rep_inputs_crm)

# 10. Update Right Preview Area for the 5 GNIDA document layout blocks to enable rendering under activeTab === 'GNIDA_PACKAGE'
# Document 1: GNIDA Flat Registry deed (idempotent check)
if '\'GNIDA_REGISTRY\' || (activeTab === \'GNIDA_PACKAGE\' && gnidaPackageDocs.registry)' not in content:
    target_registry_preview = """                            {activeTab === 'GNIDA_REGISTRY' && (
                                <>
                                    {/* PAGE 1: Data Sheet */}"""
    rep_registry_preview = """                            {(activeTab === 'GNIDA_REGISTRY' || (activeTab === 'GNIDA_PACKAGE' && gnidaPackageDocs.registry)) && (
                                <>
                                    {activeTab === 'GNIDA_PACKAGE' && (
                                        <div className="w-full max-w-4xl bg-indigo-50 border border-indigo-100 rounded-2xl p-4 text-center text-xs font-bold text-indigo-700 select-none print:hidden mb-4 mt-8 flex items-center justify-between">
                                            <span className="flex items-center gap-1.5"><i className="fa-solid fa-file-signature text-base text-indigo-600"></i> DOCUMENT 1: Flat Sub-Lease Transfer Registry Deed</span>
                                            <span className="px-2.5 py-0.5 bg-indigo-100 text-indigo-800 rounded font-black text-[9px] uppercase tracking-wider">Registry Deed</span>
                                        </div>
                                    )}
                                    {/* PAGE 1: Data Sheet */}"""
    content = safe_replace(content, target_registry_preview, rep_registry_preview)

# Document 2: GNIDA PTM (Permission to Mortgage) (idempotent check)
if '\'GNIDA_PTM\' || (activeTab === \'GNIDA_PACKAGE\' && gnidaPackageDocs.ptm)' not in content:
    target_ptm_preview = """                                    {activeTab === 'GNIDA_PTM' && (
                                        <div className="paper-page bg-white p-8 relative flex flex-col items-center">"""
    rep_ptm_preview = """                                    {(activeTab === 'GNIDA_PTM' || (activeTab === 'GNIDA_PACKAGE' && gnidaPackageDocs.ptm)) && (
                                        <>
                                            {activeTab === 'GNIDA_PACKAGE' && (
                                                <div className="w-full max-w-4xl bg-teal-50 border border-teal-100 rounded-2xl p-4 text-center text-xs font-bold text-teal-700 select-none print:hidden mb-4 mt-8 flex items-center justify-between">
                                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-file-shield text-base text-teal-600"></i> DOCUMENT 2: Permission to Mortgage (PTM) Application</span>
                                                    <span className="px-2.5 py-0.5 bg-teal-100 text-teal-800 rounded font-black text-[9px] uppercase tracking-wider">PTM Application</span>
                                                </div>
                                            )}
                                            <div className="paper-page bg-white p-8 relative flex flex-col items-center">"""
    content = safe_replace(content, target_ptm_preview, rep_ptm_preview)
    
    # We must also close the newly added fragment tag wrapper for PTM inside the package (idempotent check)
    target_ptm_close = """                                            </div>
                                        </div>
                                    )}

                                    {activeTab === 'RENT' && ("""
    rep_ptm_close = """                                            </div>
                                        </div>
                                        </>
                                    )}

                                    {activeTab === 'RENT' && ("""
    content = safe_replace(content, target_ptm_close, rep_ptm_close)

# Document 3: GNIDA KYA (Know Your Allottee) (idempotent check)
if '\'GNIDA\' || (activeTab === \'GNIDA_PACKAGE\' && gnidaPackageDocs.kya)' not in content:
    target_kya_preview = """                                    {activeTab === 'GNIDA' && (
                                        <>
                                            {/* --- PAGE 1 --- */}"""
    rep_kya_preview = """                                    {(activeTab === 'GNIDA' || (activeTab === 'GNIDA_PACKAGE' && gnidaPackageDocs.kya)) && (
                                        <>
                                            {activeTab === 'GNIDA_PACKAGE' && (
                                                <div className="w-full max-w-4xl bg-yellow-50 border border-yellow-100 rounded-2xl p-4 text-center text-xs font-bold text-yellow-700 select-none print:hidden mb-4 mt-8 flex items-center justify-between">
                                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-id-card text-base text-yellow-600"></i> DOCUMENT 3: Know Your Allottee (KYA) Verification datasheet</span>
                                                    <span className="px-2.5 py-0.5 bg-yellow-100 text-yellow-800 rounded font-black text-[9px] uppercase tracking-wider">KYA Form</span>
                                                </div>
                                            )}
                                            {/* --- PAGE 1 --- */}"""
    content = safe_replace(content, target_kya_preview, rep_kya_preview)

# Document 4: Property Mutation Form (idempotent check)
if '\'MUTATION\' || (activeTab === \'GNIDA_PACKAGE\' && gnidaPackageDocs.mutation)' not in content:
    target_mutation_preview = """                                    {activeTab === 'MUTATION' && (
                                        <div className="paper-page print-break text-justify text-gray-900 font-serif relative p-16 text-[12pt] leading-1.5">"""
    rep_mutation_preview = """                                    {(activeTab === 'MUTATION' || (activeTab === 'GNIDA_PACKAGE' && gnidaPackageDocs.mutation)) && (
                                        <>
                                            {activeTab === 'GNIDA_PACKAGE' && (
                                                <div className="w-full max-w-4xl bg-emerald-50 border border-emerald-100 rounded-2xl p-4 text-center text-xs font-bold text-emerald-700 select-none print:hidden mb-4 mt-8 flex items-center justify-between">
                                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-file-pen text-base text-emerald-600"></i> DOCUMENT 4: Property Title Mutation Application</span>
                                                    <span className="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded font-black text-[9px] uppercase tracking-wider">Mutation Form</span>
                                                </div>
                                            )}
                                            <div className="paper-page print-break text-justify text-gray-900 font-serif relative p-16 text-[12pt] leading-1.5">"""
    content = safe_replace(content, target_mutation_preview, rep_mutation_preview)

    # We must also close the newly added fragment tag wrapper for Mutation inside the package (idempotent check)
    target_mutation_close = """                                            </div>
                                        </div>
                                    )}

                                    {activeTab === 'TM_APP' && ("""
    rep_mutation_close = """                                            </div>
                                        </div>
                                        </>
                                    )}

                                    {activeTab === 'TM_APP' && ("""
    content = safe_replace(content, target_mutation_close, rep_mutation_close)

# Document 5: Transfer Memo (TM_APP) (idempotent check)
if '\'TM_APP\' || (activeTab === \'GNIDA_PACKAGE\' && gnidaPackageDocs.tm)' not in content:
    target_tm_preview = """                                    {activeTab === 'TM_APP' && (
                                        <>
                                            <div className="paper-page print-break text-gray-900 font-serif relative p-10 text-[10.5pt] leading-relaxed">"""
    rep_tm_preview = """                                    {(activeTab === 'TM_APP' || (activeTab === 'GNIDA_PACKAGE' && gnidaPackageDocs.tm)) && (
                                        <>
                                            {activeTab === 'GNIDA_PACKAGE' && (
                                                <div className="w-full max-w-4xl bg-rose-50 border border-rose-100 rounded-2xl p-4 text-center text-xs font-bold text-rose-700 select-none print:hidden mb-4 mt-8 flex items-center justify-between">
                                                    <span className="flex items-center gap-1.5"><i className="fa-solid fa-right-left text-base text-rose-600"></i> DOCUMENT 5: Transfer Memo (TM) Application Form</span>
                                                    <span className="px-2.5 py-0.5 bg-rose-100 text-rose-800 rounded font-black text-[9px] uppercase tracking-wider">Transfer Memo</span>
                                                </div>
                                            )}
                                            <div className="paper-page print-break text-gray-900 font-serif relative p-10 text-[10.5pt] leading-relaxed">"""
    content = safe_replace(content, target_tm_preview, rep_tm_preview)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Composite modifier script created.")
