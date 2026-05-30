#!/usr/bin/env python3
"""
Rewrite the NOIDA Transfer preview section to exactly match the government PDF format.
Replaces lines 6172-6923 in test_script.jsx with plain government-document styling.
"""

# The indentation prefix for all lines (36 spaces = 9 levels of 4-space indent)
P = "                                    "  # 36 spaces

new_jsx = r"""                                    {activeTab === 'NOIDA_TRANSFER' && (() => {
                                        const p = noidaTransferData;

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
                                                {/* ===== PAGE 1: Main Application Form ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-normal min-h-[1123px]">
                                                    <EsignBadge type="NOIDA_TRANSFER" />
                                                    <div className="text-center font-bold text-[13pt] uppercase tracking-wide mb-0">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>
                                                    <div className="text-center font-bold text-[11pt] uppercase underline decoration-2 mb-1">TRANSFER APPLICATION FORM (valid for six months)</div>
                                                    <div className="text-center text-[8pt] mb-4 leading-tight">FOR TRANSFER OF RESIDENTIAL PLOTS/GROUP HOUSING (flats and houses allotted by AWHO, AFNHB, Builders, Co-operative Societies) /HOUSING (Flats/Houses allotted by NOIDA)/ INDUSTRIAL PLOTS &amp; SHEDS/COMMERCIAL SHOPS &amp; PLOTS/ INSTITUTIONAL PLOTS</div>

                                                    <div className="flex justify-between text-[9pt] mb-1">
                                                        <div>Price Rs. 100/- (Rupees One Hundred Only)</div>
                                                        <div>Sl.No. <strong><Var name="slNo">{p.slNo || '_______________'}</Var></strong></div>
                                                    </div>
                                                    <div className="text-[9pt] mb-0">Date of issue by the authorized bank <strong><Var name="issueDate">{formatDate(p.issueDate)}</Var></strong></div>
                                                    <div className="text-[9pt] mb-3 pl-8">For downloaded forms date of deposit of Rs. 100/- in the authorized bank <strong><Var name="downloadDepositDate">{formatDate(p.downloadDepositDate)}</Var></strong></div>

                                                    <div className="mb-1 text-[10pt]">ASSTT. GENERAL MANAGER/Dy. GENERAL MANAGER/GENERAL MANAGER,</div>
                                                    <div className="mb-3 text-[10pt]">NOIDA.</div>

                                                    <p className="text-justify text-[9.5pt] leading-relaxed mb-3">
                                                        I/ We/ M/s (allottee) <strong><Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var></strong> (Prop.,Partner or name of the firm)
                                                        {p.transferor1Age && <> aged <strong><Var name="transferor1Age">{p.transferor1Age}</Var></strong> years,</>}
                                                        {' '}<strong><Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var></strong>
                                                        {' '}R/o, Regd. Office <strong><Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var></strong>
                                                        {p.hasJointTransferor && p.transferor2Name && <> and <strong><Var name="transferor2Name">{p.transferor2Name}</Var></strong> {p.transferor2Age && <> aged <strong><Var name="transferor2Age">{p.transferor2Age}</Var></strong> years,</>} <strong><Var name="transferor2Relation">{p.transferor2Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferor2Father">{p.transferor2Father || '__________________'}</Var></strong> R/o <strong><Var name="transferor2Address">{p.transferor2Address || '__________________'}</Var></strong></>}
                                                        {' '}is an allottee (here in shall be referred to as Transferor) of Plot/Flat or House on Group Housing Plot/Housing (Flat/ House/allotted by NOIDA)/ Industrial Plots &amp; Sheds/Commercial Shop &amp; Plots/Institutional Plot/ Premises No. <strong><Var name="plotNo">{p.plotNo || '________'}</Var></strong> Block <strong><Var name="block">{p.block || '________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '________'}</Var></strong> NOIDA having an area of <strong><Var name="area">{p.area || '________'}</Var></strong> Sq. Mtrs. want to transfer the above plot/premises in favour of Shri/Smt./M/s <strong><Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var></strong>
                                                        {p.transferee1Age && <> aged <strong><Var name="transferee1Age">{p.transferee1Age}</Var></strong> years,</>}
                                                        {' '}<strong><Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var></strong>
                                                        {' '}R/o, Regd Office <strong><Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var></strong>
                                                        {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and <strong><Var name="transferee2Name">{p.transferee2Name}</Var></strong> {p.transferee2Age && <> aged <strong><Var name="transferee2Age">{p.transferee2Age}</Var></strong> years,</>} <strong><Var name="transferee2Relation">{p.transferee2Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferee2Father">{p.transferee2Father || '__________________'}</Var></strong> R/o <strong><Var name="transferee2Address">{p.transferee2Address || '__________________'}</Var></strong></>}
                                                        {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and <strong><Var name="transferee3Name">{p.transferee3Name}</Var></strong> {p.transferee3Age && <> aged <strong><Var name="transferee3Age">{p.transferee3Age}</Var></strong> years,</>} <strong><Var name="transferee3Relation">{p.transferee3Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferee3Father">{p.transferee3Father || '__________________'}</Var></strong> R/o <strong><Var name="transferee3Address">{p.transferee3Address || '__________________'}</Var></strong></>}
                                                        {' '}(herein after shall be referred to as transferee).
                                                    </p>

                                                    {p.isGpa ? (
                                                        <p className="text-[9pt] text-justify leading-relaxed mb-3">
                                                            In case of transfer on the basis of authenticated GPA dt. <strong><Var name="gpaDate">{formatDate(p.gpaDate)}</Var></strong> through GPA of Holder Shri/Smt <strong><Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var></strong>
                                                            {p.gpaHolderAge && <> aged <strong><Var name="gpaHolderAge">{p.gpaHolderAge}</Var></strong> years,</>}
                                                            {' '}<strong><Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var></strong>,W/o,D/o Shri <strong><Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var></strong> Address <strong><Var name="gpaHolderAddress">{p.gpaHolderAddress || '____________________________________'}</Var></strong>
                                                        </p>
                                                    ) : (
                                                        <p className="text-[8.5pt] text-gray-400 line-through mb-3 select-none">In case of transfer on the basis of authenticated GPA dt.________ through GPA of Holder Shri/Smt________ S/o,W/o,D/o Shri ________ Address________________________________________ (Not Applicable)</p>
                                                    )}

                                                    <p className="text-justify text-[9.5pt] leading-relaxed mb-4">
                                                        The transferor(s) and the transferee(s) have read and understood the terms and conditions for transfer and undertake to abide by the same and accordingly apply for transfer of the above said <strong><Var name="useType">{p.useType || '________'}</Var></strong> plot/premises. In case of Industrial the premises will be used for <strong><Var name="projectName">{p.projectName || '__________________'}</Var></strong> Project which is at Sl No___________ of Annexure-A enclosed with Transfer Application form and for Commercial/Institutional the premises will be used as per terms of the original lease (Change of Project is not allowed).
                                                    </p>

                                                    <div className="flex justify-between text-center mb-6 mt-4">
                                                        <div className="w-48">
                                                            <div className="h-10"></div>
                                                            <div className="border-t border-black pt-1 text-[9pt]">Signature of the transferor(s)</div>
                                                            <div className="text-[8pt] italic">Above Signatures are attested</div>
                                                        </div>
                                                        <div className="w-48">
                                                            <div className="h-10"></div>
                                                            <div className="border-t border-black pt-1 text-[9pt]">Signature of transferee(s)</div>
                                                            <div className="text-[8pt] italic">Above signatures are attested</div>
                                                        </div>
                                                    </div>

                                                    <div className="grid grid-cols-2 gap-4 text-[8pt] mb-4">
                                                        <div className="border border-gray-400 p-2 h-20 flex flex-col justify-between">
                                                            <div>Signature, Name Designation and seal of Bank Officer attesting the signature of Transferor</div>
                                                            <div className="border-t border-dashed border-gray-400 pt-1 text-center italic text-gray-500">Official Stamp &amp; Signature</div>
                                                        </div>
                                                        <div className="border border-gray-400 p-2 h-20 flex flex-col justify-between">
                                                            <div>Signature, Name Designation and seal of Bank Officer attesting the signature of Transferee</div>
                                                            <div className="border-t border-dashed border-gray-400 pt-1 text-center italic text-gray-500">Official Stamp &amp; Signature</div>
                                                        </div>
                                                    </div>

                                                    <div className="flex gap-6 justify-center">
                                                        <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase">PHOTOGRAPH OF TRANSFEROR(S) DULY ATTESTED BY THE BANKER</div>
                                                        {p.isGpa && (
                                                            <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase">PHOTOGRAPH OF GPA HOLDER DULY ATTESTED BY THE BANKER</div>
                                                        )}
                                                        <div className="w-24 h-28 border border-black flex items-center justify-center text-center text-[7pt] p-1 uppercase">PHOTOGRAPH OF TRANSFEREE(S) DULY ATTESTED BY THE BANKER</div>
                                                    </div>

                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">1</div>
                                                </div>

                                                {/* ===== PAGE 2: Notes & Transfer Rates ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-normal min-h-[1123px]">
                                                    <div className="font-bold mb-2">Note :</div>
                                                    <div className="space-y-1 text-justify text-[8.5pt] mb-3">
                                                        <div><strong>(I)</strong> The term allottee includes transferee/sub lessee.</div>
                                                        <div><strong>(II)</strong> Signatures and Photograph of the Power of Attorney holder shall be required to be attested by the bankers, if the transfer application is submitted through General Power of Attorney Holder of the Allottee.</div>
                                                        <div><strong>(III)</strong> Group Housing means flats and houses allotted by AWHO, AFNHB, Builders and Co-operative Societies. Transfer of such flats/houses shall be considered alongwith transfer of garage, if it was allotted by the respective institution alongwith the flat/house.</div>
                                                        <div><strong>(IV)</strong> Transfer permission in favour of HUF shall not be allowed.</div>
                                                        <div><strong>(V)</strong> In case of industrial plot/premises transfer shall be permitted only after the unit has been declared functional.</div>
                                                        <div><strong>(VI)</strong> In case of industrial plot/premises project free from pollution &amp; environment hazards shall be considered. The project should not be on the banned list of directorate of Industries, UP or Development Commissioner, Small Scale Industries and Noida. A list of projects permitted in Noida is given as &apos;A&apos;, list of restricted projects is given as &apos;B&apos; and the list of negative projects is given as &apos;C&apos; on website of the Authority.</div>
                                                        <div><strong>(VII)</strong> The transfer charges for transfer Residential plot/flats/houses amongst the prescribed categories shall be 50% of the applicable transfer charges.</div>
                                                        <div><strong>(VIII)</strong> The transfer charges for transfer of industrial plots/sheds shall be 50% of the applicable transfer charges in cases of transfer/sale of the premises by financial institution under section 29 of SFC Act. The application has to be moved by the financial institution alongwith all NOC&apos;s required for making the transfer application.</div>
                                                    </div>

                                                    <div className="font-bold text-[8.5pt] mb-1"><strong>(IX)</strong> Prevailing Transfer charges</div>

                                                    <table className="w-full border-collapse border border-black text-[8pt] mb-2">
                                                        <thead>
                                                            <tr>
                                                                <th className="border border-black p-1 text-left" colSpan="2">For transfer application moved by the allottee (Rs. Per sq.mtr.)</th>
                                                                <th className="border border-black p-1 text-left w-[35%]">For transfer application moved by the Regd. GPA of the allottee</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr><td className="border border-black p-1 font-bold" colSpan="2">i. RESIDENTIAL PLOTS</td><td className="border border-black p-1 text-[7.5pt]" rowSpan="12">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td></tr>
                                                            <tr><td className="border border-black p-1">SECTOR</td><td className="border border-black p-1 text-right">RATE PER SQ MTR</td></tr>
                                                            <tr><td className="border border-black p-1">14A, 15A</td><td className="border border-black p-1 text-right">4375.00</td></tr>
                                                            <tr><td className="border border-black p-1">14,17,19,30,35,47,93</td><td className="border border-black p-1 text-right">2323.75</td></tr>
                                                            <tr><td className="border border-black p-1">11,12,15,20,21,22,23,25 TO 29,31,33,34,40,41,46,48,53,55,56,70,82,96 TO 100,122</td><td className="border border-black p-1 text-right">1619.75</td></tr>
                                                            <tr><td className="border border-black p-1">42,43,45,63A,104,107,110,118,119,120,121,128,129,130,131,133,134,135,143,151</td><td className="border border-black p-1 text-right">1179.50</td></tr>
                                                            <tr><td className="border border-black p-1">86,112,113,116,117</td><td className="border border-black p-1 text-right">986.00</td></tr>
                                                            <tr><td className="border border-black p-1">102,115,158,162, ETC</td><td className="border border-black p-1 text-right">905.00</td></tr>
                                                            <tr><td className="border border-black p-1">44 (A &amp; B BLOCK)</td><td className="border border-black p-1 text-right">4703.13</td></tr>
                                                            <tr><td className="border border-black p-1">44 (OTHER A&amp;B), 93A, 93B</td><td className="border border-black p-1 text-right">2498.03</td></tr>
                                                            <tr><td className="border border-black p-1">105, 108</td><td className="border border-black p-1 text-right">1741.23</td></tr>
                                                            <tr><td className="border border-black p-1">128,129,143B,154,168</td><td className="border border-black p-1 text-right">1267.96</td></tr>
                                                        </tbody>
                                                    </table>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">2</div>
                                                </div>

                                                {/* ===== PAGE 3: Rates continued + GPA rules ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-normal min-h-[1123px]">
                                                    <table className="w-full border-collapse border border-black text-[8pt] mb-3">
                                                        <tbody>
                                                            <tr><td className="border border-black p-1">144</td><td className="border border-black p-1 text-right">1326.94</td><td className="border border-black p-1 text-[7.5pt] w-[35%]" rowSpan="5">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td></tr>
                                                            <tr><td className="border border-black p-1">36,39,50,51,52</td><td className="border border-black p-1 text-right">2439.94</td></tr>
                                                            <tr><td className="border border-black p-1">27,34,49,61,62,63,66,71,72,92</td><td className="border border-black p-1 text-right">1700.74</td></tr>
                                                            <tr><td className="border border-black p-1">137,143B,168</td><td className="border border-black p-1 text-right">1238.48</td></tr>
                                                            <tr><td className="border border-black p-1">145</td><td className="border border-black p-1 text-right">1018.13</td></tr>
                                                        </tbody>
                                                    </table>

                                                    <table className="w-full border-collapse border border-black text-[8pt] mb-2">
                                                        <tbody>
                                                            <tr><td className="border border-black p-1 font-bold">ii. GROUP HOUSING</td><td className="border border-black p-1 text-[7.5pt] w-[50%]">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td></tr>
                                                            <tr><td className="border border-black p-1 font-bold">iii. HOUSING</td><td className="border border-black p-1 text-[7.5pt]">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td></tr>
                                                            <tr><td className="border border-black p-1 font-bold">iv. INDUSTRIAL PLOTS/ SHEDS</td><td className="border border-black p-1 text-[7.5pt]">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td></tr>
                                                        </tbody>
                                                    </table>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">3</div>
                                                </div>

                                                {/* ===== PAGE 4: Commercial GPA Rules ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-normal min-h-[1123px]">
                                                    <table className="w-full border-collapse border border-black text-[8pt] mb-3">
                                                        <tbody>
                                                            <tr>
                                                                <td className="border border-black p-1 font-bold align-top">v. COMMERCIAL SHOPS/ PLOTS</td>
                                                                <td className="border border-black p-2 text-[7.5pt] text-justify w-[50%]">
                                                                    <div className="mb-2">Commercial properties are allowed to be transferred on power of attorney basis with the following conditions:-</div>
                                                                    <div className="mb-2">Transfer application received on the basis of certified copy of Registered power of attorney only shall be entertained.</div>
                                                                    <div className="mb-2">It shall be the sole responsibility of intending transferee to ensure authenticity and validity of such power of attorney.</div>
                                                                    <div className="mb-2">The power of attorney holder shall be required to submit affidavit on the prescribed performa in support of authenticity and validity of power attorney. The intending purchaser shall also submit and indemnity bond on prescribed performa in support thereof.</div>
                                                                    <div className="mb-2">In addition original allotment letter/possession certificate/legal documents i.e. licence agreement/HPTA/lease deed/transfer deed for the property under transfer, shall also be required alongwith the transfer application.</div>
                                                                    <div className="mb-2">These documents shall be returned to transferee alongwith permission for transfer, if granted, under registered post or in person.</div>
                                                                    <div className="mb-2">Certified copy of an agreement to sell duly registered or notarised shall also be required in favour of intending transferee.</div>
                                                                    <div className="mb-2">Transfer charges shall be one and half times(1.50) of the normal transfer charges for first agreement to sell. Thereafter Transfer charges shall be increased @ 50% of the normal transfer charges for every subsequent agreement to sell.</div>
                                                                    <div className="mb-2">On grant of transfer permission transferee shall be required to execute lease deed/transfer deed as the case may be.</div>
                                                                    <div>Transfer on power of attorney basis will be subject to directions received from Govt. of U.P from time to time. In case of general power of attorney is registered without agreement to sell, then a public notice in two national dailies (one in Hindi and one in English) inviting that no claim against the concerned property exists other than respective Regd.GPA holder/ Transferee.</div>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">4</div>
                                                </div>

                                                {/* ===== PAGE 5: Institutional + Requirements ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-normal min-h-[1123px]">
                                                    <table className="w-full border-collapse border border-black text-[8pt] mb-4">
                                                        <tbody>
                                                            <tr>
                                                                <td className="border border-black p-1 font-bold align-top">vi. INSTITUTIONAL</td>
                                                                <td className="border border-black p-2 text-[7.5pt] w-[50%]">Transfer within the blood relatives of registered GPA holder, 1.5 times of normal transfer charges, other than blood relatives of registered GPA holder 2 times of normal transfer charges shall be applicable. In case of General Power of Attorney is registered without agreement to sell, then a public notice in two National Dailies (one in hindi and one in english) inviting that no claim against the concerned property exists other than respective Regd. GPA holder/Transferee.</td>
                                                            </tr>
                                                        </tbody>
                                                    </table>

                                                    <div className="font-bold text-[9pt] mb-2 underline">Requirements/Enclosures for transfer of plot/premises on request of the allottee</div>
                                                    <ol className="list-none pl-0 space-y-1.5 text-[8.5pt] text-justify mb-2">
                                                        <li>(1) Payment deposit challan (in original) for deposit of processing fees of Rs. 1000/- and transfer charges &apos;as applicable&apos; in one of the authorised banks.</li>
                                                        <li>(2) Joint affidavit by the transferor and transferee in the prescribed format on non-judicial stamp paper of Rs. 20/- duly notarised.</li>
                                                        <li>(3) Affidavit by the transferee in the prescribed format about his satisfaction towards non encumbrance on the plot/premises.</li>
                                                        <li>(4) No dues Certificate issued by the concerned Account Officer.</li>
                                                        <li>(5) No dues certificate issued by the Project Engineer (Jal).</li>
                                                        <li>(6) Copy of the project report if transfer permission is for Industrial/Institutional plot/premises.</li>
                                                        <li>(7) No Objection Certificate issued by GM (DIC) Noida and No Dues Certificate issued by UPPCL (Power Corporation) shall also be required for transfer of industrial plot/premises.</li>
                                                        <li>(8) Copy of Occupancy Certificate/Completion Certificate issued by Building Cell for transfer of Residential plots/Functional Certificate for transfer of Industrial/ Commercial/Institutional plot/premises.<br/>OR<br/>Copy of the extension letter valid upto the date of transfer issued by the concerned department(Other than Industrial Properties.).</li>
                                                        <li>(9) If the plot/premises is mortgaged then a No Objection Certificate for permitting transfer to be issued by the financial institution shall also be required.</li>
                                                        <li>(10) No Objection Certificate from the respective cooperative society for transfer of residential plots allotted to the members of cooperative societies.</li>
                                                        <li>(11) No Objection Certificate from AWHO, AFNHB, Builders, Co-operative Societies for the flats/ houses allotted by the respective institution.</li>
                                                    </ol>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">5</div>
                                                </div>

                                                {/* ===== PAGE 6: GPA Enclosures + Corporate + Categories ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[9pt] leading-normal min-h-[1123px]">
                                                    <div className="font-bold text-[9pt] mb-2 underline">Requirements/Enclosures for transfer of plot/premises on request of the General Power of Attorney of the allottee.</div>
                                                    <p className="text-[8.5pt] mb-2">In addition to the above requirement/enclosures the following shall also be required:</p>
                                                    <ol className="list-none pl-0 space-y-1 text-[8.5pt] text-justify mb-3">
                                                        <li>(1) Certified copy of the General Power of Attorney given by the allottee for transfer of the plot/premises.</li>
                                                        <li>(2) An indemnity bond by the transferee in the prescribed format.</li>
                                                        <li>(3) An affidavit by the transferee about legal validity of the GPA on the prescribed format.</li>
                                                        <li>(4) A copy of the registered agreement to sell in favour of the transferee.</li>
                                                        <li>(5) In absence of registered agreement to sell, a public notice, as per the language provided by the Authority, in two national dailies. Full pages of the newspapers carrying the public notice shall required to be submitted.</li>
                                                    </ol>

                                                    <p className="text-[8.5pt] font-bold mb-2">If the transferor/transferee is a partnership firm/Pvt. Ltd. Co./Ltd. Co./Regd. Society/Trust in addition to the above the following documents shall also be required:</p>
                                                    <ol className="list-none pl-0 space-y-1 text-[8.5pt] text-justify mb-3">
                                                        <li>a) A certified copy of the partnership deed of transferee, copy of form A &amp; B (certificates issued by Registrar of firms),</li>
                                                        <li>b) An Authority letter or Power of Attorney to purchase the plot/premises is required if transfer application is not signed by all partners.</li>
                                                        <li>c) An Authority letter or Power of Attorney of the transferor firm shall also be required if transfer application is not signed by all partners.</li>
                                                        <li>d) A certified copy of the resolution passed by board of directors of the transferor company/society/trust to sell the plot/premises and of the transferee company/society/trust to purchase the plot/premises. Both resolutions shall be in favour of the authorised signatory to sell/purchase the plot/premises.</li>
                                                        <li>e) Memorandum and article of association of the company/Memorandum of the society/trust of the transferee.</li>
                                                        <li>f) In case of company list of shareholders and list of directors duly certified by Chartered Accountant/list of executive members of the society/list of trustees in case of society/trust.</li>
                                                        <li>g) Attested photograph and signatures of all directors/society executive members and trustees.</li>
                                                    </ol>

                                                    <div className="font-bold text-[8.5pt] mb-1">The following shall fall into the prescribed categories:</div>
                                                    <ol className="list-none pl-0 space-y-1 text-[8.5pt] text-justify">
                                                        <li>1. Bonafide Sole Proprietor/Partner(s)/Director(s)/Regular Employees of bonafide functional industrial units who are operational on the land leased by NOIDA/NEPZ (Category : NOIDA-IND)</li>
                                                        <li>2. Bonafide Sole Proprietor/Partner(s)/Director(s) of the bonafide functional commercial establishment, established on land/premises allotted by NOIDA, exclusively &amp; specifically for this purpose only. (Category : NOIDA-COMM).</li>
                                                        <li>3. Bonafide Managing Trustees/Regular Employees of functional institutional which are operational on land/premises leased by NOIDA, exclusively for this purpose. (Category : NOIDA-INSTT).</li>
                                                        <li>4. Bonafide eligible villager who was a KHATEDAR/SAHKHATEDAR of the land which has been acquired for the development of NOIDA and who has received compensation of acquired land and there is no litigation pending (Category : NOIDA-VIL).</li>
                                                        <li>5. Regular employees of the Authority or regular employees of the Authority. (Category : NOIDA-EMP).</li>
                                                    </ol>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">6</div>
                                                </div>

                                                {/* ===== PAGE 7: Joint Affidavit Page 1 (Rs. 20 Stamp) ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="border border-dashed border-gray-400 p-2 text-center mb-4 text-[9pt] text-gray-600">Non-Judicial Stamp Paper of Rs. 20/-</div>
                                                    <div className="text-[8.5pt] italic mb-3">Joint affidavit on non-judicial stamp paper of Rs. 20/- from transferor(s) and transferee (s) duly notarized.</div>
                                                    <div className="text-center font-bold text-[11pt] uppercase mb-4">NEW OKHLA INDUSTRIAL DEVELOPMENT AUTHORITY</div>

                                                    {!p.isGpa ? (
                                                        <div className="mb-2 text-justify text-[9.5pt]">
                                                            I/We/M/s <strong><Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var></strong>
                                                            {p.transferor1Age && <> aged <strong><Var name="transferor1Age">{p.transferor1Age}</Var></strong> years,</>}
                                                            {' '}<strong><Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var></strong>
                                                            {' '}R/o <strong><Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var></strong>
                                                            {p.hasJointTransferor && p.transferor2Name && <> and <strong><Var name="transferor2Name">{p.transferor2Name}</Var></strong> {p.transferor2Age && <> aged <strong><Var name="transferor2Age">{p.transferor2Age}</Var></strong> years,</>} <strong><Var name="transferor2Relation">{p.transferor2Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferor2Father">{p.transferor2Father || '__________________'}</Var></strong> R/o <strong><Var name="transferor2Address">{p.transferor2Address || '__________________'}</Var></strong></>}
                                                            {' '}transferor of Plot/Premises No. <strong><Var name="plotNo">{p.plotNo || '________'}</Var></strong> Block <strong><Var name="block">{p.block || '________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '________'}</Var></strong> Noida, measuring <strong><Var name="area">{p.area || '________'}</Var></strong> sq. mtrs.
                                                        </div>
                                                    ) : (
                                                        <div className="text-gray-400 line-through text-[8.5pt] mb-2 select-none">I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor of Plot/Premises No. ________ Block ________ Sector ________ Noida, measuring ________ sq. mtrs. (Omitted - GPA Active)</div>
                                                    )}

                                                    {p.isGpa ? (
                                                        <div className="mb-2 text-justify text-[9.5pt] border-l-2 border-gray-400 pl-3">
                                                            I/We/M/s <strong><Var name="gpaHolderName">{p.gpaHolderName || '__________________'}</Var></strong>
                                                            {p.gpaHolderAge && <> aged <strong><Var name="gpaHolderAge">{p.gpaHolderAge}</Var></strong> years,</>}
                                                            {' '}<strong><Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="gpaHolderFather">{p.gpaHolderFather || '__________________'}</Var></strong>
                                                            {' '}R/o <strong><Var name="gpaHolderAddress">{p.gpaHolderAddress || '__________________'}</Var></strong>
                                                            {' '}transferor of Plot/Premises No. <strong><Var name="plotNo">{p.plotNo || '________'}</Var></strong> Block <strong><Var name="block">{p.block || '________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '________'}</Var></strong> Noida, measuring <strong><Var name="area">{p.area || '________'}</Var></strong> sq. mtrs. on behalf of the allottee Shri/Smt./Km. <strong><Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '__________________'}</Var></strong> <strong><Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '__________________'}</Var></strong> R/o <strong><Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '__________________'}</Var></strong> as registered General Power of Attorney holder, GPA registered with Sub-Registrar/Tehsildar <strong><Var name="gpaOffice">{p.gpaOffice || '________'}</Var></strong> No. <strong><Var name="gpaRegNo">{p.gpaRegNo || '________'}</Var></strong> dated <strong><Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var></strong>. (strike off if application is not through GPA.)
                                                        </div>
                                                    ) : (
                                                        <div className="text-gray-400 line-through text-[8.5pt] mb-2 select-none">OR I/We/M/s ______________________ S/o, W/o, D/o ______________________ R/o ______________________ transferor on behalf of allottee... GPA registered with Sub-Registrar/Tehsildar No. ______ dated ______ (Omitted - GPA Inactive)</div>
                                                    )}

                                                    <div className="text-center font-bold my-2">AND</div>

                                                    <div className="mb-3 text-justify text-[9.5pt]">
                                                        I/We/M/s <strong><Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '__________________'}</Var></strong>
                                                        {p.transferee1Age && <> aged <strong><Var name="transferee1Age">{p.transferee1Age}</Var></strong> years,</>}
                                                        {' '}<strong><Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '__________________'}</Var></strong>
                                                        {' '}R/o <strong><Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________'}</Var></strong>
                                                        {parseInt(p.transfereeCount) >= 2 && p.transferee2Name && <> and <strong><Var name="transferee2Name">{p.transferee2Name}</Var></strong> {p.transferee2Age && <> aged <strong><Var name="transferee2Age">{p.transferee2Age}</Var></strong> years,</>} <strong><Var name="transferee2Relation">{p.transferee2Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferee2Father">{p.transferee2Father || '__________________'}</Var></strong> R/o <strong><Var name="transferee2Address">{p.transferee2Address || '__________________'}</Var></strong></>}
                                                        {parseInt(p.transfereeCount) >= 3 && p.transferee3Name && <> and <strong><Var name="transferee3Name">{p.transferee3Name}</Var></strong> {p.transferee3Age && <> aged <strong><Var name="transferee3Age">{p.transferee3Age}</Var></strong> years,</>} <strong><Var name="transferee3Relation">{p.transferee3Relation || 'S/o'}</Var></strong> Shri <strong><Var name="transferee3Father">{p.transferee3Father || '__________________'}</Var></strong> R/o <strong><Var name="transferee3Address">{p.transferee3Address || '__________________'}</Var></strong></>}
                                                        {' '}transferee for the above stated plot/premises do hereby solemnly affirm and declare jointly on oath as under in respect of Plot/Premises No. <strong><Var name="plotNo">{p.plotNo || '________'}</Var></strong> Block <strong><Var name="block">{p.block || '________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '________'}</Var></strong> Noida, measuring <strong><Var name="area">{p.area || '________'}</Var></strong> sq. mtrs
                                                    </div>

                                                    <ol className="list-decimal pl-5 space-y-1.5 text-justify text-[9.5pt]">
                                                        <li>That the transferor and transferee are bonafide citizen of India and are competent to contract.</li>
                                                        <li>That the deponents understand that the said plot/premises is transferable on payment of transfer charges, as applicable, to the Authority.</li>
                                                        <li>That the deponents undertake to abide by the rules, regulations terms and conditions and directions of the New Okhla Industrial Development Authority (NOIDA) as applicable from time to time.</li>
                                                        <li>That the transfer of rights, interest, payments, assets, liabilities, title etc. respect to the property are limited to the extent vested in the Transferor.</li>
                                                        <li>(i) That the dues in respect of above said plot/premises have been cleared and No Dues Certificate, issued by the concerned Accounts Officer is enclosed.<br/>(ii) That the dues in respect of usages charges/no usages charges, as applicable, have been cleared and a no dues certificate issued by the Account Officer (Jal) has been enclosed.</li>
                                                        <li>That the transferor has established the unit/enterprise on the above stated premises and a copy of the functional certificate issued by the Authority is enclosed.(applicable for transfer of Industrial/Institutional/Commercial plot/premises)</li>
                                                    </ol>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">7</div>
                                                </div>

                                                {/* ===== PAGE 8: Joint Affidavit continued ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-justify text-[9.5pt] space-y-2">
                                                        <p className="pl-5">That the transferor has obtained Occupancy certificate/completion certification issued by the Authority (applicable for transfer of Residential plot/premises)<br/><strong>OR</strong><br/>That the transferor has obtained valid extension upto the date of transfer and a copy of the extension letter issued by the Authority is enclosed.<br/>(Not applicable for transfer of Group Housing/Housing)</p>
                                                    </div>
                                                    <ol start="7" className="list-decimal pl-5 space-y-1.5 text-justify text-[9.5pt] mt-2">
                                                        <li>That the above property has neither been mortgaged nor offered as collateral security to any institution and is free from all encumbrances.</li>
                                                        <li>That the deponents have ensured that there is no unauthorized construction and/or use in the property.</li>
                                                        <li>(i) The transferor, his/her spouse and/or dependent children and/or his/her/their Industrial/Commercial/Institutional unit established in NOIDA had not obtained any residential plot/premises (i.e. including the property for which this transfer application is being submitted) by way of direct allotment from the Authority and he/she/they, their spouse and/or dependent children and/or his/her/their Industrial/Commercial/ Institutional unit would not apply for allotment of any residential plot/premises under any allotment scheme of the Authority and not take possession of any residential plot/premises in any pending scheme(s) or any future scheme of the Authority but may acquire one or more residential plot/house/flat in NOIDA through transfer from open market.<br/>(ii) That the transferor his spouse/dependent children is/are not a member of any cooperative housing society nor will become member of any cooperative housing society operating in notified area of NOIDA.<br/>(iii) That the transferor understand(s) that in case of any breach of any to he terms and conditions, the Authority shall take action as it may deem fit.<br/>(iv) That the transferor is applying for transfer of the plot/premises under the terms of allotment/Lease deed/Lease-cum-sale-deed/transfer deed executed on <strong><Var name="leaseDate">{formatDate(p.leaseDate)}</Var></strong> (applicable for transfer of residential plot/flat/houses)</li>
                                                        <li>(i) That the transferee shall pay to the Authority all outstanding dues along with interest as applicable.<br/>(ii) That the outstanding premium/ lease rent /interest and all other dues against the plot/premises shall constitute the first charge against the plot/premises.</li>
                                                        <li>(i) That the deponents understands that the receipt of the transfer application and charges by the Authority are purely provisional and does not provide/constitute any right to either party for claiming grant of Transfer Permission by the Authority. The Authority reserves the right to decide the case on merit and is free to reject a request for transfer without assigning any reason.</li>
                                                    </ol>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">8</div>
                                                </div>

                                                {/* ===== PAGE 9: Joint Affidavit continued ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="text-justify text-[9.5pt] pl-5 space-y-2 mb-2">
                                                        <p>(ii) In the event of such rejection the transfer charges deposited, if any, shall be refunded to the transferor. No interest, however, shall be payable on the deposits so made.</p>
                                                        <p>(iii) If transfer does not materialize due to withdrawal of the transfer application by mutual consent of the transferor and transferee then transfer charges will not be refunded/adjusted even if transfer application is withdrawn. In case of dispute between the transferor and transferee, permission for withdrawal of transfer application shall be granted with orders of the competent court.</p>
                                                        <p>(iv) The transferee shall not transfer his/her/their rights without prior approval of the Authority in writing which the Authority may refuse without assigning any reason or allow on such terms and conditions as it may deem fit.</p>
                                                        <p>(v) The transfer of plot/premises is an act between the transferor and transferee and as such any liens, claims, damages, compensation, adverse court orders etc. arising thereof subsequently would be the sole liability of transferee(s) and Noida would remain indemnified against the same.</p>
                                                    </div>
                                                    <ol start="12" className="list-decimal pl-5 space-y-1.5 text-justify text-[9.5pt]">
                                                        <li>(i) That in the event of transfer being permitted by the Authority the deponents shall have to execute a transfer deed and thereafter shall be entitled to lease hold rights for the remaining period of 90 years from the date of execution of original legal documents or taking over possession of the plot/premises, whichever is earlier.<br/>(ii) The transfer deed shall be executed within 90 days from the date of issue of transfer memorandum. The transfer deed must, inter alia, incorporate the various terms and conditions mentioned in the transfer memorandum. The final mutation will be made in the name of the transferee after receipt of the certified copy of the transfer deed and its acceptance by the Authority. This transfer deed shall be required to be submitted with the Authority within one month from the date of its execution. In case of failure to execute lease-Cum-Sale Deed/Transfer Deed (as the case may be) by the Transferee would invite payment of penalty as applicable from time to time.<br/>(iii) The transferee shall be given one year for making the industrial unit/commercial establishment/institution functional from the date of issue of the transfer memorandum. The transferee of residential plot shall be required to obtain extension on payment of prescribed extension charges to raise construction/ obtain occupancy/completion certificate.</li>
                                                        <li>That the lease rent/ground rent of the subject property shall be revised and shall be payable as indicated by the Authority in transfer permission letter. The revised lease rent/ground rent may be enhanced after every 10 years from the date of execution of the original lease deed/legal documents subject to the condition that the same shall not exceed 50% of the lease/ground rent last thus fixed. (in case of commercial plot/shop lease rent shall not be revised, however, provision of enhancement as per terms of lease deed shall be applicable.</li>
                                                    </ol>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">9</div>
                                                </div>

                                                {/* ===== PAGE 10: Joint Affidavit Points 14-21 + Signatures ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <ol start="14" className="list-decimal pl-5 space-y-1.5 text-justify text-[9.5pt] mb-4">
                                                        <li>That the deponents understand that notwithstanding any request/instruction of either party the payment made by the either party shall be first adjusted towards the interest due and premium/cost of the property and thereafter the same shall be appropriated towards the annual lease/ground rent.</li>
                                                        <li>That the transferee shall put the plot/premises in use exclusively for the authorized purpose and shall not use it for any purpose other than the allotted/leased.</li>
                                                        <li>The lease rent/ground/rent of the aforesaid property shall be applicable as indicated in the transfer memorandum.</li>
                                                        <li>The transferee shall put the commercial property/plot/shop in use for which it has been allotted.</li>
                                                        <li>The deponents understand that the Chief Executive Officer of the Authority shall have every right to amend or after the terms and conditions as deemed fit from time to time and such amendments/modifications shall be final and binding on them.</li>
                                                        <li>The transferor and transferee agree that in the event of transfer being obtained through misrepresentation/suppression or fact or in case of any breach/violation of terms and conditions of the brochure of the Scheme/ HPTA/Licence Agreement/Lease Deed/Transfer Deed and the terms and conditions stated here is this affidavit, the Authority shall be free to take action as deemed fit and exercise its right for cancellation of allotment/lease hold rights including forfeiture of the deposited amount.</li>
                                                        <li>The deponent shall be bound by the provisions of U.P. Industrial Area Development Act, 1976 (U.P. Act No. 6 of 1976) and the rules and regulations made and/or directions issued there under and enacted/amended from time to time.</li>
                                                        <li>The deponent undertakes that the dispute, if any, with regards to approval of transfer of property and or otherwise shall be subject to the Courts Jurisdiction of High Court Allahabad/Civil Court Ghaziabad/ Gautam Budh Nagar.</li>
                                                    </ol>

                                                    <div className="flex justify-between text-center mt-6 mb-4">
                                                        <div className="w-44"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold text-[9pt]">DEPONENT<br/>(TRANSFEROR)</div></div>
                                                        <div className="w-44"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold text-[9pt]">DEPONENT<br/>(TRANSFEREE)</div></div>
                                                    </div>

                                                    <div className="border-t border-gray-400 pt-3 mt-2">
                                                        <div className="text-center font-bold underline mb-2 text-[10pt]">VERIFICATION</div>
                                                        <p className="text-justify text-[9.5pt]">We the above deponents do hereby verify that the contents and declarations made in the affidavit are true to the best of our respective knowledge and belief and nothing has been concealed therein.</p>
                                                    </div>

                                                    <div className="flex justify-between text-center mt-6 mb-2">
                                                        <div className="w-44"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold text-[9pt]">DEPONENT<br/>(TRANSFEROR)</div></div>
                                                        <div className="w-44"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold text-[9pt]">DEPONENT<br/>(TRANSFEREE)</div></div>
                                                    </div>

                                                    <p className="text-[8pt] italic mt-3">NOTE:- Affidavit is to be given on non-judicial stamp paper of Rs.20/- and duly notarized by Notary Public.</p>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">10</div>
                                                </div>

                                                {/* ===== PAGE 11: GPA Affidavit (Rs. 10 Stamp) - CONDITIONAL ===== */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-gray-300' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none text-gray-400 mt-40">
                                                            <div className="text-lg font-bold">Page 11: GPA Affidavit</div>
                                                            <div className="text-sm">This page is applicable only when &quot;Submit via GPA Holder&quot; is enabled. Hidden from print.</div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="border border-dashed border-gray-400 p-2 text-center mb-3 text-[9pt] text-gray-600">Non-Judicial Stamp Paper of Rs. 10/-</div>
                                                            <div className="text-center font-bold text-[9pt] uppercase mb-1">TO BE SUBMITTED BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY</div>
                                                            <div className="text-center text-[8pt] mb-2">(ON NON JUDICIAL STAMP PAPER OF RS. 10/- DULY NOTARISED)</div>
                                                            <div className="text-center font-bold text-[11pt] uppercase mb-3">AFFIDAVIT</div>

                                                            <p className="mb-3 text-justify text-[9.5pt]">
                                                                I, <strong><Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '________________________________________________'}</Var></strong>
                                                                {' '}aged <strong><Var name="transferee1Age">{p.transferee1Age || '__________'}</Var></strong> Years
                                                                {' '}<strong><Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var></strong>, D/o, W/o Shri <strong><Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '___________________________________________________________________'}</Var></strong>
                                                                {' '}R/o <strong><Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________________________________________________________________'}</Var></strong> hereby solemnly affirm and state on oath as under:-
                                                            </p>

                                                            <ol className="list-none pl-0 space-y-2 text-justify text-[9.5pt]">
                                                                <li>1- That deponent is transferee of plot/premises No. <strong><Var name="plotNo">{p.plotNo || '__________'}</Var></strong> Block <strong><Var name="block">{p.block || '_____________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '__________'}</Var></strong>, NOIDA measuring <strong><Var name="area">{p.area || '________________'}</Var></strong>Sqm.</li>
                                                                <li>2- That Sh./Smt./Km. <strong><Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '________________________________________'}</Var></strong> <strong><Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '________________________________'}</Var></strong> R/o <strong><Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '_________________________________________'}</Var></strong> is the allottee of Plot/ premises No. <strong><Var name="plotNo">{p.plotNo || '________________'}</Var></strong> Block <strong><Var name="block">{p.block || '_____________'}</Var></strong> Sector- <strong><Var name="sector">{p.sector || '_________'}</Var></strong>, NOIDA measuring <strong><Var name="area">{p.area || '______________________'}</Var></strong> Sqm.</li>
                                                                <li className="pl-4">OR</li>
                                                                <li>3- That Sh./Smt./Km. <strong><Var name="gpaHolderName">{p.gpaHolderName || '____________________________'}</Var></strong> <strong><Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="gpaHolderFather">{p.gpaHolderFather || '___________________________'}</Var></strong> R/o <strong><Var name="gpaHolderAddress">{p.gpaHolderAddress || '________________________________________'}</Var></strong> is power of Attorney holder of the allottee and submitting application for transfer of the plot/premises on behalf of the allottee. General Power of Attorney was executed on <strong><Var name="gpaDate">{formatDate(p.gpaDate)}</Var></strong> and registered with Sub-Registrar/Tehsildar <strong><Var name="gpaOffice">{p.gpaOffice || '_______________'}</Var></strong> on <strong><Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var></strong> at <strong><Var name="gpaRegNo">{p.gpaRegNo || '_____________________'}</Var></strong> for plot/premises No. <strong><Var name="plotNo">{p.plotNo || '_______________________'}</Var></strong> Block <strong><Var name="block">{p.block || '____________________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '____'}</Var></strong> measuring <strong><Var name="area">{p.area || '______________'}</Var></strong> Sqm.</li>
                                                                <li>4- That the said GPA has not been revoked so far.</li>
                                                                <li>5- That the deponent has satisfied himself about the authenticity and legal validity of the above stated Power of Attorney and the allottee of the plot/ premises as stated at Sl. No. 2 above is alive.</li>
                                                            </ol>

                                                            <div className="flex justify-end mt-8"><div className="w-40 text-center"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold">DEPONENT</div></div></div>

                                                            <div className="mt-6 border-t border-gray-400 pt-3">
                                                                <div className="text-center font-bold underline mb-2">VERIFICATION</div>
                                                                <p className="text-justify text-[9.5pt]">I, the above named deponent do hereby verify that the above contents from para 1 to 5 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.</p>
                                                                <div className="flex justify-end mt-8"><div className="w-40 text-center"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold">DEPONENT</div></div></div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">11</div>
                                                </div>

                                                {/* ===== PAGE 12: Transferee Standard Affidavit (Rs. 10 Stamp) ===== */}
                                                <div className="paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px]">
                                                    <div className="border border-dashed border-gray-400 p-2 text-center mb-3 text-[9pt] text-gray-600">Non-Judicial Stamp Paper of Rs. 10/-</div>
                                                    <div className="text-center font-bold text-[9pt] uppercase mb-1">TO BE SUBMITTED BY TRANSFEREE</div>
                                                    <div className="text-center text-[8pt] mb-2">(ON NON JUDICIAL STAMP PAPER OF RS. 10/- DULY NOTARISED)</div>
                                                    <div className="text-center font-bold text-[11pt] uppercase mb-3">AFFIDAVIT</div>

                                                    <p className="mb-3 text-justify text-[9.5pt]">
                                                        I, <strong><Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '________________________________________________'}</Var></strong>
                                                        {' '}aged <strong><Var name="transferee1Age">{p.transferee1Age || '__________'}</Var></strong> Years
                                                        {' '}<strong><Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var></strong>, D/o, W/o Shri <strong><Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '______________________________________________________________________'}</Var></strong>
                                                        {' '}R/o <strong><Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '__________________________________________________________________________'}</Var></strong> hereby solemnly affirm and state on oath as under:-
                                                    </p>

                                                    <ol className="list-decimal pl-5 space-y-3 text-justify text-[9.5pt]">
                                                        <li>That the deponent is transferee of plot/premises No. <strong><Var name="plotNo">{p.plotNo || '__________'}</Var></strong> Block <strong><Var name="block">{p.block || '_____________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '__________'}</Var></strong>, NOIDA measuring <strong><Var name="area">{p.area || '________________'}</Var></strong> Sqm.</li>
                                                        <li>That Sh./Smt./Km. <strong><Var name="transferor1Name">{p.transferor1Name || p.allotteeName || '_______________________________________________'}</Var></strong> <strong><Var name="transferor1Relation">{p.transferor1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferor1Father">{p.transferor1Father || p.allotteeFather || '_____________________________________'}</Var></strong> R/o <strong><Var name="transferor1Address">{p.transferor1Address || p.allotteeAddress || '______________________________________________________________________'}</Var></strong> is the allottee of Plot/ premises No. <strong><Var name="plotNo">{p.plotNo || '______________'}</Var></strong> Block <strong><Var name="block">{p.block || '___________'}</Var></strong> Sector- <strong><Var name="sector">{p.sector || '_______'}</Var></strong>, NOIDA measuring <strong><Var name="area">{p.area || '______________________'}</Var></strong> Sqm.</li>
                                                        <li>That the deponent has satisfied himself that the said plot/premises are without any encumbrance.</li>
                                                        <li>That the deponent has received/shall receive from the transferor all original documents such as allotment letter, possession letter, lease deed, transfer memorandum, transfer deed, no dues certificate, extension letter/occupancy/completion certificate/functional certification, payment deposit challans, etc. pertaining to the above stated plot/premises.</li>
                                                    </ol>

                                                    <div className="flex justify-end mt-8"><div className="w-40 text-center"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold">DEPONENT</div></div></div>

                                                    <div className="mt-6 border-t border-gray-400 pt-3">
                                                        <div className="text-center font-bold underline mb-2">VERIFICATION</div>
                                                        <p className="text-justify text-[9.5pt]">I, the above named deponent do hereby verify that the above contents from para 1 to 4 are true and correct to the best of my knowledge and no part of this is false and nothing has been concealed therein.</p>
                                                        <div className="flex justify-end mt-8"><div className="w-40 text-center"><div className="h-10"></div><div className="border-t border-black pt-1 font-bold">DEPONENT</div></div></div>
                                                    </div>
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">12</div>
                                                </div>

                                                {/* ===== PAGE 13: Indemnity Bond Page 1 (Rs. 100 Stamp) - CONDITIONAL ===== */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-gray-300' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none text-gray-400 mt-40">
                                                            <div className="text-lg font-bold">Page 13: Indemnity Bond (Page 1)</div>
                                                            <div className="text-sm">This page is applicable only when &quot;Submit via GPA Holder&quot; is enabled. Hidden from print.</div>
                                                        </div>
                                                    ) : (
                                                        <div>
                                                            <div className="border border-dashed border-gray-400 p-2 text-center mb-3 text-[9pt] text-gray-600">Non-Judicial Stamp Paper of Rs. 100/-</div>
                                                            <div className="text-center font-bold text-[9pt] uppercase mb-3 leading-tight">INDEMNITY BOND BY TRANSFEREE IF APPLICATION IS SUBMITTED THROUGH POWER OF ATTORNEY</div>

                                                            <p className="mb-3 text-justify text-[9.5pt]">
                                                                This Indemnity Bond is executed on ____________ day of ____________ in the year Two thousand ____________________ by Shri/Smt./Km. <strong><Var name="transferee1Name">{p.transferee1Name || p.transfereeName || '________________________'}</Var></strong> <strong><Var name="transferee1Relation">{p.transferee1Relation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="transferee1Father">{p.transferee1Father || p.transfereeFather || '_____________________________________'}</Var></strong> R/o <strong><Var name="transferee1Address">{p.transferee1Address || p.transfereeAddress || '________________________________________'}</Var></strong> (transferee) hereinafter referred as &apos;EXECUTANT&apos; in favour of New Okhla Industrial Development Authority hereinafter referred to as &apos;AUTHORITY&apos;.
                                                            </p>

                                                            <p className="mb-3 text-justify text-[9.5pt]">
                                                                Whereas Shri/Smt./Km. <strong><Var name="gpaHolderName">{p.gpaHolderName || '________________________________________'}</Var></strong> <strong><Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var></strong>, W/o, D/o Shri <strong><Var name="gpaHolderFather">{p.gpaHolderFather || '______________________________'}</Var></strong> R/o <strong><Var name="gpaHolderAddress">{p.gpaHolderAddress || '_____________________________________'}</Var></strong> on behalf of the allottee of commercial plot/ shop No. <strong><Var name="plotNo">{p.plotNo || '_______________'}</Var></strong> Block <strong><Var name="block">{p.block || '_______'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '___________________'}</Var></strong> measuring <strong><Var name="area">{p.area || '_____________'}</Var></strong> Sq.Mtrs. NOIDA holds the power of attorney (hereinafter called power of attorney) in respect of Plot/Shop No. <strong><Var name="plotNo">{p.plotNo || '___________________'}</Var></strong> Block <strong><Var name="block">{p.block || '_____________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '_______'}</Var></strong> measuring <strong><Var name="area">{p.area || '________'}</Var></strong> Sqm. NOIDA and being bounded as under:-
                                                            </p>

                                                            <div className="my-3 text-[9.5pt] space-y-1">
                                                                <div>ON THE NORTH BY <strong><Var name="northBoundary">{p.northBoundary || '_____________'}</Var></strong></div>
                                                                <div>ON THE SOUTH BY <strong><Var name="southBoundary">{p.southBoundary || '______________'}</Var></strong></div>
                                                                <div>ON THE EAST BY <strong><Var name="eastBoundary">{p.eastBoundary || '______________'}</Var></strong></div>
                                                                <div>ON THE WEST BY <strong><Var name="westBoundary">{p.westBoundary || '_____________'}</Var></strong></div>
                                                            </div>

                                                            <p className="text-justify text-[9.5pt]">
                                                                By virtue of the powers conferred upon Shri/Smt./Km. <strong><Var name="gpaHolderName">{p.gpaHolderName || '___________________________'}</Var></strong> <strong><Var name="gpaHolderRelation">{p.gpaHolderRelation || 'S/o'}</Var></strong>, W/o, D/o <strong><Var name="gpaHolderFather">{p.gpaHolderFather || '___________________________________'}</Var></strong> R/o <strong><Var name="gpaHolderAddress">{p.gpaHolderAddress || '________________________________________________'}</Var></strong> vide the attorney dated <strong><Var name="gpaDate">{formatDate(p.gpaDate)}</Var></strong> duly registered with Sub-Registrar on <strong><Var name="gpaRegDate">{formatDate(p.gpaRegDate)}</Var></strong> at <strong><Var name="gpaOffice">{p.gpaOffice || '___________________________'}</Var></strong> (certified copy enclosed). The executant is getting commercial plot/shop No. <strong><Var name="plotNo">{p.plotNo || '______________'}</Var></strong> Block <strong><Var name="block">{p.block || '_________'}</Var></strong> Sector <strong><Var name="sector">{p.sector || '_________'}</Var></strong>, NOIDA measuring <strong><Var name="area">{p.area || '______________'}</Var></strong> Sqm. transferred in his name.
                                                            </p>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">13</div>
                                                </div>

                                                {/* ===== PAGE 14: Indemnity Bond Page 2 - CONDITIONAL ===== */}
                                                <div className={`paper-page print-break bg-white p-10 font-serif relative text-[10pt] leading-relaxed min-h-[1123px] ${!p.isGpa ? 'print:hidden border-2 border-dashed border-gray-300' : ''}`}>
                                                    {!p.isGpa ? (
                                                        <div className="m-auto text-center space-y-3 max-w-md select-none text-gray-400 mt-40">
                                                            <div className="text-lg font-bold">Page 14: Indemnity Bond (Page 2)</div>
                                                            <div className="text-sm">This page is applicable only when &quot;Submit via GPA Holder&quot; is enabled. Hidden from print.</div>
                                                        </div>
                                                    ) : (
                                                        <div className="space-y-3 text-justify text-[9.5pt]">
                                                            <p>The executant is satisfied that as per the above documents the power of attorney holder is totally competent and legally authorized to effect the transfer/sale of the above mentioned property and to do all acts and execute all documents which are necessary for transfer/sale of the said property on behalf of the present allottee.</p>
                                                            <p>And whereas the Authority shall consider the transfer in favour of the executant provided the executant indemnifies the Authority against all losses, damages, inconvenience, cost and or litigation which may be caused because of such permission of transfer by Authority.</p>
                                                            <p>Now the (transferee) executant in the event of grant of permission by the Authority for sale/transfer of the above said property has agreed to indemnify the Authority against any claim/damage, cost, loss, inconvenience, litigation arising by the grant of permission for transfer of the above property. The executant also indemnifies the Authority for any liability in all forms that may be created by virtue of a court order and/or any other Competent Authority.</p>
                                                            <p>By this deed the executant shall also be totally responsible for other costs, damages, legal proceedings and any other loss to the Authority on account of above property and shall ensure to meet all the liabilities arising or which may arise by grant of permission to transfer and shall discharge the same from his own resources.</p>
                                                            <p>This indemnity Bond is executed in presence of the following witnesses on the day and month first above mentioned.</p>

                                                            <div className="flex justify-between items-start mt-8">
                                                                <div className="w-52 space-y-4">
                                                                    <div className="font-bold underline">WITNESSES</div>
                                                                    <div>
                                                                        1. NAME __________________________________<br/>
                                                                        ADDRESS _______________________________<br/>
                                                                        <span className="ml-3">_______________________________</span>
                                                                    </div>
                                                                    <div>
                                                                        2. NAME __________________________________<br/>
                                                                        ADDRESS _______________________________<br/>
                                                                        <span className="ml-3">_______________________________</span>
                                                                    </div>
                                                                </div>
                                                                <div className="w-48 text-center">
                                                                    <div className="h-16"></div>
                                                                    <div className="border-t border-black pt-1 font-bold uppercase">SIGNATURE OF THE EXECUTANT<br/>(TRANSFEREE)</div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    )}
                                                    <div className="absolute bottom-4 left-0 right-0 text-center text-[9pt]">14</div>
                                                </div>
                                            </>
                                        );
                                    })()}"""

# Read the file
with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

# Lines are 0-indexed in list, 1-indexed in file
# Replace lines 6172-6923 (1-indexed) = indices 6171-6922 (0-indexed)
start_idx = 6171  # line 6172
end_idx = 6922    # line 6923 (inclusive)

# Split the new JSX into lines
new_lines = [line + '\n' for line in new_jsx.split('\n')]

# Splice
new_file = lines[:start_idx] + new_lines + lines[end_idx + 1:]

print(f"New file: {len(new_file)} lines")
print(f"Removed {end_idx - start_idx + 1} lines, inserted {len(new_lines)} lines")

# Write
with open('test_script.jsx', 'w', encoding='utf-8') as f:
    f.writelines(new_file)

print("File written successfully!")
