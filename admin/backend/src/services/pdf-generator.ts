import PDFDocument from "pdfkit";
import path from "path";
import fs from "fs";

const STORAGE_ROOT = path.resolve(__dirname, "..", "..", "storage", "documents");

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function numToWords(n: number): string {
  if (n === 0) return "Zero";
  const units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];
  const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];

  const convert = (num: number): string => {
    if (num < 20) return units[num];
    const t = Math.floor(num / 10);
    return tens[t] + (num % 10 ? " " + units[num % 10] : "");
  };

  let result = "";
  const crore = Math.floor(n / 10000000); n %= 10000000;
  const lakh = Math.floor(n / 100000); n %= 100000;
  const thousand = Math.floor(n / 1000); n %= 1000;

  if (crore) result += convert(crore) + " Crore ";
  if (lakh) result += convert(lakh) + " Lakh ";
  if (thousand) result += convert(thousand) + " Thousand ";
  if (n) result += convert(n);

  return result.trim();
}

function addHeaderFooter(doc: PDFDocument, title: string) {
  doc.fontSize(8).fillColor("#94a3b8").text("INSTADEED — Generated Document", 40, 20, { align: "center" });
  doc.fontSize(7).text(`Page ${doc.page}`, 40, doc.page.height - 30, { align: "center" });
}

// ============ RENT AGREEMENT ============
function generateRentAgreement(doc: PDFDocument, data: Record<string, any>) {
  doc.fontSize(16).font("Helvetica-Bold").text("RENT AGREEMENT", { align: "center" });
  doc.moveDown(0.5);

  const stampNo = data.stampPaperNumber;
  if (stampNo) {
    doc.fontSize(8).font("Helvetica-Oblique").text(`Stamp Paper No: ${stampNo}`, { align: "center" });
    doc.moveDown(0.3);
  }

  doc.fontSize(10).font("Helvetica");
  const intro = `This Rent Agreement is made on this ${data.agreementDate || "______"} at ${data.agreementPlace || "_________________"} between:\n\n`
    + `MR./MRS. ${data.landlordName || "____________________________________"}, R/o ${data.landlordAddress || "______________________________________________________________________"}, Cont. No. - ${data.landlordPhone || "________________"}. (Hereinafter called the First Party-Owner).\n\n`
    + `AND\n\n`
    + `MR./MRS. ${data.tenantName || "____________________________________"}, R/o ${data.tenantAddress || "______________________________________________________________________"}, Cont. No. - ${data.tenantPhone || "________________"}. (Hereinafter called the Second Party Tenant).\n\n`
    + `And whereas the First Party has agreed to let out ${data.propertyAddress || "____________________________________________________"}. And the Second Party has agreed to take on rent the said premises mentioned as above the following terms and condition:-`;

  doc.text(intro);
  doc.moveDown();

  const rentAmt = data.rentAmount || "________";
  const rentWords = data.rentInWords || numToWords(Number(rentAmt) || 0);
  const maintIncluded = data.maintenanceIncluded ? "Including" : "Excluding";
  const startDate = data.startDate || "__________";
  const endDate = data.endDate || "__________";
  const paymentDay = data.paymentDay || "____";
  const advanceRent = data.advanceRent || "____________";
  const advanceWords = data.advanceInWords || numToWords(Number(advanceRent) || 0);
  const securityDeposit = data.securityDeposit || "____________";
  const securityWords = data.securityInWords || numToWords(Number(securityDeposit) || 0);
  const propertyType = data.propertyType || "Residential";

  const clauses = [
    `That the monthly rent agreed between both the parties is Rs. ${rentAmt}/- (Rupees ${rentWords} only) ${maintIncluded} Maintenance charges.`,
    `That the tenancy has commenced from ${startDate} to ${endDate} for a period of 11 months.`,
    `The monthly Rent of Rs. ${rentAmt}/- (Rupees ${rentWords} only) which shall be paid by the Second Party to the First Party by the ${paymentDay} day of every English Calendar month.`,
    "If both the parties have agreed to continue further, then after 11 months of tenancy period its mandatory that the rent will be increased by 10%.",
    `That the Second party shall not make any additions or alteration in the said premises without permission of the First party. That the Second party shall use the said premises only for ${propertyType} purpose not for any other purpose. That the First party can visit the said premises at reasonable hours.`,
    "That electric charge, Gas charges, shall be paid by the Second party. Power backup, water charges & maintenance charges with Club house will be borne by the Second party directly to the concerned authorities.",
    `That the Second party will be giving Rs. ${advanceRent}/- (Rupees ${advanceWords} only) as one month advance rent giving and Rs. ${securityDeposit}/- (Rupees ${securityWords} only) as interest free security deposit.`,
    "If this agreement is not renewed after expiry of the tenancy period, the Second party will hand over the said premises to the First party in smooth manner.",
    "All the keys which were handed over to the Second party at the time of possession should be handed over back to the First party otherwise the First party will get that lock replaced or will get the amount deducted from the security money in getting that lock replaced.",
    "The security amount is not adjustable. The First party will refund the security amount to the Second party when the Second party will vacant the premises.",
    "That in case if the First party wants to evict the said premises prior to the completion of tenancy period, then the First party will give one-month prior notice to the Second party and if the Second party wants to vacate the said Premises prior to the completion of the tenancy period, then the Second party will also give one months' notice in written or one month rent to the First party.",
    "All furniture & fixtures as per annexure/if any should be taken due care of regular maintenance & servicing of furniture & fixture must be done be the Second party. Any damage/breakage to the property/furniture & fixtures will have to be borne by Second party or that will be deducted from the security deposit.",
    `That the lease has been granted for exclusive ${propertyType} use of the same family and under no circumstances Second party cannot sublet the premises for PG or to any other party.`,
    "That the First party shall not be responsible for any incident in the premises during the tenancy period.",
    "In case the rent is not paid timely for consecutive two months and if the rent not paid for the running month by the Second party then, he/she shall be liable to vacate the premises immediately. In the First party shall not be liable to any refund of security deposit.",
    "That the second party shall not use the said property for any illegal purpose, if the second party shall use the said property for illegal purpose he will liable himself for the same the first party and his property shall not be responsible for the same.",
    "That the Tenant cannot make any addition / alteration to the said property / premises for any purposes, without the in written permission granted by the first party.",
    "In no way the second party or his heir will claim for ownership of the said flat.",
    "It has been agreed between both the parties that if tenant vacate before six months then one month of advance rent amount security will not be refundable and it shall be forfeited."
  ];

  clauses.forEach((clause, i) => {
    doc.fontSize(10).font("Helvetica-Bold").text(`${i + 1}. `, { continued: true });
    doc.font("Helvetica").text(clause);
    doc.moveDown(0.3);
  });

  doc.moveDown();
  doc.fontSize(10).font("Helvetica-Bold").text("WITNESSES:-");
  doc.moveDown(0.5);

  const w1Name = data.witness1Name || "______________________";
  const w2Name = data.witness2Name || "______________________";

  doc.fontSize(9).font("Helvetica");
  doc.text(`1. __________________________\n   (Signature)\n   Name: ${w1Name}\n   Ph: ${data.witness1Phone || ""}\n   Add: ${data.witness1Address || ""}`);
  doc.moveDown();
  doc.text(`2. __________________________\n   (Signature)\n   Name: ${w2Name}\n   Ph: ${data.witness2Phone || ""}\n   Add: ${data.witness2Address || ""}`);

  doc.addPage();
  doc.fontSize(14).font("Helvetica-Bold").text("ANNEXURE-I", { align: "center" });
  doc.moveDown();
  doc.fontSize(10).text(`Detail of fixtures & fittings provided in the flat no. ${data.propertyAddress || ""}`);
  doc.moveDown();

  const fixtures = [
    ["Tube Lights/Bulbs", data.tubeLights || "________________"],
    ["Ceiling Fans", data.fans || "________________"],
    ["LEDs", data.leds || "________________"],
    ["Chimney", data.chimney || "________________"],
    ["RO Unit", data.roUnit || "________________"],
    ["AC's", data.ac || "________________"],
    ["Main Door Keys", data.keys || "________________"],
    ["Exhaust Fan", data.exhaustFan || "________________"],
    ["Bell", data.bell || "________________"],
    ["Wall Mirror", data.mirror || "________________"],
    ["Curtain Rods", data.curtains || "________________"],
    ["Wardrobe", data.wardrobe || "________________"],
    ["Kitchen Cupboard", data.kitchenCupboard || "________________"],
    ["Modular Kitchen", data.modularKitchen || "________________"],
    ["Any Other", data.otherFixtures || "________________"],
  ];

  fixtures.forEach(([name, qty]) => {
    doc.text(`${name}: ${qty}`);
  });
}

// ============ AGREEMENT TO SELL ============
function generateAts(doc: PDFDocument, data: Record<string, any>) {
  doc.fontSize(16).font("Helvetica-Bold").text("AGREEMENT TO SELL", { align: "center" });
  doc.moveDown();
  doc.fontSize(10).font("Helvetica");

  const intro = `This deed of Agreement to sell is executed on this ${data.executionDate || "______"} between:\n\n`
    + `MR./MRS. ${data.seller1Name || "______________________"} (PAN: ${data.seller1Pan || "__________"}, AADHAR: ${data.seller1Aadhar || "________________"}) ${data.seller1Relation || "______"} MR. ${data.seller1Father || "________________"} R/O ${data.seller1Address || "____________________________________________________"} (hereinafter called the First Party/Seller).\n\n`
    + "AND\n\n"
    + `MR./MRS. ${data.buyer1Name || "______________________"} (PAN: ${data.buyer1Pan || "__________"}, AADHAR: ${data.buyer1Aadhar || "________________"}) ${data.buyer1Relation || "______"} MR. ${data.buyer1Father || "________________"} R/O ${data.buyer1Address || "____________________________________________________"} (hereinafter called the Second Party/Purchaser).\n\n`
    + `WHEREAS the First Party is the actual owner/allotted of ${data.propertyDetails || "____________________________________________________"}.\n\n`
    + `AND WHEREAS the First Party has agreed to sell the aforesaid property to the Second Party for a total consideration of Rs. ${data.totalConsideration || "________"}/- (Rupees ${data.totalConsiderationWords || "________________________"} Only.)`;

  doc.text(intro);
  doc.moveDown();
  doc.text("Terms and Conditions:\n\n1. That the Second Party has paid a token/earnest money to the First Party, and the remaining amount shall be paid as per the agreed schedule.\n2. That all the pending dues, electricity bills, and maintenance charges of the authority up to the date of possession shall be cleared by the First Party.\n3. That the First Party shall execute the Transfer Deed / Registry in favor of the Second Party or their nominee after receiving the full sale consideration.\n4. That the First Party assures the Second Party that the property is free from all sorts of encumbrances, loans, mortgages, charges, litigation, and attachments.\n5. That both parties shall abide by all the rules and regulations of the Greater Noida Industrial Development Authority (GNIDA).");
}

// ============ GENERIC DOCUMENT ============
function generateGeneric(doc: PDFDocument, data: Record<string, any>, docType: string) {
  doc.fontSize(16).font("Helvetica-Bold").text(docType.replace(/_/g, " ").replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase()), { align: "center" });
  doc.moveDown(0.5);
  doc.fontSize(8).font("Helvetica-Oblique").text("Instadeed Legal Suite - Official Document Datasheet", { align: "center" });
  doc.fontSize(7).text(`Generated Date: ${new Date().toLocaleDateString("en-IN", { year: "numeric", month: "long", day: "numeric" })}`, { align: "center" });
  doc.moveDown();

  doc.fontSize(11).font("Helvetica-Bold").fillColor("#2563EB").text("1. DOCUMENT SUMMARY");
  doc.moveDown(0.3);
  doc.fillColor("#000").fontSize(9);

  const fields = [
    ["Field Description", "Value"],
    ...Object.entries(data).filter(([_, v]) => v !== null && v !== "").map(([k, v]) => [k.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()), String(v)])
  ];

  fields.forEach(([label, value], i) => {
    doc.font(i === 0 ? "Helvetica-Bold" : "Helvetica").text(`${label}: ${value}`);
  });

  doc.moveDown();
  doc.fontSize(7).fillColor("#94a3b8").text("This document was generated electronically by Instadeed.");
}

// ============ INVOICE ============
function generateInvoice(doc: PDFDocument, data: Record<string, any>) {
  doc.fontSize(18).font("Helvetica-Bold").fillColor("#1E3FA0").text("INSTADEED");
  doc.fontSize(12).fillColor("#0F172A").text("TAX INVOICE", { align: "right" });
  doc.moveDown(0.5);

  doc.fontSize(9).fillColor("#323232");
  doc.text("Sold By:");
  doc.text("Instadeed Technology Solutions Pvt. Ltd.\nSector 62, Noida, Gautam Buddh Nagar\nUttar Pradesh, India - 201301");
  doc.font("Helvetica-Bold").text(`GSTIN: ${data.gstNumber || "09AAPCI1234A1Z5"}\nPAN: AAPCI1234A`);

  doc.moveDown();
  const items = [
    ["Invoice No:", data.invoiceNumber || ""],
    ["Invoice Date:", data.createdAt ? data.createdAt.slice(0, 10) : ""],
    ["Place of Supply:", "Uttar Pradesh (09)"],
    ["Order ID:", data.orderId || ""],
    ["Payment Status:", data.status || "PAID"],
  ];
  items.forEach(([label, val]) => {
    doc.text(`${label} ${val}`, { align: "right" });
  });

  doc.moveDown();
  const baseAmt = data.amount || 0;
  const gstAmt = data.gstAmount || 0;
  const cgstSgst = gstAmt / 2;
  const total = data.total || baseAmt + gstAmt;

  doc.fontSize(9).font("Helvetica-Bold").fillColor("#0F172A");
  doc.text("Bill To (Recipient):");
  doc.font("Helvetica").fillColor("#323232");
  doc.text(`Name: ${data.customerName || "Customer"}\nPhone: +91 ${data.customerPhone || ""}\nEmail: ${data.customerEmail || ""}`);

  doc.moveDown();
  doc.fontSize(8.5).font("Helvetica-Bold").fillColor("#0F172A");
  doc.text(`Item Description: Legal Drafting Service: ${data.agreementType || "Legal Document"}`);
  doc.text(`SAC Code: 9982`);
  doc.text(`Base Amount: INR ${baseAmt.toFixed(2)}`);
  doc.text(`CGST @ 9%: INR ${cgstSgst.toFixed(2)}`);
  doc.text(`SGST @ 9%: INR ${cgstSgst.toFixed(2)}`);
  doc.font("Helvetica-Bold").fillColor("#1E3FA0").fontSize(10);
  doc.text(`Grand Total: INR ${total.toFixed(2)}`);

  doc.moveDown();
  doc.fontSize(9).fillColor("#0F172A").text("Terms & Conditions:");
  doc.fontSize(7.5).fillColor("#646464");
  doc.text("1. Payment is due immediately upon drafting completion.\n2. Under Section 65B of the Indian Evidence Act, this invoice is digitally valid.");
}

// ============ MAIN GENERATOR ============
export async function generateDocument(
  formData: Record<string, any>,
  docType: string,
  orderId: string,
  documentNumber: string
): Promise<{ pdfPath: string }> {
  ensureDir(STORAGE_ROOT);

  const doc = new PDFDocument({ margin: 40, size: "A4" });
  const fileName = `${documentNumber}.pdf`;
  const filePath = path.join(STORAGE_ROOT, fileName);
  const stream = fs.createWriteStream(filePath);
  doc.pipe(stream);

  const payload = formData.payload || formData;
  const actualType = formData.type || docType;

  if (actualType === "RENT" || actualType === "REG_RENT" || docType === "rent-agreement" || docType === "registered-rent") {
    generateRentAgreement(doc, payload);
  } else if (actualType === "ATS" || docType === "ats") {
    generateAts(doc, payload);
  } else if (actualType === "INVOICE") {
    generateInvoice(doc, payload);
  } else {
    generateGeneric(doc, payload, actualType || docType);
  }

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on("finish", () => resolve({ pdfPath: filePath }));
    stream.on("error", reject);
  });
}
