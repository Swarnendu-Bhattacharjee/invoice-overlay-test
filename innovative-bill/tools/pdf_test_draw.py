# tools/pdf_test_draw.py
import os
from core import config
from core import pdf_overlay

test_data = {
    "invoice_no": "COORD-TEST-001",
    "invoice_date": "22/10/2025",
    "buyer": "BUYER NAME AT COORD",
    "buyer_line1": "Buyer line 1 example",
    "buyer_line2": "Buyer line 2 example",
    "product_row_1_name": "Product X (row1)",
    "product_row_1_qty": "12",
    "product_row_1_rate": "123.45",
    "subtotal": "1481.40",
    "cgst": "133.33",
    "sgst": "133.33",
    "grand_total": "1748.06",
    "amount_words": "One Thousand Seven Hundred Forty Eight Rupees Only",
    "auth_signature": "Authorised Signatory"
}

out = os.path.join("generated_invoices", "coord_test_invoice.pdf")
os.makedirs(os.path.dirname(out), exist_ok=True)
pdf_overlay.overlay_text_on_pdf(test_data, out)
print("Wrote test PDF to", out)
