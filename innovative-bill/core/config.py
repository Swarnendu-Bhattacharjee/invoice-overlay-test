import os

# ------------------------------------------------------------
# CONFIGURATION FILE — PIPL ACCOUNTING SYSTEM
# ------------------------------------------------------------

# Base project directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ------------------------------------------------------------
# LOCAL DATA PATHS
# ------------------------------------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.csv")
PRODUCT_FILE = os.path.join(DATA_DIR, "products.csv")
TRANSPORTER_FILE = os.path.join(DATA_DIR, "transporters.csv")
INVOICE_FILE = os.path.join(DATA_DIR, "invoices.csv")

# ------------------------------------------------------------
# TEMPLATE & STATIC PATHS
# ------------------------------------------------------------
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
GENERATED_DIR = os.path.join(BASE_DIR, "generated_invoices")

INVOICE_TEMPLATE = os.path.join(TEMPLATE_DIR, "invoice_template.pdf")
BLANK_TEMPLATE = os.path.join(TEMPLATE_DIR, "blank_invoice.pdf")
LOGO_FILE = os.path.join(STATIC_DIR, "logo.png")

# ------------------------------------------------------------
# CLOUD / GOOGLE SHEETS SETTINGS (placeholder)
# ------------------------------------------------------------
USE_GOOGLE_SHEETS = False  # set True later when we integrate
GOOGLE_SHEET_IDS = {
    "customers": "",
    "products": "",
    "transporters": "",
    "invoices": ""
}

# ------------------------------------------------------------
# APP SETTINGS
# ------------------------------------------------------------
APP_TITLE = "PIPL Accounting System"
VERSION = "Phase 1.0"
