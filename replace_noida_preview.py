#!/usr/bin/env python3
"""
Replace the NOIDA Transfer preview section (lines 6172-6921) in test_script.jsx
with a government-PDF-accurate version.
"""

NEW_JSX = r'''                                    {activeTab === 'NOIDA_TRANSFER' && (() => {
                                        const p = noidaTransferData;

                                        // Helpers to format names
                                        const getTransferorText = () => {
                                            const t1 = `${p.transferor1Name || p.allotteeName || '__________________' } ${p.transferor1Relation || 'S/o'} ${p.transferor1Father || p.allotteeFather || '__________________'} R/o ${p.transferor1Address || p.allotteeAddress || '__________________'}`;
                                            if (p.hasJointTransferor && p.transferor2Name) {
                                                const t2 = `${p.transferor2Name} ${p.transferor2Relation || 'S/o'} ${p.transferor2Father || '__________________'} R/o ${p.transferor2Address || '__________________'}`;
                                                return `${t1} AND ${t2}`;
                                            }
                                            return t1;
                                        };

                                        const getTransfereeText = () => {
                                            const tr1 = `${p.transferee1Name || p.transfereeName || '__________________'} ${p.transferee1Relation || 'S/o'} ${p.transferee1Father || p.transfereeFather || '__________________'} R/o ${p.transferee1Address || p.transfereeAddress || '__________________'}`;
                                            let res = tr1;
                                            if (parseInt(p.transfereeCount) >= 2 && p.transferee2Name) {
                                                const tr2 = `${p.transferee2Name} ${p.transferee2Relation || 'S/o'} ${p.transferee2Father || '__________________'} R/o ${p.transferee2Address || '__________________'}`;
                                                res += ` AND ${tr2}`;
                                            }
                                            if (parseInt(p.transfereeCount) >= 3 && p.transferee3Name) {
                                                const tr3 = `${p.transferee3Name} ${p.transferee3Relation || 'S/o'} ${p.transferee3Father || '__________________'} R/o ${p.transferee3Address || '__________________'}`;
                                                res += ` AND ${tr3}`;
                                            }
                                            return res;
                                        };

                                        const getTransferorNamesOnly = () => {
                                            const t1 = p.transferor1Name || p.allotteeName || '__________________';
                                            if (p.hasJointTransferor && p.transferor2Name) {
                                                return `${t1} & ${p.transferor2Name}`;
                                            }
                                            return t1;
                                        };

                                        const getTransfereeNamesOnly = () => {
                                            const tr1 = p.transferee1Name || p.transfereeName || '__________________';
                                            let res = tr1;
                                            if (parseInt(p.transfereeCount) >= 2 && p.transferee2Name) {
                                                res += ` & ${p.transferee2Name}`;
                                            }
                                            if (parseInt(p.transfereeCount) >= 3 && p.transferee3Name) {
                                                res += ` & ${p.transferee3Name}`;
                                            }
                                            return res;
                                        };

                                        const formatDate = (dStr) => {
                                            if (!dStr) return '__________';
                                            try {
                                                return new Date(dStr).toLocaleDateString('en-GB');
                                            } catch (e) {
                                                return dStr;
                                            }
                                        };

                                        return (
                                            <>
                                                {/* ============ PAGE 1: Main Application Form ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <EsignBadge type="NOIDA_TRANSFER" />

                                                    <div className="text-center font-bold text-[14pt] uppercase mb-1">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>
                                                    <div className="text-center font-bold text-[12pt] uppercase underline mb-1">TRANSFER APPLICATION FORM (valid for six months)</div>
                                                    <div className="text-center text-[8pt] uppercase mb-4 leading-tight">
                                                        FOR TRANSFER OF RESIDENTIAL PLOTS/GROUP HOUSING (flats and houses allotted by AWHO, AFNHB, Builders, Co-operative Societies) /HOUSING (Flats/Houses allotted by NOIDA)/ INDUSTRIAL PLOTS &amp; SHEDS/COMMERCIAL SHOPS &amp; PLOTS/ INSTITUTIONAL PLOTS
                                                    </div>

                                                    <div className="flex justify-between text-[9pt] mb-1">
                                                        <div>Price Rs. 100/- (Rupees One Hundred Only)</div>
                                                        <div>Sl.No. <Var name="slNo"><span className="border-b border-dotted border-black inline-block min-w-[120px]">{p.slNo || ''}</span></Var></div>
                                                    </div>
                                                    <div className="text-[9pt] mb-0.5">Date of issue by the authorized bank <Var name="issueDate"><span className="border-b border-dotted border-black inline-block min-w-[120px]">{formatDate(p.issueDate) !== '__________' ? formatDate(p.issueDate) : ''}</span></Var></div>
                                                    <div className="text-[9pt] mb-4 pl-8">For downloaded forms date of deposit of Rs. 100/- in the authorized bank <Var name="downloadDepositDate"><span className="border-b border-dotted border-black inline-block min-w-[120px]">{formatDate(p.downloadDepositDate) !== '__________' ? formatDate(p.downloadDepositDate) : ''}</span></Var></div>

                                                    <div className="text-[9pt] mb-4">
                                                        <div>ASSTT. GENERAL MANAGER/Dy. GENERAL MANAGER/GENERAL MANAGER,</div>
                                                        <div>NOIDA.</div>
                                                    </div>

                                                    <p className="text-justify text-[9pt] leading-relaxed mb-3">
                                                        I/ We/ M/s (allottee) <Var name="transferor1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Name || p.allotteeName || ''}</span></Var>
                                                        {p.hasJointTransferor && p.transferor2Name && <> and <Var name="transferor2Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferor2Name}</span></Var></>}
                                                        {' '}(Prop.,Partner or name of the firm)
                                                        {' '}<Var name="transferor1Relation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.transferor1Relation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="transferor1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Father || p.allotteeFather || ''}</span></Var>
                                                        {' '}R/o, Regd. Office <Var name="transferor1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferor1Address || p.allotteeAddress || ''}</span></Var>
                                                        {' '}is an allottee (here in shall be referred to as Transferor) of Plot/Flat or House on Group Housing Plot/Housing (Flat/ House/allotted by NOIDA)/ Industrial Plots &amp; Sheds/Commercial Shop &amp; Plots/Institutional Plot/ Premises No.
                                                        {' '}<Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[60px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[60px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[60px] font-bold">{p.sector || ''}</span></Var> NOIDA having an area of
                                                        {' '}<Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[60px] font-bold">{p.area || ''}</span></Var> Sq. Mtrs. want to transfer the above plot/premises in favour of Shri/Smt./M/s
                                                        {' '}<Var name="transferee1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Name || p.transfereeName || ''}</span></Var>
                                                        {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and <Var name="transferee2Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee2Name}</span></Var></>}
                                                        {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and <Var name="transferee3Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee3Name}</span></Var></>}
                                                        {' '}<Var name="transferee1Relation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.transferee1Relation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="transferee1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Father || p.transfereeFather || ''}</span></Var>
                                                        {' '}R/o, Regd Office <Var name="transferee1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferee1Address || p.transfereeAddress || ''}</span></Var>
                                                        {' '}(herein after shall be referred to as transferee).
                                                    </p>

                                                    {/* GPA paragraph */}
                                                    {p.isGpa ? (
                                                        <p className="text-justify text-[9pt] leading-relaxed mb-3">
                                                            In case of transfer on the basis of authenticated GPA dt. <Var name="gpaDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaDate) !== '__________' ? formatDate(p.gpaDate) : ''}</span></Var> through GPA of Holder Shri/Smt <Var name="gpaHolderName"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderName || ''}</span></Var>
                                                            {' '}<Var name="gpaHolderRelation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.gpaHolderRelation || 'S/o'}</span></Var>,W/o,D/o Shri <Var name="gpaHolderFather"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderFather || ''}</span></Var>
                                                            {' '}Address <Var name="gpaHolderAddress"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.gpaHolderAddress || ''}</span></Var>
                                                        </p>
                                                    ) : (
                                                        <p className="text-[9pt] leading-relaxed mb-3 text-gray-400 line-through select-none">
                                                            In case of transfer on the basis of authenticated GPA dt.__________________ through GPA of Holder Shri/Smt___________________ S/o,W/o,D/o Shri __________________________________ Address____________________________________
                                                        </p>
                                                    )}

                                                    <p className="text-justify text-[9pt] leading-relaxed mb-4">
                                                        The transferor(s) and the transferee(s) have read and understood the terms and conditions for transfer and undertake to abide by the same and accordingly apply for transfer of the above said <Var name="useType"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{p.useType || ''}</span></Var> plot/premises in case of Industrial the premises will be used for <Var name="projectName"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.projectName || ''}</span></Var> Project which is at Sl No <Var name="slNo"><span className="border-b border-dotted border-black inline-block min-w-[40px]">{p.slNo || ''}</span></Var> of Annexure-A enclosed with Transfer Application from and for, Commercial/Institutional the premises will be used for as per terms of the original lease (Change of Project is not allowed).
                                                    </p>

                                                    {/* Signatures */}
                                                    <div className="flex justify-between text-center text-[9pt] mb-3">
                                                        <div className="w-48">
                                                            <div className="h-10"></div>
                                                            <div className="border-t border-black pt-1">Signature of the transferor(s)</div>
                                                            <div className="text-[8pt] italic">Above Signatures are attested</div>
                                                        </div>
                                                        <div className="w-48">
                                                            <div className="h-10"></div>
                                                            <div className="border-t border-black pt-1">Signature of transferee(s)</div>
                                                            <div className="text-[8pt] italic">Above signatures are attested</div>
                                                        </div>
                                                    </div>

                                                    {/* Bank Officer Attestation - 2x2 grid */}
                                                    <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-[8pt] mb-3">
                                                        <div className="border border-black p-2 min-h-[60px]">
                                                            <div>Signature, Name Designation</div>
                                                            <div>and seal of Bank Officer attesting</div>
                                                            <div>the signature</div>
                                                        </div>
                                                        <div className="border border-black p-2 min-h-[60px]">
                                                            <div>Signature, Name Designation</div>
                                                            <div>and seal of Bank Officer attesting the signature</div>
                                                        </div>
                                                        <div className="border border-black p-2 min-h-[60px]">
                                                            <div>Signature, Name Designation</div>
                                                            <div>and seal of Bank Officer attesting</div>
                                                            <div>the signature</div>
                                                        </div>
                                                        <div className="border border-black p-2 min-h-[60px]">
                                                            <div>Signature, Name Designation</div>
                                                            <div>and seal of Bank Officer attesting the signature</div>
                                                        </div>
                                                    </div>

                                                    {/* Photograph boxes */}
                                                    <div className="flex justify-center gap-6">
                                                        <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase leading-tight">
                                                            PHOTOGRAPH<br/>OF<br/>TRANSFEROR(S)<br/>DULY<br/>ATTESTED BY<br/>THE BANKER
                                                        </div>
                                                        {p.isGpa && (
                                                            <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase leading-tight">
                                                                PHOTOGRAPH<br/>OF<br/>GPA HOLDER<br/>DULY<br/>ATTESTED BY<br/>THE BANKER
                                                            </div>
                                                        )}
                                                        <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase leading-tight">
                                                            PHOTOGRAPH<br/>OF<br/>TRANSFEREE(S)<br/>DULY ATTESTED<br/>BY THE BANKER
                                                        </div>
                                                    </div>

                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">1</div>
                                                </div>

                                                {/* ============ PAGE 2: Notes & Transfer Rates ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[9pt]">
                                                        <div className="font-bold mb-2">Note :</div>
                                                        <div className="space-y-1.5 text-justify text-[8.5pt]">
                                                            <div><strong>(I)</strong> The term allottee includes transferee/sub lessee.</div>
                                                            <div><strong>(II)</strong> Signatures and Photograph of the Power of Attorney holder shall be required to be attested by the bankers, if the transfer application is submitted through General Power of Attorney Holder of the Allottee.</div>
                                                            <div><strong>(III)</strong> Group Housing means flats and houses allotted by AWHO, AFNHB, Builders and Co-operative Societies. Transfer of such flats/houses shall be considered alongwith transfer of garage, if it was allotted by the respective institution alongwith the flat/house.</div>
                                                            <div><strong>(IV)</strong> Transfer permission in favour of HUF shall not be allowed.</div>
                                                            <div><strong>(V)</strong> In case of industrial plot/premises transfer shall be permitted only after the unit has been declared functional.</div>
                                                            <div><strong>(VI)</strong> In case of industrial plot/premises project free from pollution &amp; environment hazards shall be considered. The project should not be on the banned list of directorate of Industries, UP or Development Commissioner, Small Scale Industries and Noida. A list of projects permitted in Noida is given as &apos;A&apos;, list of restricted projects is given as &apos;B&apos; and the list of negative projects is given as &apos;C&apos; on website of the Authority.</div>
                                                            <div><strong>(VII)</strong> The transfer charges for transfer Residential plot/flats/houses amongst the prescribed categories shall be 50% of the applicable transfer charges.</div>
                                                            <div><strong>(VIII)</strong> The transfer charges for transfer of industrial plots/sheds shall be 50% of the applicable transfer charges in cases of transfer/sale of the premises by financial institution under section 29 of SFC Act. The application has to be moved by the financial institution alongwith all NOC&apos;s required for making the transfer application.</div>
                                                        </div>

                                                        <div className="font-bold mt-3 mb-1"><strong>(IX)</strong> Prevailing Transfer charges</div>

                                                        {/* Two-column layout like the PDF */}
                                                        <div className="flex gap-2 text-[7.5pt]">
                                                            {/* Left column: rates table */}
                                                            <div className="flex-1">
                                                                <div className="font-bold mb-1 text-[8pt]">For transfer application moved by the allottee amount in Rs. Per sq.mtr. as mentioned below:-</div>
                                                                <div className="font-bold mb-1 text-[8pt]">i. RESIDENTIAL PLOTS</div>
                                                                <table className="w-full border-collapse border border-black text-[7pt]">
                                                                    <thead>
                                                                        <tr>
                                                                            <th className="border border-black p-0.5 text-left">SECTOR</th>
                                                                            <th className="border border-black p-0.5 text-right">RATE PER SQ MTR</th>
                                                                        </tr>
                                                                    </thead>
                                                                    <tbody>
                                                                        <tr><td className="border border-black p-0.5">14A, 15A</td><td className="border border-black p-0.5 text-right">4375.00</td></tr>
                                                                        <tr><td className="border border-black p-0.5">14, 17, 19, 30, 35, 47, 93</td><td className="border border-black p-0.5 text-right">2323.75</td></tr>
                                                                        <tr><td className="border border-black p-0.5">11, 12, 15, 20, 21, 22, 23, 25 TO 29, 31, 33, 34, 40, 41, 46, 48, 53, 55, 56, 70, 82, 96 TO 100, 122</td><td className="border border-black p-0.5 text-right">1619.75</td></tr>
                                                                        <tr><td className="border border-black p-0.5">42, 43, 45, 63A, 104, 107, 110, 118, 119, 120, 121, 128, 129, 130, 131, 133, 134, 135, 143, 151</td><td className="border border-black p-0.5 text-right">1179.50</td></tr>
                                                                        <tr><td className="border border-black p-0.5">86, 112, 113, 116, 117</td><td className="border border-black p-0.5 text-right">986.00</td></tr>
                                                                        <tr><td className="border border-black p-0.5">102, 115, 158, 162, ETC</td><td className="border border-black p-0.5 text-right">905.00</td></tr>
                                                                        <tr><td className="border border-black p-0.5">44 (A &amp; B BLOCK)</td><td className="border border-black p-0.5 text-right">4703.13</td></tr>
                                                                        <tr><td className="border border-black p-0.5">44 (OTHER A&amp;B), 93A, 93B</td><td className="border border-black p-0.5 text-right">2498.03</td></tr>
                                                                        <tr><td className="border border-black p-0.5">105, 108</td><td className="border border-black p-0.5 text-right">1741.23</td></tr>
                                                                        <tr><td className="border border-black p-0.5">128, 129, 143B, 154, 168</td><td className="border border-black p-0.5 text-right">1267.96</td></tr>
                                                                        <tr><td className="border border-black p-0.5">144</td><td className="border border-black p-0.5 text-right">1326.94</td></tr>
                                                                        <tr><td className="border border-black p-0.5">36, 39, 50, 51, 52</td><td className="border border-black p-0.5 text-right">2439.94</td></tr>
                                                                        <tr><td className="border border-black p-0.5">27, 34, 49, 61, 62, 63, 66, 71, 72, 92</td><td className="border border-black p-0.5 text-right">1700.74</td></tr>
                                                                        <tr><td className="border border-black p-0.5">137, 143B, 168</td><td className="border border-black p-0.5 text-right">1238.48</td></tr>
                                                                        <tr><td className="border border-black p-0.5">145</td><td className="border border-black p-0.5 text-right">1018.13</td></tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>

                                                            {/* Right column: GPA transfer rules */}
                                                            <div className="w-[45%] text-[7.5pt]">
                                                                <div className="font-bold mb-1 text-[8pt]">For transfer application moved by the Regd. GPA of the allottee</div>
                                                                <p className="text-justify leading-snug">
                                                                    Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.
                                                                </p>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">2</div>
                                                </div>

                                                {/* ============ PAGE 3: Rate table continued + GPA rules (GPA Conditional) ============ */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none pt-40">
                                                            <div className="text-gray-400 text-[10pt] font-bold">Page 3: GPA Transfer Rate Rules</div>
                                                            <p className="text-[9pt] text-gray-400">This page contains GPA-based transfer charge rules. It is hidden from print because GPA is not applicable.</p>
                                                            <div className="text-[8pt] text-gray-500 border border-gray-300 px-3 py-1 inline-block">Page 3 - Omitted from Print (GPA not active)</div>
                                                        </div>
                                                    ) : (
                                                        <div className="text-[8pt]">
                                                            {/* Two-column layout continuation */}
                                                            <div className="flex gap-2 text-[7.5pt]">
                                                                <div className="flex-1">
                                                                    {/* Continued from page 2 */}
                                                                    <div className="font-bold mb-1 text-[8pt]">ii. GROUP HOUSING</div>
                                                                    <p className="text-justify leading-snug mb-2">Transfer charges as applicable per the scheme/allotment terms.</p>

                                                                    <div className="font-bold mb-1 text-[8pt]">iii. HOUSING</div>
                                                                    <p className="text-justify leading-snug mb-2">Transfer charges as applicable per the scheme/allotment terms.</p>

                                                                    <div className="font-bold mb-1 text-[8pt]">iv. INDUSTRIAL PLOTS/ SHEDS</div>
                                                                    <p className="text-justify leading-snug mb-2">Transfer charges as applicable per the scheme/allotment terms.</p>

                                                                    <div className="font-bold mb-1 text-[8pt]">v. COMMERCIAL SHOPS/ PLOTS</div>
                                                                    <p className="text-justify leading-snug mb-2">Commercial properties are allowed to be transferred on power of attorney basis with the following conditions:-</p>
                                                                </div>
                                                                <div className="w-[45%] text-[7.5pt] space-y-2">
                                                                    <p className="text-justify leading-snug">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</p>
                                                                    <p className="text-justify leading-snug">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</p>
                                                                    <p className="text-justify leading-snug">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">3</div>
                                                </div>

                                                {/* ============ PAGE 4: Commercial GPA Rules (GPA Conditional) ============ */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none pt-40">
                                                            <div className="text-gray-400 text-[10pt] font-bold">Page 4: Commercial GPA Conditions</div>
                                                            <p className="text-[9pt] text-gray-400">This page details GPA conditions for Commercial property transfers. It is hidden from print because GPA is not applicable.</p>
                                                            <div className="text-[8pt] text-gray-500 border border-gray-300 px-3 py-1 inline-block">Page 4 - Omitted from Print (GPA not active)</div>
                                                        </div>
                                                    ) : (
                                                        <div className="text-[8pt] text-justify">
                                                            <div className="flex gap-2 text-[7.5pt]">
                                                                <div className="flex-1 space-y-2">
                                                                    <p className="leading-snug">Transfer application received on the basis of certified copy of Registered power of attorney only shall be entertained.</p>
                                                                    <p className="leading-snug">It shall be the sole responsibility of intending transferee to ensure authenticity and validity of such power of attorney.</p>
                                                                    <p className="leading-snug">The power of attorney holder shall be required to submit affidavit on the prescribed performa in support of authenticity and validity of power attorney. The intending purchaser shall also submit and indemnity bond on prescribed performa in support thereof.</p>
                                                                    <p className="leading-snug">In addition original allotment letter/possession certificate/legal documents i.e. licence agreement/HPTA/lease deed/transfer deed for the property under transfer, shall also be required alongwith the transfer application.</p>
                                                                    <p className="leading-snug">These documents shall be returned to transferee alongwith permission for transfer, if granted, under registered post or in person.</p>
                                                                    <p className="leading-snug">Certified copy of an agreement to sell duly registered or notarised shall also be required in favour of intending transferee. Transfer charges shall be one and half times(1.50) of the normal transfer charges for first agreement to sell. Thereafter Transfer charges shall be increased @ 50% of the normal transfer charges for every subsequent agreement to sell.</p>
                                                                    <p className="leading-snug">On grant of transfer permission transferee shall be required to execute lease deed/transfer deed as the case may be.</p>
                                                                    <p className="leading-snug">Transfer on power of attorney basis will be subject to directions received from Govt. of U.P from time to time. In case of general power of attorney is registered without agreement to sell, then a public notice in two national dailies (one in Hindi and one in English) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/ Transferee.</p>
                                                                </div>
                                                                <div className="w-[45%] text-[7.5pt]">
                                                                    <div className="font-bold mb-1 text-[8pt]">vi. INSTITUTIONAL</div>
                                                                    <p className="text-justify leading-snug">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</p>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">4</div>
                                                </div>

                                                {/* ============ PAGE 5: Institutional + Requirements/Enclosures ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[8.5pt] text-justify">
                                                        <div className="font-bold mb-3 text-[9pt]">Requirements/Enclosures for transfer of plot/premises on request of the allottee</div>

                                                        <div className="space-y-1.5">
                                                            <div>(1) Payment deposit challan (in original) for deposit of processing fees of Rs. 1000/- and transfer charges &apos;as applicable&apos; in one of the authorised banks.</div>
                                                            <div>(2) Joint affidavit by the transferor and transferee in the prescribed format on non-judicial stamp paper of Rs. 20/- duly notarised.</div>
                                                            <div>(3) Affidavit by the transferee in the prescribed format about his satisfaction towards non encumbrance on the plot/premises.</div>
                                                            <div>(4) No dues Certificate issued by the concerned Account Officer.</div>
                                                            <div>(5) No dues certificate issued by the Project Engineer (Jal).</div>
                                                            <div>(6) Copy of the project report if transfer permission is for Industrial/Institutional plot/premises.</div>
                                                            <div>(7) No Objection Certificate issued by GM (DIC) Noida and No Dues Certificate issued by UPPCL (Power Corporation) shall also be required for transfer of industrial plot/premises.</div>
                                                            <div>(8) Copy of Occupancy Certificate/Completion Certificate issued by Building Cell for transfer of Residential plots/Functional Certificate for transfer of Industrial/ Commercial/Institutional plot/premises.<br/>OR<br/>Copy of the extension letter valid upto the date of transfer issued by the concerned department(Other than Industrial Properties.).</div>
                                                            <div>(9) If the plot/premises is mortgaged then a No Objection Certificate for permitting transfer to be issued by the financial institution shall also be required.</div>
                                                            <div>(10) No Objection Certificate from the respective cooperative society for transfer of residential plots allotted to the members of cooperative societies.</div>
                                                            <div>(11) No Objection Certificate from AWHO, AFNHB, Builders, Co-operative Societies for the flats/ houses allotted by the respective institution.</div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">5</div>
                                                </div>

                                                {/* ============ PAGE 6: GPA Enclosures + Corporate + Prescribed Categories ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[8.5pt] text-justify">
                                                        <div className="font-bold mb-2 text-[9pt]">Requirements/Enclosures for transfer of plot/premises on request of the General Power of Attorney of the allottee.</div>
                                                        <div className="mb-2">In addition to the above requirement/enclosures the following shall also be required:</div>
                                                        <div className="space-y-1 mb-4">
                                                            <div>(1) Certified copy of the General Power of Attorney given by the allottee for transfer of the plot/premises.</div>
                                                            <div>(2) An indemnity bond by the transferee in the prescribed format.</div>
                                                            <div>(3) An affidavit by the transferee about legal validity of the GPA on the prescribed format.</div>
                                                            <div>(4) A copy of the registered agreement to sell in favour of the transferee.</div>
                                                            <div>(5) In absence of registered agreement to sell, a public notice, as per the language provided by the Authority, in two national dailies. Full pages of the newspapers carrying the public notice shall required to be submitted.</div>
                                                        </div>

                                                        <div className="font-bold mb-1 text-[9pt]">If the transferor/transferee is a partnership firm/Pvt. Ltd. Co./Ltd. Co./Regd. Society/Trust in addition to the above the following documents shall also be required:</div>
                                                        <div className="space-y-1 mb-4">
                                                            <div>a) A certified copy of the partnership deed of transferee, copy of form A &amp; B (certificates issued by Registrar of firms),</div>
                                                            <div>b) An Authority letter or Power of Attorney to purchase the plot/premises is required if transfer application is not signed by all partners.</div>
                                                            <div>c) An Authority letter or Power of Attorney of the transferor firm shall also be required if transfer application is not signed by all partners.</div>
                                                            <div>d) A certified copy of the resolution passed by board of directors of the transferor company/society/trust to sell the plot/premises and of the transferee company/society/trust to purchase the plot/premises. Both resolutions shall be in favour of the authorised signatory to sell/purchase the plot/premises.</div>
                                                            <div>e) Memorandum and article of association of the company/Memorandum of the society/trust of the transferee.</div>
                                                            <div>f) In case of company list of shareholders and list of directors duly certified by Chartered Accountant/list of executive members of the society/list of trustees in case of society/trust.</div>
                                                            <div>g) Attested photograph and signatures of all directors/society executive members and trustees.</div>
                                                        </div>

                                                        <div className="font-bold mb-1 text-[9pt]">The following shall fall into the prescribed categories:</div>
                                                        <div className="space-y-1">
                                                            <div>1. Bonafide Sole Proprietor/Partner(s)/Director(s)/Regular Employees of bonafide functional industrial units who are operational on the land leased by NOIDA/NEPZ (Category : NOIDA-IND)</div>
                                                            <div>2. Bonafide Sole Proprietor/Partner(s)/Director(s) of the bonafide functional commercial establishment, established on land/premises allotted by NOIDA, exclusively &amp; specifically for this purpose only. (Category : NOIDA-COMM).</div>
                                                            <div>3. Bonafide Managing Trustees/Regular Employees of functional institutional which are operational on land/premises leased by NOIDA, exclusively for this purpose. (Category : NOIDA-INSTT).</div>
                                                            <div>4. Bonafide eligible villager who was a KHATEDAR/SAHKHATEDAR of the land which has been acquired for the development of NOIDA and who has received compensation of acquired land and there is no litigation pending (Category : NOIDA-VIL).</div>
                                                            <div>5. Regular employees of the Authority or regular employees of the Authority. (Category : NOIDA-EMP).</div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">6</div>
                                                </div>

                                                {/* ============ PAGE 7: Joint Affidavit (Stamp Paper Rs. 20) - Page 1 ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-center text-[9pt] italic mb-2">Joint affidavit on non-judicial stamp paper of Rs. 20/- from transferor(s) and transferee (s) duly notarized.</div>

                                                    <div className="text-center font-bold text-[12pt] uppercase mb-4">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>

                                                    <div className="space-y-3 text-justify text-[9.5pt]">
                                                        {/* Transferor block OR GPA holder block */}
                                                        {!p.isGpa ? (
                                                            <p className="leading-relaxed">
                                                                I/We/M/s <Var name="transferor1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Name || p.allotteeName || ''}</span></Var>
                                                                {' '}<Var name="transferor1Relation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.transferor1Relation || 'S/o'}</span></Var>, W/o, D/o <Var name="transferor1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Father || p.allotteeFather || ''}</span></Var>
                                                                {' '}R/o <Var name="transferor1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferor1Address || p.allotteeAddress || ''}</span></Var>
                                                                {p.hasJointTransferor && p.transferor2Name && <> and <Var name="transferor2Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferor2Name}</span></Var> <Var name="transferor2Relation"><span>{p.transferor2Relation || 'S/o'}</span></Var> Shri <Var name="transferor2Father"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferor2Father || ''}</span></Var> R/o <Var name="transferor2Address"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferor2Address || ''}</span></Var></>}
                                                                {' '}transferor of Plot/Premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var> Noida, measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> sq. mtrs.
                                                            </p>
                                                        ) : (
                                                            <p className="leading-relaxed text-gray-400 line-through select-none text-[9pt]">
                                                                I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor of Plot/Premises No. ________ Block ________ Sector ________ Noida, measuring ________ sq. mtrs.
                                                            </p>
                                                        )}

                                                        <div className="text-center font-bold">OR</div>

                                                        {/* GPA holder alternative */}
                                                        {p.isGpa ? (
                                                            <p className="leading-relaxed">
                                                                I/We/M/s <Var name="gpaHolderName"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderName || ''}</span></Var>
                                                                {' '}<Var name="gpaHolderRelation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.gpaHolderRelation || 'S/o'}</span></Var>, W/o, D/o <Var name="gpaHolderFather"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderFather || ''}</span></Var>
                                                                {' '}R/o <Var name="gpaHolderAddress"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.gpaHolderAddress || ''}</span></Var>
                                                                {' '}transferor of Plot/Premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var> Noida, measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> sq. mtrs. on behalf of the allottee Shri/Smt./Km. <Var name="transferor1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Name || p.allotteeName || ''}</span></Var>
                                                                {' '}<Var name="transferor1Relation"><span>{p.transferor1Relation || 'S/o'}</span></Var>, W/o, D/o <Var name="transferor1Father"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferor1Father || p.allotteeFather || ''}</span></Var>
                                                                {' '}R/o <Var name="transferor1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferor1Address || p.allotteeAddress || ''}</span></Var>
                                                                {' '}as registered General Power of Attorney holder, GPA registered with Sub-Registrar/Tehsildar No. <Var name="gpaRegNo"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{p.gpaRegNo || ''}</span></Var> dated <Var name="gpaRegDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaRegDate) !== '__________' ? formatDate(p.gpaRegDate) : ''}</span></Var> (strike off if application is not through GPA.)
                                                            </p>
                                                        ) : (
                                                            <p className="leading-relaxed text-gray-400 line-through select-none text-[9pt]">
                                                                I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor of Plot/Premises No. ________ Block ________ Sector ________ Noida, measuring ________ sq. mtrs. on behalf of the allottee Shri/Smt./Km. ______________________ S/o, W/o, D/o ______________________ R/o ______________________ as registered General Power of Attorney holder, GPA registered with Sub-Registrar/Tehsildar No. ______________________ dated ______________________ (strike off if application is not through GPA.)
                                                            </p>
                                                        )}

                                                        <div className="text-center font-bold">AND</div>

                                                        {/* Transferee block */}
                                                        <p className="leading-relaxed">
                                                            I/We/M/s <Var name="transferee1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Name || p.transfereeName || ''}</span></Var>
                                                            {' '}<Var name="transferee1Relation"><span className="border-b border-dotted border-black inline-block min-w-[30px]">{p.transferee1Relation || 'S/o'}</span></Var>, W/o, D/o <Var name="transferee1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Father || p.transfereeFather || ''}</span></Var>
                                                            {' '}R/o <Var name="transferee1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferee1Address || p.transfereeAddress || ''}</span></Var>
                                                            {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and <Var name="transferee2Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee2Name}</span></Var> <Var name="transferee2Relation"><span>{p.transferee2Relation || 'S/o'}</span></Var> Shri <Var name="transferee2Father"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee2Father || ''}</span></Var> R/o <Var name="transferee2Address"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee2Address || ''}</span></Var></>}
                                                            {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and <Var name="transferee3Name"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee3Name}</span></Var> <Var name="transferee3Relation"><span>{p.transferee3Relation || 'S/o'}</span></Var> Shri <Var name="transferee3Father"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee3Father || ''}</span></Var> R/o <Var name="transferee3Address"><span className="border-b border-dotted border-black inline-block min-w-[120px] font-bold">{p.transferee3Address || ''}</span></Var></>}
                                                            {' '}transferee for the above stated plot/premises do hereby solemnly affirm and declare jointly on oath as under in respect of Plot/Premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var> Noida, measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> sq. mtrs
                                                        </p>
                                                    </div>

                                                    {/* Affidavit Points 1-6 */}
                                                    <div className="mt-3 text-[9.5pt] text-justify space-y-1.5">
                                                        <div>1. That the transferor and transferee are bonafide citizen of India and are competent to contract.</div>
                                                        <div>2. That the deponents understand that the said plot/premises is transferable on payment of transfer charges, as applicable, to the Authority.</div>
                                                        <div>3. That the deponents undertake to abide by the rules, regulations terms and conditions and directions of the New Okhla Industrial Development Authority (NOIDA) as applicable from time to time.</div>
                                                        <div>4. That the transfer of rights, interest, payments, assets, liabilities, title etc. respect to the property are limited to the extent vested in the Transferor.</div>
                                                        <div>5. (i) That the dues in respect of above said plot/premises have been cleared and No Dues Certificate, issued by the concerned Accounts Officer is enclosed.<br/>(ii) That the dues in respect of usages charges/no usages charges, as applicable, have been cleared and a no dues certificate issued by the Account Officer (Jal) has been enclosed.</div>
                                                        <div>6. That the transferor has established the unit/enterprise on the above stated premises and a copy of the functional certificate issued by the Authority is enclosed.(applicable for transfer of Industrial/Institutional/Commercial plot/premises)</div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">7</div>
                                                </div>

                                                {/* ============ PAGE 8: Joint Affidavit cont - Points 6(cont)-11(i) ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[9.5pt] text-justify space-y-2">
                                                        <div className="pl-4">
                                                            That the transferor has obtained Occupancy certificate/completion certification issued by the Authority (applicable for transfer of Residential plot/premises)<br/>
                                                            <strong>OR</strong><br/>
                                                            That the transferor has obtained valid extension upto the date of transfer and a copy of the extension letter issued by the Authority is enclosed.<br/>
                                                            (Not applicable for transfer of Group Housing/Housing)
                                                        </div>
                                                        <div>7. That the above property has neither been mortgaged nor offered as collateral security to any institution and is free from all encumbrances.</div>
                                                        <div>8. That the deponents have ensured that there is no unauthorized construction and/or use in the property.</div>
                                                        <div>9. (i) The transferor, his/her spouse and/or dependent children and/or his/her/their Industrial/Commercial/Institutional unit established in NOIDA had not obtained any residential plot/premises (i.e. including the property for which this transfer application is being submitted) by way of direct allotment from the Authority and he/she/they, their spouse and/or dependent children and/or his/her/their Industrial/Commercial/ Institutional unit would not apply for allotment of any residential plot/premises under any allotment scheme of the Authority and not take possession of any residential plot/premises in any pending scheme(s) or any future scheme of the Authority but may acquire one or more residential plot/house/flat in NOIDA through transfer from open market.<br/>
                                                        (ii) That the transferor his spouse/dependent children is/are not a member of any cooperative housing society nor will become member of any cooperative housing society operating in notified area of NOIDA.<br/>
                                                        (iii) That the transferor understand(s) that in case of any breach of any to he terms and conditions, the Authority shall take action as it may deem fit.<br/>
                                                        (iv) That the transferor is applying for transfer of the plot/premises under the terms of allotment/Lease deed/Lease-cum-sale-deed/transfer deed executed on <Var name="leaseDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.leaseDate) !== '__________' ? formatDate(p.leaseDate) : ''}</span></Var> (applicable for transfer of residential plot/flat/houses)</div>
                                                        <div>10. (i) That the transferee shall pay to the Authority all outstanding dues along with interest as applicable.<br/>
                                                        (ii) That the outstanding premium/ lease rent /interest and all other dues against the plot/premises shall constitute the first charge against the plot/premises.</div>
                                                        <div>11. (i) That the deponents understands that the receipt of the transfer application and charges by the Authority are purely provisional and does not provide/constitute any right to either party for claiming grant of Transfer Permission by the Authority. The Authority reserves the right to decide the case on merit and is free to reject a request for transfer without assigning any reason.</div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">8</div>
                                                </div>

                                                {/* ============ PAGE 9: Joint Affidavit cont - Points 11(ii)-13 ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[9.5pt] text-justify space-y-2">
                                                        <div>(ii) In the event of such rejection the transfer charges deposited, if any, shall be refunded to the transferor. No interest, however, shall be payable on the deposits so made.</div>
                                                        <div>(iii) If transfer does not materialize due to withdrawal of the transfer application by mutual consent of the transferor and transferee then transfer charges will not be refunded/adjusted even if transfer application is withdrawn. In case of dispute between the transferor and transferee, permission for withdrawal of transfer application shall be granted with orders of the competent court.</div>
                                                        <div>(iv) The transferee shall not transfer his/her/their rights without prior approval of the Authority in writing which the Authority may refuse without assigning any reason or allow on such terms and conditions as it may deem fit.</div>
                                                        <div>(v) The transfer of plot/premises is an act between the transferor and transferee and as such any liens, claims, damages, compensation, adverse court orders etc. arising thereof subsequently would be the sole liability of transferee(s) and Noida would remain indemnified against the same.</div>
                                                        <div>12. (i) That in the event of transfer being permitted by the Authority the deponents shall have to execute a transfer deed and thereafter shall be entitled to lease hold rights for the remaining period of 90 years from the date of execution of original legal documents or taking over possession of the plot/premises, whichever is earlier.<br/>
                                                        (ii) The transfer deed shall be executed within 90 days from the date of issue of transfer memorandum. The transfer deed must, inter alia, incorporate the various terms and conditions mentioned in the transfer memorandum. The final mutation will be made in the name of the transferee after receipt of the certified copy of the transfer deed and its acceptance by the Authority. This transfer deed shall be required to be submitted with the Authority within one month from the date of its execution. In case of failure to execute lease-Cum-Sale Deed/Transfer Deed (as the case may be) by the Transferee would invite payment of penalty as applicable from time to time.<br/>
                                                        (iii) The transferee shall be given one year for making the industrial unit/commercial establishment/institution functional from the date of issue of the transfer memorandum. The transferee of residential plot shall be required to obtain extension on payment of prescribed extension charges to raise construction/ obtain occupancy/completion certificate.</div>
                                                        <div>13. That the lease rent/ground rent of the subject property shall be revised and shall be payable as indicated by the Authority in transfer permission letter. The revised lease rent/ground rent may be enhanced after every 10 years from the date of execution of the original lease deed/legal documents subject to the condition that the same shall not exceed 50% of the lease/ground rent last thus fixed. (in case of commercial plot/shop lease rent shall not be revised, however, provision of enhancement as per terms of lease deed shall be applicable.</div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">9</div>
                                                </div>

                                                {/* ============ PAGE 10: Joint Affidavit cont - Points 14-21 + Signatures + Verification ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-[9.5pt] text-justify space-y-1.5">
                                                        <div>14. That the deponents understand that notwithstanding any request/instruction of either party the payment made by the either party shall be first adjusted towards the interest due and premium/cost of the property and thereafter the same shall be appropriated towards the annual lease/ground rent.</div>
                                                        <div>15. That the transferee shall put the plot/premises in use exclusively for the authorized purpose and shall not use it for any purpose other than the allotted/leased.</div>
                                                        <div>16. The lease rent/ground/rent of the aforesaid property shall be applicable as indicated in the transfer memorandum.</div>
                                                        <div>17. The transferee shall put the commercial property/plot/shop in use for which it has been allotted.</div>
                                                        <div>18. The deponents understand that the Chief Executive Officer of the Authority shall have every right to amend or after the terms and conditions as deemed fit from time to time and such amendments/modifications shall be final and binding on them.</div>
                                                        <div>19. The transferor and transferee agree that in the event of transfer being obtained through misrepresentation/suppression or fact or in case of any breach/violation of terms and conditions of the brochure of the Scheme/ HPTA/Licence Agreement/Lease Deed/Transfer Deed and the terms and conditions stated here is this affidavit, the Authority shall be free to take action as deemed fit and exercise its right for cancellation of allotment/lease hold rights including forfeiture of the deposited amount.</div>
                                                        <div>20. The deponent shall be bound by the provisions of U.P. Industrial Area Development Act, 1976 (U.P. Act No. 6 of 1976) and the rules and regulations made and/or directions issued there under and enacted/amended from time to time.</div>
                                                        <div>21. The deponent undertakes that the dispute, if any, with regards to approval of transfer of property and or otherwise shall be subject to the Courts Jurisdiction of High Court Allahabad/Civil Court Ghaziabad/ Gautam Budh Nagar.</div>
                                                    </div>

                                                    <div className="flex justify-between text-center mt-8 text-[9pt]">
                                                        <div className="w-40">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT<br/>(TRANSFEROR)</div>
                                                        </div>
                                                        <div className="w-40">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT<br/>(TRANSFEREE)</div>
                                                        </div>
                                                    </div>

                                                    <div className="mt-4 border-t border-black pt-3">
                                                        <div className="text-center font-bold uppercase mb-2">VERIFICATION</div>
                                                        <p className="text-justify text-[9.5pt]">We the above deponents do hereby verify that the contents and declarations made in the affidavit are true to the best or our respective knowledge and belief and nothing has been canceled.</p>
                                                    </div>

                                                    <div className="flex justify-between text-center mt-8 text-[9pt]">
                                                        <div className="w-40">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT<br/>(TRANSFEROR)</div>
                                                        </div>
                                                        <div className="w-40">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT<br/>(TRANSFEREE)</div>
                                                        </div>
                                                    </div>

                                                    <div className="mt-4 text-[8pt]">
                                                        <strong>NOTE:-</strong> Affidavit is to be given on non-judicial stamp paper of Rs.20/- and duly notarized by Notary Public.
                                                    </div>

                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">10</div>
                                                </div>

                                                {/* ============ PAGE 11: GPA Affidavit (Stamp Paper Rs. 10) - CONDITIONAL ============ */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none pt-40">
                                                            <div className="text-gray-400 text-[10pt] font-bold">Page 11: Transferee GPA Affidavit</div>
                                                            <p className="text-[9pt] text-gray-400">This affidavit is required only when application is submitted through Power of Attorney. Hidden from print because GPA is not applicable.</p>
                                                            <div className="text-[8pt] text-gray-500 border border-gray-300 px-3 py-1 inline-block">Page 11 - Omitted from Print (GPA not active)</div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="text-center font-bold uppercase text-[10pt] mb-1">TO BE SUBMITTED BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY</div>
                                                            <div className="text-center text-[9pt] mb-3">(ON NON JUDICIAL STAMP PAPER OF RS. 10/- DULY NOTARISED)</div>
                                                            <div className="text-center font-bold text-[12pt] uppercase mb-4">AFFIDAVIT</div>

                                                            <p className="text-justify text-[9.5pt] leading-relaxed mb-3">
                                                                I, <Var name="transferee1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Name || p.transfereeName || ''}</span></Var> aged <Var name="transferee1Age"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.transferee1Age || ''}</span></Var> Years <Var name="transferee1Relation"><span>{p.transferee1Relation || 'S/o'}</span></Var>, D/o, W/o Shri <Var name="transferee1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Father || p.transfereeFather || ''}</span></Var>
                                                                {' '}R/o <Var name="transferee1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferee1Address || p.transfereeAddress || ''}</span></Var>
                                                                {' '}hereby solemnly affirm and state on oath as under:-
                                                            </p>

                                                            <div className="space-y-2 text-justify text-[9.5pt]">
                                                                <div>1- That deponent is transferee of plot/premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var>, NOIDA measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var>Sqm.</div>
                                                                <div>2- That Sh./Smt./Km. <Var name="transferor1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Name || p.allotteeName || ''}</span></Var> <Var name="transferor1Relation"><span>{p.transferor1Relation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="transferor1Father"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferor1Father || p.allotteeFather || ''}</span></Var> R/o <Var name="transferor1Address"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferor1Address || p.allotteeAddress || ''}</span></Var> is the allottee of Plot/ premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector- <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var>, NOIDA measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sqm.</div>
                                                                <div className="text-center font-bold">OR</div>
                                                                <div>3- That Sh./Smt./Km. <Var name="gpaHolderName"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderName || ''}</span></Var> <Var name="gpaHolderRelation"><span>{p.gpaHolderRelation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="gpaHolderFather"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.gpaHolderFather || ''}</span></Var> R/o <Var name="gpaHolderAddress"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.gpaHolderAddress || ''}</span></Var> is power of Attorney holder of the allottee and submitting application for transfer of the plot/premises on behalf of the allottee. General Power of Attorney was executed on <Var name="gpaDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaDate) !== '__________' ? formatDate(p.gpaDate) : ''}</span></Var> and registered with Sub-Registrar/Tehsildar <Var name="gpaOffice"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{p.gpaOffice || ''}</span></Var> on <Var name="gpaRegDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaRegDate) !== '__________' ? formatDate(p.gpaRegDate) : ''}</span></Var> at <Var name="gpaRegNo"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{p.gpaRegNo || ''}</span></Var> for plot/premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.sector || ''}</span></Var> measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sqm.</div>
                                                                <div>4- That the said GPA has not been revoked so far.</div>
                                                                <div>5- That the deponent has satisfied himself about the authenticity and legal validity of the above stated Power of Attorney and the allottee of the plot/ premises as stated at Sl. No. 2 above is alive.</div>
                                                            </div>

                                                            <div className="flex justify-end mt-10">
                                                                <div className="w-40 text-center">
                                                                    <div className="h-12"></div>
                                                                    <div className="border-t border-black pt-1 font-bold">DEPONENT</div>
                                                                </div>
                                                            </div>

                                                            <div className="mt-4 border-t border-black pt-3">
                                                                <div className="text-center font-bold uppercase mb-2">VERIFICATION</div>
                                                                <p className="text-justify text-[9.5pt]">I, the above named deponent do hereby verify that the above contents from para 1 to 5 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.</p>
                                                            </div>

                                                            <div className="flex justify-end mt-10">
                                                                <div className="w-40 text-center">
                                                                    <div className="h-12"></div>
                                                                    <div className="border-t border-black pt-1 font-bold">DEPONENT</div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">11</div>
                                                </div>

                                                {/* ============ PAGE 12: Transferee Affidavit (Stamp Paper Rs. 10) ============ */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-center font-bold uppercase text-[10pt] mb-1">TO BE SUBMITTED BY TRANSFEREE</div>
                                                    <div className="text-center text-[9pt] mb-3">(ON NON JUDICIAL STAMP PAPER OF RS. 10/- DULY NOTARISED)</div>
                                                    <div className="text-center font-bold text-[12pt] uppercase mb-4">AFFIDAVIT</div>

                                                    <p className="text-justify text-[9.5pt] leading-relaxed mb-3">
                                                        I, <Var name="transferee1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Name || p.transfereeName || ''}</span></Var> aged <Var name="transferee1Age"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.transferee1Age || ''}</span></Var> Years <Var name="transferee1Relation"><span>{p.transferee1Relation || 'S/o'}</span></Var>, D/o, W/o Shri <Var name="transferee1Father"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Father || p.transfereeFather || ''}</span></Var>
                                                        {' '}R/o <Var name="transferee1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferee1Address || p.transfereeAddress || ''}</span></Var>
                                                        {' '}hereby solemnly affirm and state on oath as under:-
                                                    </p>

                                                    <div className="space-y-3 text-justify text-[9.5pt]">
                                                        <div>1. That the deponent is transferee of plot/premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var>, NOIDA measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var>Sqm.</div>
                                                        <div>2. That Sh./Smt./Km. <Var name="transferor1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferor1Name || p.allotteeName || ''}</span></Var> <Var name="transferor1Relation"><span>{p.transferor1Relation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="transferor1Father"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferor1Father || p.allotteeFather || ''}</span></Var> R/o <Var name="transferor1Address"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferor1Address || p.allotteeAddress || ''}</span></Var> is the allottee of Plot/ premises No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.block || ''}</span></Var> Sector- <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var>, NOIDA measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sqm.</div>
                                                        <div>3. That the deponent has satisfied himself that the said plot/premises are without any encumbrance.</div>
                                                        <div>4. That the deponent has received/shall receive from the transferor all original documents such as allotment letter, possession letter, lease deed, transfer memorandum, transfer deed, no dues certificate, extension letter/occupancy/completion certificate/functional certification, payment deposit challans, etc. pertaining to the above stated plot/premises.</div>
                                                    </div>

                                                    <div className="flex justify-end mt-10">
                                                        <div className="w-40 text-center">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT</div>
                                                        </div>
                                                    </div>

                                                    <div className="mt-4 border-t border-black pt-3">
                                                        <div className="text-center font-bold uppercase mb-2">VERIFICATION</div>
                                                        <p className="text-justify text-[9.5pt]">I, the above named deponent do hereby verify that the above contents from para 1 to 4 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.</p>
                                                    </div>

                                                    <div className="flex justify-end mt-10">
                                                        <div className="w-40 text-center">
                                                            <div className="h-12"></div>
                                                            <div className="border-t border-black pt-1 font-bold">DEPONENT</div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">12</div>
                                                </div>

                                                {/* ============ PAGE 13: Indemnity Bond Page 1 (Stamp Paper Rs. 100) - CONDITIONAL ============ */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none pt-40">
                                                            <div className="text-gray-400 text-[10pt] font-bold">Page 13: Indemnity Bond (Page 1)</div>
                                                            <p className="text-[9pt] text-gray-400">This indemnity bond is required only for GPA-based transfers. Hidden from print because GPA is not applicable.</p>
                                                            <div className="text-[8pt] text-gray-500 border border-gray-300 px-3 py-1 inline-block">Page 13 - Omitted from Print (GPA not active)</div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="text-center text-[9pt] mb-1">(ON NON JUDICIAL STAMP PAPER RS. 100/- DULY NOTARISED)</div>
                                                            <div className="text-center font-bold uppercase text-[10pt] mb-4">INDEMNITY BOND BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY</div>

                                                            <p className="text-justify text-[9.5pt] leading-relaxed mb-3">
                                                                This Indemnity Bond is executed on <span className="border-b border-dotted border-black inline-block min-w-[40px]"></span> day of <span className="border-b border-dotted border-black inline-block min-w-[60px]"></span> in the year Two thousand <span className="border-b border-dotted border-black inline-block min-w-[80px]"></span> by Shri/Smt./Km. <Var name="transferee1Name"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.transferee1Name || p.transfereeName || ''}</span></Var> <Var name="transferee1Relation"><span>{p.transferee1Relation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="transferee1Father"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.transferee1Father || p.transfereeFather || ''}</span></Var> R/o <Var name="transferee1Address"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.transferee1Address || p.transfereeAddress || ''}</span></Var> (transferee) hereinafter referred as &apos;EXECUTANT&apos; in favour of New Okhla Industrial Development Authority hereinafter referred to as &apos;AUTHORITY&apos;.
                                                            </p>

                                                            <p className="text-justify text-[9.5pt] leading-relaxed mb-3">
                                                                Whereas Shri/Smt./Km. <Var name="gpaHolderName"><span className="border-b border-dotted border-black inline-block min-w-[180px] font-bold">{p.gpaHolderName || ''}</span></Var> <Var name="gpaHolderRelation"><span>{p.gpaHolderRelation || 'S/o'}</span></Var>, W/o, D/o Shri <Var name="gpaHolderFather"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.gpaHolderFather || ''}</span></Var> R/o <Var name="gpaHolderAddress"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.gpaHolderAddress || ''}</span></Var> on behalf of the allottee of commercial plot/ shop No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.sector || ''}</span></Var> measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sq.Mtrs. NOIDA holds the power of attorney (hereinafter called power of attorney) in respect of Plot/Shop No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.sector || ''}</span></Var> measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sqm. NOIDA and being bounded as under:-
                                                            </p>

                                                            {/* Boundaries */}
                                                            <div className="text-[9.5pt] space-y-1 mb-3 pl-4">
                                                                <div>ON THE NORTH BY <Var name="northBoundary"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.northBoundary || ''}</span></Var></div>
                                                                <div>ON THE SOUTH BY <Var name="southBoundary"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.southBoundary || ''}</span></Var></div>
                                                                <div>ON THE EAST BY <Var name="eastBoundary"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.eastBoundary || ''}</span></Var></div>
                                                                <div>ON THE WEST BY <Var name="westBoundary"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.westBoundary || ''}</span></Var></div>
                                                            </div>

                                                            <p className="text-justify text-[9.5pt] leading-relaxed">
                                                                By virtue of the powers conferred upon Shri/Smt./Km. <Var name="gpaHolderName"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.gpaHolderName || ''}</span></Var> <Var name="gpaHolderRelation"><span>{p.gpaHolderRelation || 'S/o'}</span></Var>, W/o, D/o <Var name="gpaHolderFather"><span className="border-b border-dotted border-black inline-block min-w-[150px] font-bold">{p.gpaHolderFather || ''}</span></Var> R/o <Var name="gpaHolderAddress"><span className="border-b border-dotted border-black inline-block min-w-[200px] font-bold">{p.gpaHolderAddress || ''}</span></Var> vide the attorney dated <Var name="gpaDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaDate) !== '__________' ? formatDate(p.gpaDate) : ''}</span></Var> duly registered with Sub-Registrar on <Var name="gpaRegDate"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{formatDate(p.gpaRegDate) !== '__________' ? formatDate(p.gpaRegDate) : ''}</span></Var> at <Var name="gpaRegNo"><span className="border-b border-dotted border-black inline-block min-w-[80px] font-bold">{p.gpaRegNo || ''}</span></Var> (certified copy enclosed). The executant is getting commercial plot/shop No. <Var name="plotNo"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.plotNo || ''}</span></Var> Block <Var name="block"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.block || ''}</span></Var> Sector <Var name="sector"><span className="border-b border-dotted border-black inline-block min-w-[30px] font-bold">{p.sector || ''}</span></Var>, NOIDA measuring <Var name="area"><span className="border-b border-dotted border-black inline-block min-w-[40px] font-bold">{p.area || ''}</span></Var> Sqm. transferred in his name.
                                                            </p>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">13</div>
                                                </div>

                                                {/* ============ PAGE 14: Indemnity Bond Page 2 - CONDITIONAL ============ */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none pt-40">
                                                            <div className="text-gray-400 text-[10pt] font-bold">Page 14: Indemnity Bond (Page 2)</div>
                                                            <p className="text-[9pt] text-gray-400">Continuation of indemnity bond with signatures and witnesses. Hidden from print because GPA is not applicable.</p>
                                                            <div className="text-[8pt] text-gray-500 border border-gray-300 px-3 py-1 inline-block">Page 14 - Omitted from Print (GPA not active)</div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="space-y-3 text-justify text-[9.5pt]">
                                                                <p className="indent-8">The executant is satisfied that as per the above documents the power of attorney holder is totally competent and legally authorized to effect the transfer/sale of the above mentioned property and to do all acts and execute all documents which are necessary for transfer/sale of the said property on behalf of the present allottee.</p>
                                                                <p className="indent-8">And whereas the Authority shall consider the transfer in favour of the executant provided the executant indemnifies the Authority against all losses, damages, inconvenience, cost and or litigation which may be caused because of such permission of transfer by Authority.</p>
                                                                <p className="indent-8">Now the (transferee) executant in the event of grant of permission by the Authority for sale/transfer of the above said property has agreed to indemnify the Authority against any claim/damage, cost, loss, inconvenience, litigation arising by the grant of permission for transfer of the above property. The executant also indemnifies the Authority for any liability in all forms that may be created by virtue of a court order and/or any other Competent Authority.</p>
                                                                <p className="indent-8">By this deed the executant shall also be totally responsible for other costs, damages, legal proceedings and any other loss to the Authority on account of above property and shall ensure to meet all the liabilities arising or which may arise by grant of permission to transfer and shall discharge the same from his own resources.</p>
                                                                <p className="indent-8">This indemnity Bond is executed in presence of the following witnesses on the day and month first above mentioned.</p>
                                                            </div>

                                                            <div className="flex justify-end mt-8">
                                                                <div className="w-56 text-center">
                                                                    <div className="h-12"></div>
                                                                    <div className="border-t border-black pt-1 font-bold">SIGNATURE OF THE EXECUTANT<br/>(TRANSFEREE)</div>
                                                                </div>
                                                            </div>

                                                            <div className="mt-8 text-[9.5pt]">
                                                                <div className="font-bold uppercase mb-3">WITNESSES</div>
                                                                <div className="space-y-4">
                                                                    <div>
                                                                        <div>1. NAME <span className="border-b border-dotted border-black inline-block min-w-[250px]"></span></div>
                                                                        <div className="pl-3">ADDRESS <span className="border-b border-dotted border-black inline-block min-w-[240px]"></span></div>
                                                                        <div className="pl-12"><span className="border-b border-dotted border-black inline-block min-w-[250px]"></span></div>
                                                                    </div>
                                                                    <div>
                                                                        <div>2. NAME <span className="border-b border-dotted border-black inline-block min-w-[250px]"></span></div>
                                                                        <div className="pl-3">ADDRESS <span className="border-b border-dotted border-black inline-block min-w-[240px]"></span></div>
                                                                        <div className="pl-12"><span className="border-b border-dotted border-black inline-block min-w-[250px]"></span></div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt] text-black">14</div>
                                                </div>
                                            </>
                                        );
                                    })()}'''

def main():
    # Read the current file
    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Total lines in file: {len(lines)}")
    print(f"Line 6172: {lines[6171][:80].strip()}")
    print(f"Line 6921: {lines[6920][:80].strip()}")
    print(f"Line 6922: {lines[6921][:80].strip()}")
    print(f"Line 6923: {lines[6922][:80].strip()}")

    # Lines are 0-indexed in the array, but 1-indexed in the spec
    # We want to replace lines 6172-6923 (inclusive, 1-indexed)
    # That is indices 6171 to 6922 (inclusive, 0-indexed)
    # The section ends at })()}  which is line 6923

    before = lines[:6171]   # lines 1..6171
    after = lines[6923:]    # lines 6924..end

    # Build the replacement
    new_content = NEW_JSX + '\n'

    # Write back
    with open('test_script.jsx', 'w', encoding='utf-8') as f:
        f.writelines(before)
        f.write(new_content)
        f.writelines(after)

    # Count new line total
    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        new_lines = f.readlines()
    print(f"New total lines: {len(new_lines)}")
    print("Replacement complete!")

if __name__ == '__main__':
    main()
