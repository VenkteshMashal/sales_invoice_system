from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_invoice_pdf(invoice, company, customer):
    folder_path = "generated_invoices"
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"invoice_{invoice.invoice_number.replace('/', '_')}.pdf"
    file_path = os.path.join(folder_path, file_name)

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("<b>Tax Invoice</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    company_info = f"""
    <b>{company.company_name}</b><br/>
    {company.address or ""}<br/>
    Phone: {company.phone or ""}<br/>
    Email: {company.email or ""}<br/>
    State: {company.state or ""}
    """

    invoice_info = f"""
    <b>Invoice No:</b> {invoice.invoice_number}<br/>
    <b>Date:</b> {invoice.invoice_date}
    """

    header_table = Table([
        [Paragraph(company_info, styles["Normal"]), Paragraph(invoice_info, styles["Normal"])]
    ], colWidths=[350, 170])

    elements.append(header_table)
    elements.append(Spacer(1, 20))

    bill_to = f"""
    <b>Bill To:</b><br/>
    {customer.customer_name}<br/>
    Contact No: {customer.phone}<br/>
    {customer.address or ""}
    """

    elements.append(Paragraph(bill_to, styles["Normal"]))
    elements.append(Spacer(1, 20))

    data = [["#", "Item Name", "Quantity", "Unit", "Price/Unit", "Amount"]]

    for index, item in enumerate(invoice.items, start=1):
        data.append([
            index,
            item.item_name,
            str(item.quantity),
            item.unit,
            f"Rs. {item.price_per_unit}",
            f"Rs. {item.amount}"
        ])

    data.append(["", "", "", "", "Sub Total", f"Rs. {invoice.sub_total}"])
    data.append(["", "", "", "", "GST", f"Rs. {invoice.gst_amount}"])
    data.append(["", "", "", "", "Total", f"Rs. {invoice.total_amount}"])

    table = Table(data, colWidths=[30, 160, 70, 60, 90, 90])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    summary = f"""
    <b>Invoice Amount In Words:</b><br/>
    {invoice.amount_in_words}<br/><br/>
    <b>Received:</b> Rs. {invoice.paid_amount}<br/>
    <b>Balance:</b> Rs. {invoice.balance_amount}<br/>
    <b>Status:</b> {invoice.payment_status}
    """

    elements.append(Paragraph(summary, styles["Normal"]))
    elements.append(Spacer(1, 40))

    elements.append(Paragraph(f"For {company.company_name}:", styles["Normal"]))
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Authorized Signatory", styles["Normal"]))

    doc.build(elements)

    return file_path