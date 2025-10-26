import os
import pandas as pd
from datetime import date
from core import config, db_manager, utils

# ------------------------------------------------------------
# INVOICE MANAGER — Core computation & PDF generation bridge
# ------------------------------------------------------------

def prepare_invoice_data(form_data: dict):
    """
    Combine user-entered data with calculated fields.
    """
    qty = utils.safe_float(form_data.get("qty", 0))
    rate = utils.safe_float(form_data.get("rate", 0))
    subtotal = utils.calc_total(qty, rate)

    cgst = subtotal * 0.09  # 9%
    sgst = subtotal * 0.09  # 9%
    grand_total = subtotal + cgst + sgst

    return {
        "invoice_no": form_data.get("invoice_no", ""),
        "invoice_date": utils.format_date(form_data.get("invoice_date", date.today())),
        "buyer": form_data.get("buyer", ""),
        "product": form_data.get("product", ""),
        "qty": qty,
        "rate": rate,
        "subtotal": subtotal,
        "cgst": round(cgst, 2),
        "sgst": round(sgst, 2),
        "grand_total": round(grand_total, 2),
        "amount_words": utils.num_to_words(round(grand_total, 2)),
        "timestamp": utils.timestamp(),
    }


def save_invoice_to_db(invoice_data: dict):
    """Store invoice metadata to the main CSV (invoices.csv)."""
    return db_manager.save_invoice(invoice_data)


def generate_invoice_pdf(invoice_data: dict, template_path=None):
    """
    Overlay data onto blank invoice PDF template using coordinate mapping.
    """
    from core import pdf_overlay  # lazy import to avoid circular dependencies
    template = template_path or config.BLANK_TEMPLATE
    output_name = f"Invoice_{invoice_data['invoice_no']}.pdf"
    output_path = os.path.join(config.GENERATED_DIR, output_name)

    # Create actual PDF overlay using ReportLab
    pdf_overlay.overlay_text_on_pdf(invoice_data, output_path)

    return output_path


# ------------------------------------------------------------
# (Optional utility) Quick test mode
# ------------------------------------------------------------
if __name__ == "__main__":
    test_data = {
        "invoice_no": "TEST001",
        "invoice_date": date.today(),
        "buyer": "Test Buyer Pvt Ltd",
        "product": "Insulation Sleeve",
        "qty": 10,
        "rate": 50,
    }
    inv = prepare_invoice_data(test_data)
    save_invoice_to_db(inv)
    path = generate_invoice_pdf(inv)
    print(f"✅ Test invoice generated at: {path}")
