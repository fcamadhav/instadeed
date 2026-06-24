import os
from fpdf import FPDF

class TaxInvoicePDF(FPDF):
    def header(self):
        self.set_y(10)
        
    def footer(self):
        self.set_y(-25)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "This is a computer-generated invoice and does not require a physical signature.", align="C")
        self.ln(6)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="C")

def generate_invoice_pdf(invoice_data: dict, filepath: str):
    pdf = TaxInvoicePDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Colors
    primary_color = (30, 63, 160) # Brand blue
    text_dark = (15, 23, 42)      # Charcoal
    text_muted = (100, 116, 139)  # Muted gray
    border_color = (226, 232, 240)
    
    # 1. Header Section (Title & Brand Logo/Text)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*primary_color)
    pdf.cell(100, 10, "INSTADEED")
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*text_dark)
    pdf.cell(90, 10, "TAX INVOICE", align="R")
    pdf.ln(12)
    
    # 2. Seller and Invoice Meta info (Side-by-Side)
    y_start = pdf.get_y()
    
    # Left Column: Seller Details
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Sold By:")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(100, 4.5, "Instadeed Technology Solutions Pvt. Ltd.")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Sector 62, Noida, Gautam Buddh Nagar")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Uttar Pradesh, India - 201301")
    pdf.ln(4.5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(100, 4.5, "GSTIN: 09AAPCI1234A1Z5")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "PAN: AAPCI1234A")
    
    # Right Column: Invoice Details (absolute positioned at same Y)
    pdf.set_y(y_start)
    pdf.set_x(115)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(75, 5, "Invoice Details:", align="R")
    pdf.ln(5)
    
    details = [
        ("Invoice No:", invoice_data.get("invoice_number", "")),
        ("Invoice Date:", invoice_data.get("created_at", "")[:10]),
        ("Place of Supply:", "Uttar Pradesh (09)"),
        ("State Code:", "09"),
        ("Order ID:", invoice_data.get("order_id", "")[:13]),
        ("Payment Status:", invoice_data.get("status", "PAID"))
    ]
    
    for label, val in details:
        pdf.set_x(115)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        # We write label
        pdf.cell(35, 4.5, label, align="L")
        # We write value in bold
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(40, 4.5, val, align="R")
        pdf.ln(4.5)
        
    pdf.ln(4)
    
    # Horizontal separator
    pdf.set_draw_color(*border_color)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # 3. Bill To Section
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Bill To (Recipient):")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(100, 4.5, f"Name: {invoice_data.get('customer_name', 'Customer')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, f"Phone: +91 {invoice_data.get('customer_phone', '')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, f"Email: {invoice_data.get('customer_email', '')}")
    pdf.ln(4.5)
    pdf.cell(100, 4.5, "Address: Gautam Buddh Nagar, Uttar Pradesh, India")
    pdf.ln(8)
    
    # 4. Itemized Table
    # Widths: Item Description (75), SAC (18), Price (24), CGST (24), SGST (24), Total (25)
    col_widths = [75, 18, 24, 24, 24, 25]
    headers = ["Item Description", "SAC Code", "Base Amount", "CGST (9%)", "SGST (9%)", "Total"]
    
    pdf.set_fill_color(248, 250, 252) # Light slate
    pdf.set_text_color(*text_dark)
    pdf.set_font("Helvetica", "B", 8.5)
    
    # Draw headers
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1, align="C", fill=True)
    pdf.ln()
    
    # Values
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 30, 30)
    
    item_desc = f"Legal Drafting Service: {invoice_data.get('agreement_type', 'Legal Document')}"
    sac_code = "9982"
    base_amt = invoice_data.get("amount", 0.0)
    gst_amt = invoice_data.get("gst_amount", 0.0)
    cgst_sgst = round(gst_amt / 2, 2)
    total_amt = invoice_data.get("total", 0.0)
    
    row_data = [
        item_desc,
        sac_code,
        f"INR {base_amt:.2f}",
        f"INR {cgst_sgst:.2f}",
        f"INR {cgst_sgst:.2f}",
        f"INR {total_amt:.2f}"
    ]
    
    # Draw row
    pdf.cell(col_widths[0], 10, row_data[0], border=1, align="L")
    pdf.cell(col_widths[1], 10, row_data[1], border=1, align="C")
    pdf.cell(col_widths[2], 10, row_data[2], border=1, align="R")
    pdf.cell(col_widths[3], 10, row_data[3], border=1, align="R")
    pdf.cell(col_widths[4], 10, row_data[4], border=1, align="R")
    pdf.cell(col_widths[5], 10, row_data[5], border=1, align="R")
    pdf.ln(10)
    
    pdf.ln(5)
    
    # 5. Summary / Totals block in the right
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(45, 6, "Subtotal (Base Price):", align="L")
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(45, 6, f"INR {base_amt:.2f}", align="R")
    pdf.ln(6)
    
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(45, 6, "CGST @ 9%:", align="L")
    pdf.cell(45, 6, f"INR {cgst_sgst:.2f}", align="R")
    pdf.ln(6)
    
    pdf.set_x(110)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(45, 6, "SGST @ 9%:", align="L")
    pdf.cell(45, 6, f"INR {cgst_sgst:.2f}", align="R")
    pdf.ln(6)
    
    # Total row with background fill
    pdf.ln(1)
    pdf.set_x(110)
    pdf.set_fill_color(238, 244, 255) # Brand light blue background
    pdf.set_draw_color(*primary_color)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*primary_color)
    pdf.cell(45, 8, "Grand Total:", border="TB", align="L", fill=True)
    pdf.cell(45, 8, f"INR {total_amt:.2f}", border="TB", align="R", fill=True)
    pdf.ln(8)
    
    pdf.ln(10)
    
    # 6. Terms & Signature
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*text_dark)
    pdf.cell(100, 5, "Terms & Conditions:")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(120, 4, "1. Payment is due immediately upon drafting completion.")
    pdf.ln(4)
    pdf.cell(120, 4, "2. Under Section 65B of the Indian Evidence Act, this invoice is digitally valid.")
    pdf.ln(4)
    pdf.cell(120, 4, "3. For support or queries, write to billing@instadeed.in")
    
    # Save file
    pdf.output(filepath)

if __name__ == "__main__":
    mock_invoice = {
        "invoice_number": "INV-20260624-A3D8",
        "created_at": "2026-06-24T13:37:09",
        "order_id": "ord_29103980129",
        "status": "PAID",
        "customer_name": "Madhav Prasad Bhati",
        "customer_phone": "9812345678",
        "customer_email": "madhav.bhati@example.com",
        "agreement_type": "GNIDA 5-in-1 Composite Package",
        "amount": 422.88,
        "gst_amount": 76.12,
        "total": 499.00
    }
    
    # Ensure scratch directory exists
    os.makedirs("scratch", exist_ok=True)
    generate_invoice_pdf(mock_invoice, "scratch/test_invoice.pdf")
    print("PDF generated successfully at scratch/test_invoice.pdf")
