from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from core import config
import os

def overlay_text_on_pdf(data: dict, output_path: str):
    """
    Generate a new PDF by overlaying text fields onto the blank invoice template.
    """
    overlay_path = os.path.join(config.GENERATED_DIR, "temp_overlay.pdf")
    c = canvas.Canvas(overlay_path)
    c.setFont("Helvetica", 10)

    # ------------------------------------------------------------
    # EXAMPLE COORDINATES — adjust as per your blank_invoice.pdf
    # ------------------------------------------------------------
    # Invoice header
    c.drawString(430, 780, str(data.get("invoice_no", "")))
    c.drawString(430, 765, str(data.get("invoice_date", "")))

    # Buyer details
    c.drawString(80, 720, str(data.get("buyer", "")))

    # Product + totals
    c.drawString(80, 680, str(data.get("product", "")))
    c.drawString(260, 680, str(data.get("qty", "")))
    c.drawString(320, 680, str(data.get("rate", "")))
    c.drawString(400, 680, str(data.get("subtotal", "")))
    c.drawString(460, 680, str(data.get("grand_total", "")))

    # Amount in words
    c.drawString(80, 620, str(data.get("amount_words", "")))

    c.save()

    # ------------------------------------------------------------
    # Merge overlay with base template
    # ------------------------------------------------------------
    template_path = config.BLANK_TEMPLATE
    base_pdf = PdfReader(template_path)
    overlay_pdf = PdfReader(overlay_path)
    writer = PdfWriter()

    page = base_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    with open(output_path, "wb") as out:
        writer.write(out)

    os.remove(overlay_path)
    return output_path
