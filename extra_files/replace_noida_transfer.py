import os
import subprocess
import re

def compile_check():
    print("Running build.py to verify syntax...")
    result = subprocess.run("python build.py", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Compilation failed!")
        print(result.stderr)
        return False
    print("Compilation succeeded!")
    return True

def main():
    backup_file = 'test_script.jsx.bak'
    if not os.path.exists(backup_file):
        print("Creating backup of test_script.jsx...")
        with open('test_script.jsx', 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the new NOIDA_TRANSFER render block
    noida_transfer_jsx = """{activeTab === 'NOIDA_TRANSFER' && (() => {
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
                                                {/* PAGE 1: Main Application Form */}
                                                <div className="paper-page print-break bg-white p-10 font-sans relative text-[9pt] leading-normal flex flex-col justify-between min-h-[1123px]">
                                                    <EsignBadge type="NOIDA_TRANSFER" />
                                                    <div>
                                                        <div className="text-center font-bold text-[13px] tracking-tight text-blue-900 uppercase">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>
                                                        <div className="text-center font-extrabold text-[12px] my-1 uppercase underline decoration-double">TRANSFER APPLICATION FORM (valid for six months)</div>
                                                        <div className="text-center text-[7pt] text-gray-500 font-bold mb-4 uppercase leading-tight max-w-2xl mx-auto border border-gray-200 p-1.5 bg-gray-50 rounded">
                                                            FOR TRANSFER OF RESIDENTIAL PLOTS/GROUP HOUSING (flats and houses allotted by AWHO, AFNHB, Builders, Co-operative Societies) /HOUSING (Flats/Houses allotted by NOIDA)/ INDUSTRIAL PLOTS & SHEDS/COMMERCIAL SHOPS & PLOTS/ INSTITUTIONAL PLOTS
                                                        </div>

                                                        {/* Form serial & deposit metadata */}
                                                        <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 border border-slate-300 p-2.5 rounded-lg mb-4 text-[8pt]">
                                                            <div>Price: <strong>Rs. 100/- (Rupees One Hundred Only)</strong></div>
                                                            <div>Sl. No. : <strong>[<Var name="slNo">{p.slNo || '__________'}</Var>]</strong></div>
                                                            <div>Date of Issue by Authorized Bank: <strong>[<Var name="issueDate">{formatDate(p.issueDate)}</Var>]</strong></div>
                                                            <div>
                                                                Downloaded Form Fee Deposit Date: <strong>[<Var name="downloadDepositDate">{formatDate(p.downloadDepositDate)}</Var>]</strong>
                                                            </div>
                                                            {p.downloadDepositChallanNo && (
                                                                <div className="col-span-2 text-gray-700">
                                                                    Deposit Challan: <strong>[<Var name="downloadDepositChallanNo">{p.downloadDepositChallanNo}</Var>]</strong> {p.downloadDepositBank && <>at <strong>[<Var name="downloadDepositBank">{p.downloadDepositBank}</Var>]</strong></>}
                                                                </div>
                                                            )}
                                                        </div>

                                                        <div className="space-y-0.5 mb-4 text-[9pt] font-semibold text-gray-800">
                                                            <div>To,</div>
                                                            <div>ASSTT. GENERAL MANAGER/Dy. GENERAL MANAGER/GENERAL MANAGER,</div>
                                                            <div>NOIDA.</div>
                                                        </div>

                                                        {/* Deponent sentence */}
                                                        <p className="mb-3 text-justify leading-relaxed text-[8.5pt]">
                                                            I/ We/ M/s (allottee) <strong>[<Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var>]</strong>
                                                            {p.transferor1Age && <> aged <strong>[<Var name="transferor1Age">{p.transferor1Age}</Var>]</strong> years, </>}
                                                            {' '}<strong>[<Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var>]</strong>
                                                            {' '}R/o, Regd. Office <strong>[<Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var>]</strong>
                                                            {p.hasJointTransferor && p.transferor2Name && <> and Joint Transferor: <strong>[<Var name="transferor2Name">{p.transferor2Name}</Var>]</strong> {p.transferor2Age && <> aged <strong>[<Var name="transferor2Age">{p.transferor2Age}</Var>]</strong> years, </>} <strong>[<Var name="transferor2Relation">{p.transferor2Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor2Father">{p.transferor2Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferor2Address">{p.transferor2Address || '__________________'}</Var>]</strong></>}
                                                            {' '}is an allottee (here in shall be referred to as Transferor) of Plot/Flat or House on Group Housing Plot/Housing (Flat/ House/allotted by NOIDA)/ Industrial Plots & Sheds/Commercial Shop & Plots/Institutional Plot/ Premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block/Tower <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> NOIDA having an area of <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sq. Mtrs. want to transfer the above plot/premises in favour of Shri/Smt./M/s <strong>[<Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var>]</strong>
                                                            {p.transferee1Age && <> aged <strong>[<Var name="transferee1Age">{p.transferee1Age}</Var>]</strong> years, </>}
                                                            {' '}<strong>[<Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var>]</strong>
                                                            {' '}R/o, Regd Office <strong>[<Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var>]</strong>
                                                            {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and Transferee 2: <strong>[<Var name="transferee2Name">{p.transferee2Name}</Var>]</strong> {p.transferee2Age && <> aged <strong>[<Var name="transferee2Age">{p.transferee2Age}</Var>]</strong> years, </>} <strong>[<Var name="transferee2Relation">{p.transferee2Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee2Father">{p.transferee2Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferee2Address">{p.transferee2Address || '__________________'}</Var>]</strong></>}
                                                            {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and Transferee 3: <strong>[<Var name="transferee3Name">{p.transferee3Name}</Var>]</strong> {p.transferee3Age && <> aged <strong>[<Var name="transferee3Age">{p.transferee3Age}</Var>]</strong> years, </>} <strong>[<Var name="transferee3Relation">{p.transferee3Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee3Father">{p.transferee3Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferee3Address">{p.transferee3Address || '__________________'}</Var>]</strong></>}
                                                            {' '} (herein after shall be referred to as transferee).
                                                        </p>

                                                        {p.isGpa ? (
                                                            <div className="bg-purple-50/50 p-2 border border-purple-200 rounded mb-3 text-[8pt] leading-normal">
                                                                In case of transfer on the basis of authenticated GPA dt. <strong>[<Var name="gpaDate">{formatDate(p.gpaDate)}</Var>]</strong> through GPA Holder: <strong>[<Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var>]</strong>
                                                                {p.gpaHolderAge && <> aged <strong>[<Var name="gpaHolderAge">{p.gpaHolderAge}</Var>]</strong> years, </>}
                                                                {' '}<strong>[<Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var>]</strong> Address: <strong>[<Var name="gpaHolderAddress">{p.gpaHolderAddress || '____________________________________'}</Var>]</strong>.
                                                            </div>
                                                        ) : (
                                                            <div className="text-gray-400 line-through text-[7.5pt] mb-3 select-none">
                                                                In case of transfer on the basis of authenticated GPA dt. ________ through GPA of Holder Shri/Smt. ________ S/o, W/o, D/o Shri ________ Address: ________________ (Not Applicable)
                                                            </div>
                                                        )}

                                                        <p className="mb-4 text-justify leading-relaxed text-[8.5pt]">
                                                            The transferor(s) and the transferee(s) have read and understood the terms and conditions for transfer and undertake to abide by the same and accordingly apply for transfer of the above said <strong>[<Var name="useType">{p.useType || '________'}</Var>]</strong> plot/premises. In case of Industrial, the premises will be used for <strong>[<Var name="projectName">{p.projectName || '__________________'}</Var>]</strong> Project which is at Sl No___________ of Annexure-A enclosed with Transfer Application form and for Commercial/Institutional the premises will be used as per terms of the original lease (Change of Project is not allowed).
                                                        </p>
                                                    </div>

                                                    {/* Signatures & Attestations */}
                                                    <div>
                                                        <div className="flex justify-between items-start text-center mb-4 pt-2">
                                                            <div className="w-48">
                                                                <div className="h-8"></div>
                                                                <div className="border-t border-black pt-1 font-bold text-[8.5pt] uppercase">Signature of the Transferor(s)</div>
                                                                <div className="text-[7pt] text-gray-500 italic">Above Signatures are attested</div>
                                                            </div>
                                                            <div className="w-48">
                                                                <div className="h-8"></div>
                                                                <div className="border-t border-black pt-1 font-bold text-[8.5pt] uppercase">Signature of Transferee(s)</div>
                                                                <div className="text-[7pt] text-gray-500 italic">Above Signatures are attested</div>
                                                            </div>
                                                        </div>

                                                        {/* Bank Officer Attestation */}
                                                        <div className="grid grid-cols-2 gap-4 text-[7pt] leading-tight text-gray-600 mb-4">
                                                            <div className="border border-gray-300 p-2 rounded h-24 flex flex-col justify-between">
                                                                <div>Signature, Name Designation and seal of Bank Officer attesting the signature of Transferor:</div>
                                                                <div className="border-t border-dashed border-gray-300 pt-0.5 text-center italic text-gray-400">Official Stamp & Signature</div>
                                                            </div>
                                                            <div className="border border-gray-300 p-2 rounded h-24 flex flex-col justify-between">
                                                                <div>Signature, Name Designation and seal of Bank Officer attesting the signature of Transferee:</div>
                                                                <div className="border-t border-dashed border-gray-300 pt-0.5 text-center italic text-gray-400">Official Stamp & Signature</div>
                                                            </div>
                                                        </div>

                                                        {/* Photographs */}
                                                        <div className="flex gap-4 justify-center">
                                                            <div className="w-24 h-28 border border-gray-300 border-dashed flex items-center justify-center text-center text-[6.5pt] p-1.5 text-gray-500 uppercase bg-gray-50/50">
                                                                Photograph of Transferor Duly Attested by Banker
                                                            </div>
                                                            {p.isGpa && (
                                                                <div className="w-24 h-28 border border-purple-300 border-dashed flex items-center justify-center text-center text-[6.5pt] p-1.5 text-purple-600 uppercase bg-purple-50/20">
                                                                    Photograph of GPA Holder Duly Attested by Banker
                                                                </div>
                                                            )}
                                                            <div className="w-24 h-28 border border-gray-300 border-dashed flex items-center justify-center text-center text-[6.5pt] p-1.5 text-gray-500 uppercase bg-gray-50/50">
                                                                Photograph of Transferee Duly Attested by Banker
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 1</div>
                                                </div>

                                                {/* PAGE 2: Notes & Instructions */}
                                                <div className="paper-page print-break bg-white p-10 font-sans relative text-[8pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[11px] mb-3 uppercase underline">GENERAL TERMS & CONDITIONS FOR TRANSFER (Page 2)</div>
                                                        
                                                        <div className="space-y-1.5 text-justify text-gray-700">
                                                            <div className="font-bold text-gray-900 text-[8.5pt]">Note :</div>
                                                            <div><strong>(I)</strong> The term allottee includes transferee/sub lessee.</div>
                                                            <div><strong>(II)</strong> Signatures and Photograph of the Power of Attorney holder shall be required to be attested by the bankers, if the transfer application is submitted through General Power of Attorney Holder of the Allottee.</div>
                                                            <div><strong>(III)</strong> Group Housing means flats and houses allotted by AWHO, AFNHB, Builders and Co-operative Societies. Transfer of such flats/houses shall be considered alongwith transfer of garage, if it was allotted by the respective institution alongwith the flat/house.</div>
                                                            <div><strong>(IV)</strong> Transfer permission in favour of HUF shall not be allowed.</div>
                                                            <div><strong>(V)</strong> In case of industrial plot/premises transfer shall be permitted only after the unit has been declared functional.</div>
                                                            <div><strong>(VI)</strong> In case of industrial plot/premises project free from pollution & environment hazards shall be considered. The project should not be on the banned list of directorate of Industries, UP or Noida.</div>
                                                            <div><strong>(VII)</strong> The transfer charges for transfer Residential plot/flats/houses amongst the prescribed categories shall be 50% of the applicable transfer charges.</div>
                                                            <div><strong>(VIII)</strong> The transfer charges for transfer of industrial plots/sheds shall be 50% of the applicable transfer charges in cases of transfer/sale by financial institutions under section 29 of SFC Act.</div>
                                                            <div className="font-bold text-gray-900 text-[8.5pt] mt-2"><strong>(IX)</strong> Prevailing Transfer charges (Residential Plots Sector-wise rates per Sq. Mtr.):</div>
                                                        </div>

                                                        {/* Residential plot rates table */}
                                                        <table className="w-full mt-2 border-collapse border border-gray-300 text-[7.5pt]">
                                                            <thead>
                                                                <tr className="bg-gray-100">
                                                                    <th className="border border-gray-300 p-1 text-left">Sector Group / Sectors</th>
                                                                    <th className="border border-gray-300 p-1 text-right w-28">Rate (Rs./Sqm.)</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody>
                                                                <tr><td className="border border-gray-300 p-1">14A, 15A</td><td className="border border-gray-300 p-1 text-right font-semibold">4375.00</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">14, 17, 19, 30, 35, 47, 93</td><td className="border border-gray-300 p-1 text-right font-semibold">2323.75</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">11, 12, 15, 20, 21, 22, 23, 25 TO 29, 31, 33, 34, 40, 41, 46, 48, 53, 55, 56, 70, 82, 96 TO 100, 122</td><td className="border border-gray-300 p-1 text-right font-semibold">1619.75</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">42, 43, 45, 63A, 104, 107, 110, 118, 119, 120, 121, 128, 129, 130, 131, 133, 134, 135, 143, 151</td><td className="border border-gray-300 p-1 text-right font-semibold">1179.50</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">86, 112, 113, 116, 117</td><td className="border border-gray-300 p-1 text-right font-semibold">986.00</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">102, 115, 158, 162, ETC</td><td className="border border-gray-300 p-1 text-right font-semibold">905.00</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">44 (A & B BLOCK)</td><td className="border border-gray-300 p-1 text-right font-semibold">4703.13</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">44 (OTHER A&B), 93A, 93B</td><td className="border border-gray-300 p-1 text-right font-semibold">2498.03</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">105, 108</td><td className="border border-gray-300 p-1 text-right font-semibold">1741.23</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">128, 129, 143B, 154, 168</td><td className="border border-gray-300 p-1 text-right font-semibold">1267.96</td></tr>
                                                                <tr><td className="border border-gray-300 p-1">144</td><td className="border border-gray-300 p-1 text-right font-semibold">1326.94</td></tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 2</div>
                                                </div>

                                                {/* PAGE 3: GPA Rates & Instructions (Conditional Placeholder) */}
                                                <div className={`paper-page print-break bg-white p-10 font-sans relative text-[8pt] leading-relaxed flex flex-col justify-between min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-purple-200' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-4 max-w-md select-none">
                                                            <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto text-2xl border border-purple-100">
                                                                <i className="fa-solid fa-key"></i>
                                                            </div>
                                                            <h3 className="text-sm font-bold text-slate-800">Page 3: GPA Rates & General Instructions</h3>
                                                            <p className="text-[10px] text-slate-500 leading-normal">
                                                                This instruction page details GPA-based transfer charges. It is hidden from printing because <strong>Submit via GPA Holder</strong> is disabled.
                                                            </p>
                                                            <div className="text-[8px] text-purple-600 font-bold bg-purple-50 px-2.5 py-1 rounded w-fit mx-auto border border-purple-100">
                                                                Page 3 (GPA Instruction) - Omitted from Print
                                                            </div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="text-center font-bold text-[11px] mb-3 uppercase underline">GENERAL TERMS & CONDITIONS FOR TRANSFER (Page 3)</div>
                                                            
                                                            <div className="space-y-3 text-justify text-gray-700">
                                                                {/* Rates Continued */}
                                                                <table className="w-full border-collapse border border-gray-300 text-[7.5pt]">
                                                                    <thead>
                                                                        <tr className="bg-gray-100">
                                                                            <th className="border border-gray-300 p-1 text-left">Sector Group / Sectors (Continued)</th>
                                                                            <th className="border border-gray-300 p-1 text-right w-28">Rate (Rs./Sqm.)</th>
                                                                        </tr>
                                                                    </thead>
                                                                    <tbody>
                                                                        <tr><td className="border border-gray-300 p-1">36, 39, 50, 51, 52</td><td className="border border-gray-300 p-1 text-right font-semibold">2439.94</td></tr>
                                                                        <tr><td className="border border-gray-300 p-1">27, 34, 49, 61, 62, 63, 66, 71, 72, 92</td><td className="border border-gray-300 p-1 text-right font-semibold">1700.74</td></tr>
                                                                        <tr><td className="border border-gray-300 p-1">137, 143B, 168</td><td className="border border-gray-300 p-1 text-right font-semibold">1238.48</td></tr>
                                                                        <tr><td className="border border-gray-300 p-1">145</td><td className="border border-gray-300 p-1 text-right font-semibold">1018.13</td></tr>
                                                                    </tbody>
                                                                </table>

                                                                <div className="bg-purple-50 p-2.5 rounded border border-purple-100 mt-2 text-[7.5pt]">
                                                                    <strong>GPA Transfer Rate Rules:</strong> Transfer within the blood relatives of registered GPA holder: 1.5 times of normal transfer charges. Other than blood relatives of registered GPA holder: 2 times of normal transfer charges shall be applicable. In case General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in Hindi and one in English) inviting that no claim against the property exists other than the respective Regd. GPA holder/Transferee is required.
                                                                </div>

                                                                <div className="font-bold text-gray-900 uppercase text-[8pt] mt-3">ii. GROUP HOUSING</div>
                                                                <p className="text-[7.5pt]">Transfer within the blood relatives of registered GPA holder: 1.5 times of normal transfer charges. Other than blood relatives of registered GPA holder: 2 times of normal transfer charges shall be applicable. GPA registered without agreement to sell requires a public notice in two National Dailies (one in Hindi and one in English).</p>

                                                                <div className="font-bold text-gray-900 uppercase text-[8pt] mt-2">iii. HOUSING</div>
                                                                <p className="text-[7.5pt]">Transfer within the blood relatives of registered GPA holder: 1.5 times of normal transfer charges. Other than blood relatives of registered GPA holder: 2 times of normal transfer charges shall be applicable. General Power of Attorney registered without agreement to sell requires public notice in two National Dailies.</p>

                                                                <div className="font-bold text-gray-900 uppercase text-[8pt] mt-2">iv. INDUSTRIAL PLOTS/ SHEDS</div>
                                                                <p className="text-[7.5pt]">Transfer within the blood relatives of registered GPA holder: 1.5 times of normal transfer charges. Other than blood relatives of registered GPA holder: 2 times of normal transfer charges shall be applicable. General Power of Attorney registered without agreement to sell requires public notice in two National Dailies.</p>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 3</div>
                                                </div>

                                                {/* PAGE 4: Commercial GPA Rules (Conditional Placeholder) */}
                                                <div className={`paper-page print-break bg-white p-10 font-sans relative text-[8pt] leading-relaxed flex flex-col justify-between min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-purple-200' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-4 max-w-md select-none">
                                                            <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto text-2xl border border-purple-100">
                                                                <i className="fa-solid fa-key"></i>
                                                            </div>
                                                            <h3 className="text-sm font-bold text-slate-800">Page 4: Commercial GPA Conditions</h3>
                                                            <p className="text-[10px] text-slate-500 leading-normal">
                                                                This instruction page details GPA conditions for Commercial property transfers. It is hidden from printing because <strong>Submit via GPA Holder</strong> is disabled.
                                                            </p>
                                                            <div className="text-[8px] text-purple-600 font-bold bg-purple-50 px-2.5 py-1 rounded w-fit mx-auto border border-purple-100">
                                                                Page 4 (GPA Instruction) - Omitted from Print
                                                            </div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="text-center font-bold text-[11px] mb-3 uppercase underline">GENERAL TERMS & CONDITIONS FOR TRANSFER (Page 4)</div>
                                                            
                                                            <div className="space-y-2.5 text-justify text-gray-700">
                                                                <div className="font-bold text-gray-900 uppercase text-[8pt]">v. COMMERCIAL SHOPS/ PLOTS</div>
                                                                <p className="text-[7.5pt]">Commercial properties are allowed to be transferred on power of attorney basis with the following conditions:-</p>
                                                                
                                                                <ul className="list-disc pl-5 space-y-1.5 text-[7.5pt]">
                                                                    <li>Transfer application received on the basis of certified copy of Registered power of attorney only shall be entertained.</li>
                                                                    <li>It shall be the sole responsibility of the intending transferee to ensure the authenticity and validity of such power of attorney.</li>
                                                                    <li>The power of attorney holder shall be required to submit an affidavit on the prescribed performa in support of authenticity and validity of power of attorney. The intending purchaser shall also submit an indemnity bond on the prescribed performa in support thereof.</li>
                                                                    <li>In addition, the original allotment letter/possession certificate/legal documents i.e. licence agreement/HPTA/lease deed/transfer deed for the property under transfer, shall also be required alongwith the transfer application.</li>
                                                                    <li>These documents shall be returned to the transferee alongwith the permission for transfer, if granted, under registered post or in person.</li>
                                                                    <li>Certified copy of an agreement to sell duly registered or notarised shall also be required in favour of the intending transferee.</li>
                                                                    <li>Transfer charges shall be one and half times (1.50) of the normal transfer charges for the first agreement to sell. Thereafter Transfer charges shall be increased @ 50% of the normal transfer charges for every subsequent agreement to sell.</li>
                                                                    <li>On grant of transfer permission transferee shall be required to execute lease deed/transfer deed as the case may be.</li>
                                                                    <li>Transfer on power of attorney basis will be subject to directions received from Govt. of U.P. from time to time. In case of general power of attorney is registered without agreement to sell, then a public notice in two national dailies (one in Hindi and one in English) inviting that no claim exists other than respective Regd. GPA holder/Transferee is required.</li>
                                                                </ul>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 4</div>
                                                </div>

                                                {/* PAGE 5: Institutional & Requirements for Allottee */}
                                                <div className="paper-page print-break bg-white p-10 font-sans relative text-[8pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[11px] mb-3 uppercase underline">GENERAL TERMS & CONDITIONS & ENCLOSURES (Page 5)</div>
                                                        
                                                        <div className="space-y-3 text-justify text-gray-700">
                                                            <div className="font-bold text-gray-900 uppercase text-[8pt]">vi. INSTITUTIONAL</div>
                                                            <p className="text-[7.5pt]">
                                                                Transfer within the blood relatives of registered GPA holder: 1.5 times of normal transfer charges. Other than blood relatives of registered GPA holder: 2 times of normal transfer charges shall be applicable. In case General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies is required.
                                                            </p>

                                                            <div className="border-t border-gray-300 pt-2 mt-2">
                                                                <div className="font-bold text-gray-900 text-[8.5pt] mb-2 uppercase">Requirements/Enclosures for transfer of plot/premises on request of the allottee:</div>
                                                                <ol className="list-decimal pl-5 space-y-1 text-[7.5pt]">
                                                                    <li>Payment deposit challan (in original) for deposit of processing fees of Rs. 1000/- and transfer charges &apos;as applicable&apos; in one of the authorised banks. (Processing Fee Challan: <strong>[<Var name="processingFeeChallanNo">{p.processingFeeChallanNo || '___________'}</Var>]</strong> dt. <strong>[<Var name="processingFeeDate">{formatDate(p.processingFeeDate)}</Var>]</strong>)</li>
                                                                    <li>Joint affidavit by the transferor and transferee in the prescribed format on non-judicial stamp paper of Rs. 20/- duly notarised.</li>
                                                                    <li>Affidavit by the transferee in the prescribed format about his satisfaction towards non encumbrance on the plot/premises.</li>
                                                                    <li>No dues Certificate issued by the concerned Account Officer.</li>
                                                                    <li>No dues certificate issued by the Project Engineer (Jal).</li>
                                                                    <li>Copy of the project report if transfer permission is for Industrial/Institutional plot/premises.</li>
                                                                    <li>No Objection Certificate issued by GM (DIC) Noida and No Dues Certificate issued by UPPCL (Power Corporation) shall also be required for transfer of industrial plot/premises.</li>
                                                                    <li>Copy of Occupancy Certificate/Completion Certificate issued by Building Cell for transfer of Residential plots/Functional Certificate for transfer of Industrial/ Commercial/Institutional plot/premises. OR Copy of the extension letter valid upto the date of transfer.</li>
                                                                    <li>If the plot/premises is mortgaged then a No Objection Certificate for permitting transfer to be issued by the financial institution shall also be required.</li>
                                                                    <li>No Objection Certificate from the respective cooperative society for transfer of residential plots allotted to the members of cooperative societies.</li>
                                                                    <li>No Objection Certificate from AWHO, AFNHB, Builders, Co-operative Societies for the flats/ houses allotted by the respective institution.</li>
                                                                </ol>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 5</div>
                                                </div>

                                                {/* PAGE 6: Requirements for GPA & Corporate Checklists */}
                                                <div className="paper-page print-break bg-white p-10 font-sans relative text-[8pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[11px] mb-3 uppercase underline">ENCLOSURES & PRESCRIBED CATEGORIES (Page 6)</div>
                                                        
                                                        <div className="space-y-3 text-justify text-gray-700">
                                                            <div className="bg-purple-50/50 p-2.5 rounded border border-purple-100">
                                                                <div className="font-bold text-purple-900 text-[8pt] mb-1">Requirements/Enclosures for transfer of plot/premises on request of the General Power of Attorney of the allottee:</div>
                                                                <ul className="list-disc pl-5 space-y-0.5 text-[7.5pt] text-purple-800">
                                                                    <li>Certified copy of the General Power of Attorney given by the allottee for transfer of the plot/premises.</li>
                                                                    <li>An indemnity bond by the transferee in the prescribed format (Rs. 100/- Stamp Paper).</li>
                                                                    <li>An affidavit by the transferee about legal validity of the GPA on the prescribed format (Rs. 10/- Stamp Paper).</li>
                                                                    <li>A copy of the registered agreement to sell in favour of the transferee.</li>
                                                                    <li>In absence of registered agreement to sell, a public notice, as per the language provided by the Authority, in two national dailies.</li>
                                                                </ul>
                                                            </div>

                                                            <div className="text-[7.5pt] border-t border-gray-200 pt-2">
                                                                <div className="font-bold text-gray-900 mb-1">If the transferor/transferee is a partnership firm/Pvt. Ltd. Co./Ltd. Co./Regd. Society/Trust:</div>
                                                                <ul className="list-alpha pl-5 space-y-0.5">
                                                                    <li>a) A certified copy of the partnership deed of transferee, copy of form A & B (Registrar of firms),</li>
                                                                    <li>b) Authority letter or Power of Attorney to purchase if not signed by all partners.</li>
                                                                    <li>c) Authority letter or Power of Attorney of the transferor firm if not signed by all partners.</li>
                                                                    <li>d) Certified copy of board resolution of transferor to sell and transferee to purchase in favour of authorized signatory.</li>
                                                                    <li>e) Memorandum and Articles of Association of company / Memorandum of society / trust.</li>
                                                                    <li>f) List of shareholders & list of directors certified by CA / list of executive members / list of trustees.</li>
                                                                    <li>g) Attested photograph and signatures of all directors/society executive members and trustees.</li>
                                                                </ul>
                                                            </div>

                                                            <div className="text-[7.5pt] border-t border-gray-200 pt-2">
                                                                <div className="font-bold text-gray-900 mb-1">The following shall fall into the prescribed categories:</div>
                                                                <ol className="list-decimal pl-5 space-y-0.5">
                                                                    <li>1. Bonafide Sole Proprietor/Partner(s)/Director(s)/Regular Employees of functional units on land leased by NOIDA (Category: NOIDA-IND)</li>
                                                                    <li>2. Bonafide Sole Proprietor/Partner(s)/Director(s) of functional commercial establishments (Category: NOIDA-COMM)</li>
                                                                    <li>3. Bonafide Managing Trustees/Regular Employees of functional institutions (Category: NOIDA-INSTT)</li>
                                                                    <li>4. Bonafide eligible villager who was a KHATEDAR/SAHKHATEDAR of acquired land and received compensation without pending litigation (Category: NOIDA-VIL)</li>
                                                                    <li>5. Regular employees of the Authority (Category: NOIDA-EMP)</li>
                                                                </ol>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 6</div>
                                                </div>

                                                {/* PAGE 7: Joint Affidavit (Page 1) */}
                                                <div className="paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="border-2 border-dashed border-gray-300 rounded-lg p-2.5 text-center mb-6 bg-gray-50/50">
                                                            <div className="text-[10pt] font-sans font-bold text-gray-500 uppercase tracking-widest">Non-Judicial Stamp Paper of Rs. 20/-</div>
                                                            <div className="text-[7pt] text-gray-400 mt-0.5">Joint Affidavit of Transferor & Transferee - Page 1</div>
                                                        </div>

                                                        <div className="text-center font-bold text-[11pt] tracking-tight uppercase mb-4 text-blue-900">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>
                                                        
                                                        {/* Deponent text block */}
                                                        <div className="space-y-3 text-justify">
                                                            {!p.isGpa ? (
                                                                <div className="leading-normal">
                                                                    I/We/M/s <strong>[<Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var>]</strong>
                                                                    {p.transferor1Age && <> aged <strong>[<Var name="transferor1Age">{p.transferor1Age}</Var>]</strong> years, </>}
                                                                    {' '}<strong>[<Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var>]</strong>
                                                                    {' '}R/o <strong>[<Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var>]</strong>
                                                                    {p.hasJointTransferor && p.transferor2Name && <> and Joint Transferor: <strong>[<Var name="transferor2Name">{p.transferor2Name}</Var>]</strong> {p.transferor2Age && <> aged <strong>[<Var name="transferor2Age">{p.transferor2Age}</Var>]</strong> years, </>} <strong>[<Var name="transferor2Relation">{p.transferor2Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor2Father">{p.transferor2Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferor2Address">{p.transferor2Address || '__________________'}</Var>]</strong></>}
                                                                    {' '}transferor of Plot/Premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> Noida, measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> sq. mtrs.
                                                                </div>
                                                            ) : (
                                                                <div className="text-gray-400 line-through text-[8.5pt] select-none leading-none">
                                                                    I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor of Plot/Premises No. ________ Block ________ Sector ________ Noida, measuring ________ sq. mtrs. (Omitted - GPA is Active)
                                                                </div>
                                                            )}

                                                            {p.isGpa ? (
                                                                <div className="leading-normal bg-purple-50/50 p-2 border border-purple-100 rounded">
                                                                    I/We/M/s <strong>[<Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var>]</strong>
                                                                    {p.gpaHolderAge && <> aged <strong>[<Var name="gpaHolderAge">{p.gpaHolderAge}</Var>]</strong> years, </>}
                                                                    {' '}<strong>[<Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var>]</strong>
                                                                    {' '}R/o <strong>[<Var name="gpaHolderAddress">{p.gpaHolderAddress || '__________________'}</Var>]</strong>
                                                                    {' '}transferor of Plot/Premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> Noida, measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> sq. mtrs. on behalf of the allottee Shri/Smt./Km. <strong>[<Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var>]</strong> <strong>[<Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var>]</strong> as registered General Power of Attorney holder, GPA registered with Sub-Registrar/Tehsildar <strong>[<Var name="gpaOffice">{p.gpaOffice || '________'}</Var>]</strong> No. <strong>[<Var name="gpaRegNo">{p.gpaRegNo || '________'}</Var>]</strong> dated <strong>[<Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var>]</strong>.
                                                                </div>
                                                            ) : (
                                                                <div className="text-gray-400 line-through text-[8.5pt] select-none leading-none">
                                                                    I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor of Plot/Premises No. ________ Block ________ Sector ________ Noida, measuring ________ sq. mtrs. on behalf of the allottee Shri/Smt./Km. ______________________ S/o, W/o, D/o ______________________ R/o ______________________ as registered General Power of Attorney holder, GPA registered with Sub-Registrar/Tehsildar No. ______________________ dated ______________________ (Omitted - GPA is Inactive)
                                                                </div>
                                                            )}

                                                            <div className="text-center font-bold my-1">AND</div>

                                                            <div className="leading-normal">
                                                                I/We/M/s <strong>[<Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var>]</strong>
                                                                {p.transferee1Age && <> aged <strong>[<Var name="transferee1Age">{p.transferee1Age}</Var>]</strong> years, </>}
                                                                {' '}<strong>[<Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var>]</strong>
                                                                {' '}R/o <strong>[<Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var>]</strong>
                                                                {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and Transferee 2: <strong>[<Var name="transferee2Name">{p.transferee2Name}</Var>]</strong> {p.transferee2Age && <> aged <strong>[<Var name="transferee2Age">{p.transferee2Age}</Var>]</strong> years, </>} <strong>[<Var name="transferee2Relation">{p.transferee2Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee2Father">{p.transferee2Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferee2Address">{p.transferee2Address || '__________________'}</Var>]</strong></>}
                                                                {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and Transferee 3: <strong>[<Var name="transferee3Name">{p.transferee3Name}</Var>]</strong> {p.transferee3Age && <> aged <strong>[<Var name="transferee3Age">{p.transferee3Age}</Var>]</strong> years, </>} <strong>[<Var name="transferee3Relation">{p.transferee3Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee3Father">{p.transferee3Father || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferee3Address">{p.transferee3Address || '__________________'}</Var>]</strong></>}
                                                                {' '}transferee for the above stated plot/premises do hereby solemnly affirm and declare jointly on oath as under in respect of Plot/Premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> Noida, measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> sq. mtrs
                                                            </div>
                                                        </div>

                                                        {/* Affidavit Points 1-6 */}
                                                        <ol className="list-decimal pl-5 mt-4 space-y-2 text-justify">
                                                            <li>That the transferor and transferee are bonafide citizen of India and are competent to contract.</li>
                                                            <li>That the deponents understand that the said plot/premises is transferable on payment of transfer charges, as applicable, to the Authority.</li>
                                                            <li>That the deponents undertake to abide by the rules, regulations terms and conditions and directions of the New Okhla Industrial Development Authority (NOIDA) as applicable from time to time.</li>
                                                            <li>That the transfer of rights, interest, payments, assets, liabilities, title etc. respect to the property are limited to the extent vested in the Transferor.</li>
                                                            <li>(i) That the dues in respect of above said plot/premises have been cleared and No Dues Certificate, issued by the concerned Accounts Officer is enclosed. <br/>
                                                            (ii) That the dues in respect of usages charges/no usages charges, as applicable, have been cleared and a no dues certificate issued by the Account Officer (Jal) has been enclosed.</li>
                                                            <li>That the transferor has established the unit/enterprise on the above stated premises and a copy of the functional certificate issued by the Authority is enclosed. (applicable for transfer of Industrial/Institutional/Commercial plot/premises)</li>
                                                        </ol>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 7</div>
                                                </div>

                                                {/* PAGE 8: Joint Affidavit (Page 2) */}
                                                <div className="paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[10pt] uppercase mb-4 text-gray-400">Joint Affidavit - Page 2</div>
                                                        
                                                        <div className="space-y-3 text-justify">
                                                            <p className="leading-relaxed pl-5">
                                                                That the transferor has obtained Occupancy certificate/completion certification issued by the Authority (applicable for transfer of Residential plot/premises) <br/>
                                                                <strong>OR</strong> <br/>
                                                                That the transferor has obtained valid extension upto the date of transfer and a copy of the extension letter issued by the Authority is enclosed. (Not applicable for transfer of Group Housing/Housing).
                                                            </p>

                                                            <ol className="list-decimal pl-5 space-y-2 start-7">
                                                                <li className="list-item">That the above property has neither been mortgaged nor offered as collateral security to any institution and is free from all encumbrances.</li>
                                                                <li className="list-item">That the deponents have ensured that there is no unauthorized construction and/or use in the property.</li>
                                                                <li className="list-item">
                                                                    (i) The transferor, his/her spouse and/or dependent children and/or his/her/their Industrial/Commercial/Institutional unit established in NOIDA had not obtained any residential plot/premises (i.e. including the property for which this transfer application is being submitted) by way of direct allotment from the Authority and he/she/they, their spouse and/or dependent children and/or his/her/their Industrial/Commercial/ Institutional unit would not apply for allotment of any residential plot/premises under any allotment scheme of the Authority and not take possession of any residential plot/premises in any pending scheme(s) or any future scheme of the Authority but may acquire one or more residential plot/house/flat in NOIDA through transfer from open market. <br/>
                                                                    (ii) That the transferor his spouse/dependent children is/are not a member of any cooperative housing society nor will become member of any cooperative housing society operating in notified area of NOIDA. <br/>
                                                                    (iii) That the transferor understand(s) that in case of any breach of any to he terms and conditions, the Authority shall take action as it may deem fit. <br/>
                                                                    (iv) That the transferor is applying for transfer of the plot/premises under the terms of allotment/Lease deed/Lease-cum-sale-deed/transfer deed executed on <strong>[<Var name="leaseDate">{formatDate(p.leaseDate)}</Var>]</strong> (applicable for transfer of residential plot/flat/houses).
                                                                </li>
                                                                <li className="list-item">
                                                                    (i) That the transferee shall pay to the Authority all outstanding dues along with interest as applicable. <br/>
                                                                    (ii) That the outstanding premium/ lease rent /interest and all other dues against the plot/premises shall constitute the first charge against the plot/premises.
                                                                </li>
                                                                <li className="list-item">
                                                                    (i) That the deponents understands that the receipt of the transfer application and charges by the Authority are purely provisional and does not provide/constitute any right to either party for claiming grant of Transfer Permission by the Authority. The Authority reserves the right to decide the case on merit and is free to reject a request for transfer without assigning any reason.
                                                                </li>
                                                            </ol>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 8</div>
                                                </div>

                                                {/* PAGE 9: Joint Affidavit (Page 3) */}
                                                <div className="paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[10pt] uppercase mb-4 text-gray-400">Joint Affidavit - Page 3</div>
                                                        
                                                        <ol className="list-decimal pl-5 space-y-2 text-justify start-11">
                                                            <li className="list-item">
                                                                (ii) In the event of such rejection the transfer charges deposited, if any, shall be refunded to the transferor. No interest, however, shall be payable on the deposits so made. <br/>
                                                                (iii) If transfer does not materialize due to withdrawal of the transfer application by mutual consent of the transferor and transferee then transfer charges will not be refunded/adjusted even if transfer application is withdrawn. In case of dispute between the transferor and transferee, permission for withdrawal of transfer application shall be granted with orders of the competent court. <br/>
                                                                (iv) The transferee shall not transfer his/her/their rights without prior approval of the Authority in writing which the Authority may refuse without assigning any reason or allow on such terms and conditions as it may deem fit. <br/>
                                                                (v) The transfer of plot/premises is an act between the transferor and transferee and as such any liens, claims, damages, compensation, adverse court orders etc. arising thereof subsequently would be the sole liability of transferee(s) and Noida would remain indemnified against the same.
                                                            </li>
                                                            <li className="list-item">
                                                                (i) That in the event of transfer being permitted by the Authority the deponents shall have to execute a transfer deed and thereafter shall be entitled to lease hold rights for the remaining period of 90 years from the date of execution of original legal documents or taking over possession of the plot/premises, whichever is earlier. <br/>
                                                                (ii) The transfer deed shall be executed within 90 days from the date of issue of transfer memorandum. The transfer deed must, inter alia, incorporate the various terms and conditions mentioned in the transfer memorandum. The final mutation will be made in the name of the transferee after receipt of the certified copy of the transfer deed and its acceptance by the Authority. This transfer deed shall be required to be submitted with the Authority within one month from the date of its execution. In case of failure to execute lease-Cum-Sale Deed/Transfer Deed (as the case may be) by the Transferee would invite payment of penalty as applicable from time to time. <br/>
                                                                (iii) The transferee shall be given one year for making the industrial unit/commercial establishment/institution functional from the date of issue of the transfer memorandum. The transferee of residential plot shall be required to obtain extension on payment of prescribed extension charges to raise construction/ obtain occupancy/completion certificate.
                                                            </li>
                                                            <li className="list-item">That the lease rent/ground rent of the subject property shall be revised and shall be payable as indicated by the Authority in transfer permission letter. The revised lease rent/ground rent may be enhanced after every 10 years from the date of execution of the original lease deed/legal documents subject to the condition that the same shall not exceed 50% of the lease/ground rent last thus fixed. (in case of commercial plot/shop lease rent shall not be revised, however, provision of enhancement as per terms of lease deed shall be applicable.</li>
                                                        </ol>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 9</div>
                                                </div>

                                                {/* PAGE 10: Joint Affidavit (Page 4) */}
                                                <div className="paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="text-center font-bold text-[10pt] uppercase mb-3 text-gray-400">Joint Affidavit - Page 4</div>
                                                        
                                                        <ol className="list-decimal pl-5 space-y-1.5 text-justify start-14 mb-4">
                                                            <li className="list-item">That the deponents understand that notwithstanding any request/instruction of either party the payment made by the either party shall be first adjusted towards the interest due and premium/cost of the property and thereafter the same shall be appropriated towards the annual lease/ground rent.</li>
                                                            <li className="list-item">That the transferee shall put the plot/premises in use exclusively for the authorized purpose and shall not use it for any purpose other than the allotted/leased.</li>
                                                            <li className="list-item">The lease rent/ground/rent of the aforesaid property shall be applicable as indicated in the transfer memorandum.</li>
                                                            <li className="list-item">The transferee shall put the commercial property/plot/shop in use for which it has been allotted.</li>
                                                            <li className="list-item">The deponents understand that the Chief Executive Officer of the Authority shall have every right to amend or after the terms and conditions as deemed fit from time to time and such amendments/modifications shall be final and binding on them.</li>
                                                            <li className="list-item">The transferor and transferee agree that in the event of transfer being obtained through misrepresentation/suppression or fact or in case of any breach/violation of terms and conditions of the brochure of the Scheme/ HPTA/Licence Agreement/Lease Deed/Transfer Deed and the terms and conditions stated here is this affidavit, the Authority shall be free to take action as deemed fit and exercise its right for cancellation of allotment/lease hold rights including forfeiture of the deposited amount.</li>
                                                            <li className="list-item">The deponent shall be bound by the provisions of U.P. Industrial Area Development Act, 1976 (U.P. Act No. 6 of 1976) and the rules and regulations made and/or directions issued there under and enacted/amended from time to time.</li>
                                                            <li className="list-item">The deponent undertakes that the dispute, if any, with regards to approval of transfer of property and or otherwise shall be subject to the Courts Jurisdiction of High Court Allahabad/Civil Court Ghaziabad/ Gautam Budh Nagar.</li>
                                                        </ol>

                                                        <div className="flex justify-between font-bold text-center mt-6 text-[9pt]">
                                                            <div className="w-40 border-t border-black pt-1">DEPONENT<br/>(TRANSFEROR)</div>
                                                            <div className="w-40 border-t border-black pt-1">DEPONENT<br/>(TRANSFEREE)</div>
                                                        </div>

                                                        {/* Verification */}
                                                        <div className="mt-5 border-t border-gray-300 pt-3">
                                                            <div className="text-center font-bold underline mb-1 uppercase text-[10pt]">VERIFICATION</div>
                                                            <p className="text-justify leading-normal text-[9pt]">
                                                                We the above deponents do hereby verify that the contents and declarations made in the affidavit are true to the best of our respective knowledge and belief and nothing has been concealed therein.
                                                            </p>
                                                            <div className="flex justify-between font-bold text-center mt-8 text-[9pt]">
                                                                <div className="w-40 border-t border-black pt-1">DEPONENT<br/>(TRANSFEROR)</div>
                                                                <div className="w-40 border-t border-black pt-1">DEPONENT<br/>(TRANSFEREE)</div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 10</div>
                                                </div>

                                                {/* PAGE 11: Transferee's GPA Affidavit (Rs. 10 Stamp) */}
                                                <div className={`paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-purple-200' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-4 max-w-md select-none">
                                                            <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto text-2xl border border-purple-100">
                                                                <i className="fa-solid fa-stamp"></i>
                                                            </div>
                                                            <h3 className="text-sm font-bold text-slate-800">Page 11: Transferee GPA Affidavit</h3>
                                                            <p className="text-[10px] text-slate-500 leading-normal">
                                                                This affidavit confirms the validity of the Transferor&apos;s GPA. It is hidden from printing because <strong>Submit via GPA Holder</strong> is disabled.
                                                            </p>
                                                            <div className="text-[8px] text-purple-600 font-bold bg-purple-50 px-2.5 py-1 rounded w-fit mx-auto border border-purple-100">
                                                                Page 11 (GPA Affidavit) - Omitted from Print
                                                            </div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-2 text-center mb-4 bg-gray-50/50">
                                                                <div className="text-[9pt] font-sans font-bold text-gray-500 uppercase tracking-widest">Non-Judicial Stamp Paper of Rs. 10/-</div>
                                                                <div className="text-[7pt] text-gray-400 mt-0.5">GPA Validity Affidavit - Duly Notarized</div>
                                                            </div>

                                                            <div className="text-center font-bold text-[8.5pt] uppercase leading-tight mb-4 text-gray-600 max-w-xl mx-auto border border-gray-200 p-1.5 bg-gray-50/50 rounded">
                                                                TO BE SUBMITTED BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY
                                                            </div>

                                                            <p className="mb-3 text-justify">
                                                                I, <strong>[<Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var>]</strong>
                                                                {p.transferee1Age && <> aged <strong>[<Var name="transferee1Age">{p.transferee1Age}</Var>]</strong> years, </>}
                                                                {' '}<strong>[<Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var>]</strong>
                                                                {' '}R/o <strong>[<Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var>]</strong>, hereby solemnly affirm and state on oath as under:-
                                                            </p>

                                                            <ol className="list-decimal pl-5 space-y-2 text-justify">
                                                                <li>That deponent is transferee of plot/premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong>, NOIDA measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm.</li>
                                                                <li>That Sh./Smt./Km. <strong>[<Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var>]</strong> <strong>[<Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var>]</strong> is the allottee of Plot/ premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector- <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong>, NOIDA measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm.</li>
                                                                <li>That Sh./Smt./Km. <strong>[<Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var>]</strong> <strong>[<Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="gpaHolderAddress">{p.gpaHolderAddress || '__________________'}</Var>]</strong> is power of Attorney holder of the allottee and submitting application for transfer of the plot/premises on behalf of the allottee. General Power of Attorney was executed on <strong>[<Var name="gpaDate">{formatDate(p.gpaDate)}</Var>]</strong> and registered with Sub-Registrar/Tehsildar <strong>[<Var name="gpaOffice">{p.gpaOffice || '________'}</Var>]</strong> on <strong>[<Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var>]</strong> at Reg No. <strong>[<Var name="gpaRegNo">{p.gpaRegNo || '________'}</Var>]</strong> for plot/premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm.</li>
                                                                <li>That the said GPA has not been revoked so far.</li>
                                                                <li>That the deponent has satisfied himself about the authenticity and legal validity of the above stated Power of Attorney and the allottee of the plot/ premises as stated at Sl. No. 2 above is alive on this day.</li>
                                                            </ol>

                                                            <div className="flex justify-end mt-8">
                                                                <div className="w-40 text-center border-t border-black pt-1 font-bold">DEPONENT</div>
                                                            </div>

                                                            <div className="mt-4 border-t border-gray-200 pt-3">
                                                                <div className="font-bold text-center underline mb-1">VERIFICATION</div>
                                                                <p className="text-justify leading-normal text-[9pt]">
                                                                    I, the above named deponent do hereby verify that the above contents from para 1 to 5 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.
                                                                </p>
                                                                <div className="flex justify-end mt-8">
                                                                    <div className="w-40 text-center border-t border-black pt-1 font-bold">DEPONENT</div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 11</div>
                                                </div>

                                                {/* PAGE 12: Transferee's Standard Affidavit (Rs. 10 Stamp) */}
                                                <div className="paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px]">
                                                    <div>
                                                        <div className="border-2 border-dashed border-gray-300 rounded-lg p-2 text-center mb-4 bg-gray-50/50">
                                                            <div className="text-[9pt] font-sans font-bold text-gray-500 uppercase tracking-widest">Non-Judicial Stamp Paper of Rs. 10/-</div>
                                                            <div className="text-[7pt] text-gray-400 mt-0.5">Transferee Undertaking Affidavit - Duly Notarized</div>
                                                        </div>

                                                        <div className="text-center font-bold text-[8.5pt] uppercase leading-tight mb-4 text-gray-600 max-w-xl mx-auto border border-gray-200 p-1.5 bg-gray-50/50 rounded">
                                                            TO BE SUBMITTED BY TRANSFEREE
                                                        </div>

                                                        <p className="mb-3 text-justify">
                                                            I, <strong>[<Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var>]</strong>
                                                            {p.transferee1Age && <> aged <strong>[<Var name="transferee1Age">{p.transferee1Age}</Var>]</strong> years, </>}
                                                            {' '}<strong>[<Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var>]</strong>
                                                            {' '}R/o <strong>[<Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var>]</strong>, hereby solemnly affirm and state on oath as under:-
                                                        </p>

                                                        <ol className="list-decimal pl-5 space-y-3 text-justify">
                                                            <li>That the deponent is transferee of plot/premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong>, NOIDA measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm.</li>
                                                            <li>That Sh./Smt./Km. <strong>[<Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var>]</strong> <strong>[<Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var>]</strong> is the allottee of Plot/ premises No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector- <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong>, NOIDA measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm.</li>
                                                            <li>That the deponent has satisfied himself that the said plot/premises are without any encumbrance.</li>
                                                            <li>That the deponent has received/shall receive from the transferor all original documents such as allotment letter, possession letter, lease deed, transfer memorandum, transfer deed, no dues certificate, extension letter/occupancy/completion certificate/functional certification, payment deposit challans, etc. pertaining to the above stated plot/premises.</li>
                                                        </ol>

                                                        <div className="flex justify-end mt-8">
                                                            <div className="w-40 text-center border-t border-black pt-1 font-bold">DEPONENT</div>
                                                        </div>

                                                        <div className="mt-4 border-t border-gray-200 pt-3">
                                                            <div className="font-bold text-center underline mb-1">VERIFICATION</div>
                                                            <p className="text-justify leading-normal text-[9pt]">
                                                                I, the above named deponent do hereby verify that the above contents from para 1 to 4 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.
                                                            </p>
                                                            <div className="flex justify-end mt-8">
                                                                <div className="w-40 text-center border-t border-black pt-1 font-bold">DEPONENT</div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 12</div>
                                                </div>

                                                {/* PAGE 13: Transferee's Indemnity Bond Page 1 (Rs. 100 Stamp) */}
                                                <div className={`paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-purple-200' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-4 max-w-md select-none">
                                                            <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto text-2xl border border-purple-100">
                                                                <i className="fa-solid fa-file-shield"></i>
                                                            </div>
                                                            <h3 className="text-sm font-bold text-slate-800">Page 13: Transferee Indemnity Bond</h3>
                                                            <p className="text-[10px] text-slate-500 leading-normal">
                                                                This deed indemnifies the Authority against claims for transfers via GPA. It is hidden from printing because <strong>Submit via GPA Holder</strong> is disabled.
                                                            </p>
                                                            <div className="text-[8px] text-purple-600 font-bold bg-purple-50 px-2.5 py-1 rounded w-fit mx-auto border border-purple-100">
                                                                Page 13 (GPA Indemnity) - Omitted from Print
                                                            </div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-2 text-center mb-4 bg-gray-50/50">
                                                                <div className="text-[9pt] font-sans font-bold text-gray-500 uppercase tracking-widest">Non-Judicial Stamp Paper of Rs. 100/-</div>
                                                                <div className="text-[7pt] text-gray-400 mt-0.5">Transferee Indemnity Bond - Duly Notarized</div>
                                                            </div>

                                                            <div className="text-center font-bold text-[8.5pt] uppercase leading-tight mb-4 text-gray-600 max-w-xl mx-auto border border-gray-200 p-1.5 bg-gray-50/50 rounded">
                                                                INDEMNITY BOND BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY
                                                            </div>

                                                            <p className="mb-3 text-justify">
                                                                This Indemnity Bond is executed on this <strong>[<Var name="dated">{formatDate(p.dated)}</Var>]</strong> by Shri/Smt./Km. <strong>[<Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var>]</strong>
                                                                {p.transferee1Age && <> aged <strong>[<Var name="transferee1Age">{p.transferee1Age}</Var>]</strong> years, </>}
                                                                {' '}<strong>[<Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var>]</strong>
                                                                {' '}R/o <strong>[<Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var>]</strong> (transferee) hereinafter referred as &apos;EXECUTANT&apos; in favour of New Okhla Industrial Development Authority hereinafter referred to as &apos;AUTHORITY&apos;.
                                                            </p>

                                                            <p className="mb-3 text-justify">
                                                                Whereas Shri/Smt./Km. <strong>[<Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var>]</strong> <strong>[<Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="gpaHolderAddress">{p.gpaHolderAddress || '__________________'}</Var>]</strong> on behalf of the allottee of commercial plot/ shop No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sq.Mtrs. NOIDA holds the power of attorney (hereinafter called power of attorney) in respect of Plot/Shop No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong> measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm. NOIDA and being bounded as under:-
                                                            </p>

                                                            {/* Boundaries list */}
                                                            <div className="grid grid-cols-2 gap-2 border border-gray-300 p-2 rounded bg-gray-50/50 text-[8pt] mb-3">
                                                                <div><strong>ON THE NORTH BY:</strong> <strong>[<Var name="northBoundary">{p.northBoundary || '_________________'}</Var>]</strong></div>
                                                                <div><strong>ON THE SOUTH BY:</strong> <strong>[<Var name="southBoundary">{p.southBoundary || '_________________'}</Var>]</strong></div>
                                                                <div><strong>ON THE EAST BY:</strong> <strong>[<Var name="eastBoundary">{p.eastBoundary || '_________________'}</Var>]</strong></div>
                                                                <div><strong>ON THE WEST BY:</strong> <strong>[<Var name="westBoundary">{p.westBoundary || '_________________'}</Var>]</strong></div>
                                                            </div>

                                                            <p className="mb-3 text-justify">
                                                                By virtue of the powers conferred upon Shri/Smt./Km. <strong>[<Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var>]</strong> <strong>[<Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var>]</strong> Shri <strong>[<Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var>]</strong> R/o <strong>[<Var name="gpaHolderAddress">{p.gpaHolderAddress || '__________________'}</Var>]</strong> vide the attorney dated <strong>[<Var name="gpaDate">{formatDate(p.gpaDate)}</Var>]</strong> duly registered with Sub-Registrar on <strong>[<Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var>]</strong> at Reg No. <strong>[<Var name="gpaRegNo">{p.gpaRegNo || '________'}</Var>]</strong> (certified copy enclosed). The executant is getting commercial plot/shop No. <strong>[<Var name="plotNo">{p.plotNo || '________'}</Var>]</strong> Block <strong>[<Var name="block">{p.block || '________'}</Var>]</strong> Sector <strong>[<Var name="sector">{p.sector || '________'}</Var>]</strong>, NOIDA measuring <strong>[<Var name="area">{p.area || '________'}</Var>]</strong> Sqm. transferred in his name.
                                                            </p>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 13</div>
                                                </div>

                                                {/* PAGE 14: Transferee's Indemnity Bond Page 2 */}
                                                <div className={`paper-page print-break bg-white p-12 font-serif relative text-[9.5pt] leading-relaxed flex flex-col justify-between min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-purple-200' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-4 max-w-md select-none">
                                                            <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mx-auto text-2xl border border-purple-100">
                                                                <i className="fa-solid fa-file-shield"></i>
                                                            </div>
                                                            <h3 className="text-sm font-bold text-slate-800">Page 14: Transferee Indemnity Bond (Page 2)</h3>
                                                            <p className="text-[10px] text-slate-500 leading-normal">
                                                                This page contains execute signatures and witnesses for the Indemnity Bond. It is hidden from printing because <strong>Submit via GPA Holder</strong> is disabled.
                                                            </p>
                                                            <div className="text-[8px] text-purple-600 font-bold bg-purple-50 px-2.5 py-1 rounded w-fit mx-auto border border-purple-100">
                                                                Page 14 (GPA Indemnity) - Omitted from Print
                                                            </div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="text-center font-bold text-[10pt] uppercase mb-4 text-gray-400">Transferee Indemnity Bond - Page 2</div>
                                                            
                                                            <div className="space-y-3 text-justify">
                                                                <p>The executant is satisfied that as per the above documents the power of attorney holder is totally competent and legally authorized to effect the transfer/sale of the above mentioned property and to do all acts and execute all documents which are necessary for transfer/sale of the said property on behalf of the present allottee.</p>
                                                                <p>And whereas the Authority shall consider the transfer in favour of the executant provided the executant indemnifies the Authority against all losses, damages, inconvenience, cost and or litigation which may be caused because of such permission of transfer by Authority.</p>
                                                                <p>Now the (transferee) executant in the event of grant of permission by the Authority for sale/transfer of the above said property has agreed to indemnify the Authority against any claim/damage, cost, loss, inconvenience, litigation arising by the grant of permission for transfer of the above property. The executant also indemnifies the Authority for any liability in all forms that may be created by virtue of a court order and/or any other Competent Authority.</p>
                                                                <p>By this deed the executant shall also be totally responsible for other costs, damages, legal proceedings and any other loss to the Authority on account of above property and shall ensure to meet all the liabilities arising or which may arise by grant of permission to transfer and shall discharge the same from his own resources.</p>
                                                                <p>This indemnity Bond is executed in presence of the following witnesses on the day and month first above mentioned.</p>
                                                            </div>

                                                            <div className="flex justify-between items-start mt-8 text-[9pt]">
                                                                <div className="w-52 space-y-2">
                                                                    <div className="font-bold underline uppercase">WITNESSES:</div>
                                                                    <div>
                                                                        1. NAME: __________________________________<br/>
                                                                        ADDRESS: _______________________________<br/>
                                                                        ________________________________________
                                                                    </div>
                                                                    <div>
                                                                        2. NAME: __________________________________<br/>
                                                                        ADDRESS: _______________________________<br/>
                                                                        ________________________________________
                                                                    </div>
                                                                </div>
                                                                <div className="w-56 text-center pt-8 border-t border-black font-bold">
                                                                    SIGNATURE OF THE EXECUTANT<br/>
                                                                    (TRANSFEREE)
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[8pt] text-gray-400 font-bold">Page 14</div>
                                                </div>
                                            </>
                                        );
                                    })()}"""
    
    # Replace the existing activeTab === 'NOIDA_TRANSFER' rendering block in content
    # Find the starting index
    pattern_start = "activeTab === 'NOIDA_TRANSFER' && (() => {"
    idx_start = content.find(pattern_start)
    if idx_start == -1:
        print("Error: Could not find NOIDA_TRANSFER render block start!")
        return

    # Find the matching close brace block
    # Let's count open and close braces starting from idx_start
    brace_count = 0
    idx_end = -1
    for idx in range(idx_start, len(content)):
        char = content[idx]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                idx_end = idx + 1
                break

    # Verify we matched correctly by checking if it ends with "()}"
    snippet = content[idx_start:idx_end]
    if not snippet.strip().endswith("})()"):
        # Scan further just in case
        idx_end_final = content.find("})()}", idx_start)
        if idx_end_final != -1:
            idx_end = idx_end_final + 5
            snippet = content[idx_start:idx_end]
        else:
            print("Warning: Matching closing block not cleanly found. Snippet end: ", snippet[-20:])

    print(f"Replacing snippet of length {len(snippet)} bytes.")
    content = content[:idx_start] + noida_transfer_jsx + content[idx_end:]

    with open('test_script.jsx', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Submitting for compilation check...")
    if not compile_check():
        print("Reverting changes due to syntax errors...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open('test_script.jsx', 'w', encoding='utf-8') as f:
            f.write(content)
        compile_check()
    else:
        print("Completed update successfully!")

if __name__ == '__main__':
    main()
