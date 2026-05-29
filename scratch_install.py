import os

file_path = "Madhav_Drafting_Hub.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """                                        <div className="text-center mt-6 font-bold absolute bottom-6 left-0 right-0">-6-</div>
                                    </div>
                                </>
                            )}"""

replacement = """                                        <div className="text-center mt-6 font-bold absolute bottom-6 left-0 right-0">-6-</div>
                                    </div>

                                    {/* PAGE 7: BUYER AFFIDAVIT */}
                                    <div className="paper-page print-break text-gray-900 font-serif relative p-10 text-[10.5pt] leading-relaxed">
                                        <div className="text-right text-[10px] uppercase mb-4 text-gray-500 font-sans tracking-widest font-bold">Buyer Signature Affidavit</div>
                                        <div className="text-center font-bold text-xl mb-6 underline font-sans">शपथ पत्र</div>
                                        
                                        <div className="mb-6 font-bold font-sans">
                                            समक्ष:- श्रीमान प्रबंधक महोदय सम्पत्ति <br />
                                            ग्रेटर नोएडा औद्योगिक विकास प्राधिकरण <br />
                                            जिला:- गौतम बुद्ध नगर, उत्तर प्रदेश 
                                        </div>

                                        <div className="mb-4 leading-loose text-justify font-sans">
                                            शपथ पत्र की और से श्री / श्रीमती <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeName || '................'}</span>{' '}
                                            आयु <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeAge || '................'}</span>{' '}
                                            पुत्र/पुत्री/पत्नी <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeParentName || '................'}</span>{' '} 
                                            निवासी <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeAddress || '................................'}</span>{' '}
                                            आधारों पर प्रस्तुत है कि-
                                        </div>

                                        <ol className="list-decimal list-outside ml-6 space-y-4 text-justify font-sans">
                                            <li className="pl-2">यह कि मेरा उपरोक्त नाम व पता सब सच व सही है।</li>
                                            <li className="pl-2 leading-loose">
                                                यह कि मैं शपथ कर्ता / कर्ती एक आवासीय प्लॉट/फ्लैट/दुकान संख्या <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.plotNo || '................'}</span>{' '}
                                                टाइप/ब्लॉक <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.block || '................'}</span>{' '}
                                                सेक्टर <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.sector || '................'}</span>{' '}
                                                क्षेत्रफल <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.area || '................'}</span>{' '}
                                                आवंटन संख्या <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.allotmentNo || '................'}</span>{' '}
                                                को मैंने श्री / श्रीमती <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transferorName || '................................'}</span>{' '}
                                                से खरीदा है । यदि ट्रांसफर के बाद मूल आवंटी व किसी अन्य व्यक्ति से किसी विषय का अथवा क्लेम कि बात भविष्य में कोई विवाद उत्पन्न होता है तो उसकी पूर्ण जिम्मेदारी मुझ शपथ कर्ता की होगी। प्राधिकरण / योजना प्रभारी / योजना सहायक की कोई जिम्मेदारी नहीं होगी। तथा उक्त प्लॉट / फ्लैट / दुकान / प्रॉपर्टी का हस्तांतरण मुझ शपथकर्ता के पक्ष में किया जाना आवश्यक है।
                                            </li>
                                            <li className="pl-2">यह कि भूखण्ड पर कोई Dues / मोरगेज पाया जाता है तो उसकी पूर्ण जिम्मेदारी मुझ शपथकर्ता की होगी ।</li>
                                            <li className="pl-2">यह कि वर्ष 2020 की प्राधिकरण द्वारा वांछित भवन निर्माण विलम्ब शुल्क मेरे द्वारा जमा किया जाएगा।</li>
                                            <li className="pl-2">यह कि शपथ पत्र कि धारा 1 व 4 सच व सही है ।</li>
                                        </ol>

                                        <div className="flex justify-between items-end mt-16 mt-8 font-sans font-bold">
                                            <div>
                                                सत्यापित स्थान :- गौतम बुद्ध नगर। <br />
                                                दिनांक :-  ……………………………
                                            </div>
                                            <div className="text-center w-48 border-t border-black pt-2">
                                                हo शपथकर्ता / कर्ती <br />
                                                (Buyer)
                                            </div>
                                        </div>
                                        <div className="text-center mt-6 font-bold absolute bottom-6 left-0 right-0 font-sans">-7-</div>
                                    </div>

                                    {/* PAGE 8: SELLER AFFIDAVIT */}
                                    <div className="paper-page print-break text-gray-900 font-serif relative p-10 text-[10.5pt] leading-relaxed">
                                        <div className="text-right text-[10px] uppercase mb-4 text-gray-500 font-sans tracking-widest font-bold">Seller Signature Affidavit</div>
                                        <div className="text-center font-bold text-xl mb-6 underline font-sans">शपथ पत्र</div>

                                        <div className="mb-6 font-bold font-sans">
                                            समक्ष:- श्रीमान प्रबंधक महोदय <br />
                                            ग्रेटर नोएडा औद्योगिक विकास प्राधिकरण <br />
                                            जिला:- गौतम बुद्ध नगर, उत्तर प्रदेश 
                                        </div>

                                        <div className="mb-6 leading-loose text-justify font-sans">
                                            शपथ पत्र की और से श्री / श्रीमती <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transferorName || '................'}</span>{' '}
                                            पुत्र/पुत्री/पत्नी <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transferorParentName || '................'}</span>{' '} 
                                            निवासी <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transferorAddress || '................................'}</span>{' '}
                                            आधारों पर प्रस्तुत है कि-
                                        </div>

                                        <div className="mb-4 font-bold font-sans">मैं शपथ कर्ता कर्ती शपथ पूर्वक बयान करता / करती हू कि –</div>

                                        <ol className="list-decimal list-outside ml-6 space-y-4 text-justify font-sans">
                                            <li className="pl-2">यह कि मेरा उपरोक्त नाम व पता सब सच व सही है।</li>
                                            <li className="pl-2 leading-loose">
                                                यह कि मैं शपथ कर्ता / कर्ती एक आवासीय प्लॉट/फ्लैट/दुकान संख्या <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.plotNo || '................'}</span>{' '}
                                                टाइप/ब्लॉक <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.block || '................'}</span>{' '}
                                                सेक्टर <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.sector || '................'}</span>{' '}
                                                क्षेत्रफल <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.area || '................'}</span>{' '} 
                                                वर्ग मीटर, आवंटन संख्या <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.allotmentNo || '................'}</span>{' '}
                                                का / की मालिकाना मालिक व काबिज हू जिसका मैंने श्री / श्रीमती <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeName || '................................'}</span>{' '}
                                                को विक्रय कर दिया है।
                                            </li>
                                            <li className="pl-2 leading-loose">
                                                यह कि उक्त प्लॉट / फ्लैट / दुकान / प्रॉपर्टी का हस्तांतरण श्री / श्रीमती <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.transfereeName || '................................'}</span>{' '}
                                                के पक्ष में किये जाने में मुझ शपथकर्ता को कोई आपत्ति नहीं है।
                                            </li>
                                            <li className="pl-2">यह कि यदि भविष्य में मेरे हस्ताक्षरों कि आवश्यकता होती है तो मैं ग्रेटर नोएडा औद्योगिक विकास प्राधिकरण में आने के लिये बाधित रखूँगा / रहूँगी ।</li>
                                            <li className="pl-2">यह कि शपथ पत्र कि धारा 1 व 4 मेरे निजी ज्ञान में सब सच व सही है। कोई बात झूठ या छिपायी नहीं गयी है। ईश्वर मेरा साक्षी है।</li>
                                        </ol>

                                        <div className="flex justify-between items-end mt-16 font-sans font-bold">
                                            <div>
                                                सत्यापित स्थान :- गौतम बुद्ध नगर। <br />
                                                दिनांक :-  ……………………………
                                            </div>
                                            <div className="text-center w-48 border-t border-black pt-2">
                                                हo शपथकर्ता / कर्ती <br />
                                                (Seller)
                                            </div>
                                        </div>
                                        <div className="text-center mt-6 font-bold absolute bottom-6 left-0 right-0 font-sans">-8-</div>
                                    </div>

                                    {/* PAGE 9: JOINT AFFIDAVIT */}
                                    <div className="paper-page print-break text-gray-900 font-serif relative p-10 text-[10.5pt] leading-relaxed flex flex-col justify-center">
                                        <div className="text-right text-[10px] uppercase mb-8 text-gray-500 font-sans tracking-widest font-bold absolute top-10 right-10">Seller AND Buyer Signature Affidavit</div>

                                        <div className="mb-16 mt-8 leading-loose text-center text-[12pt] font-sans">
                                            This stamp paper is attached with this transfer form for the residential Plot / Flat / Shop / Property No. <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.plotNo || '........'}</span>{' '}
                                            Type / Block <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.block || '........'}</span>{' '}
                                            Sector <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.sector || '........'}</span>{' '}
                                            Area <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.area || '........'}</span> Sq. Mtrs. Vide Allotment No.{' '}
                                            <span className="font-bold bg-rose-50 px-1 underline decoration-dotted decoration-gray-500 decoration-1 underline-offset-4 decoration-clone">{tmAppData.allotmentNo || '................'}</span>{' '}
                                            Situated in Greater Noida, Distt. Gautam Buddha Nagar.
                                        </div>

                                        <div className="flex justify-between items-end mt-24 px-12 font-sans">
                                            <div className="text-center w-48">
                                                <div className="font-bold mb-1">Deponent-1</div>
                                                <div className="text-gray-600 font-bold border-t border-black pt-2">Transferor</div>
                                            </div>
                                            <div className="text-center w-48">
                                                <div className="font-bold mb-1">Deponent-2</div>
                                                <div className="text-gray-600 font-bold border-t border-black pt-2">Transferee</div>
                                            </div>
                                        </div>
                                        <div className="text-center mt-6 font-bold absolute bottom-6 left-0 right-0 font-sans">-9-</div>
                                    </div>
                                </>
                            )}"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Target string not found in the file.")
