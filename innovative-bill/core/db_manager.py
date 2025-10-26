import pandas as pd
import os
from core import config

# ------------------------------------------------------------
# DATABASE MANAGER — Handles Local CSV + Google Sheets (future)
# ------------------------------------------------------------

def load_csv(path: str) -> pd.DataFrame:
    """Safely load a CSV file into a DataFrame."""
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"[ERROR] Could not read {path}: {e}")
        return pd.DataFrame()


def save_csv(df: pd.DataFrame, path: str):
    """Safely save a DataFrame to CSV."""
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        print(f"[ERROR] Could not write to {path}: {e}")


def get_customers():
    """Return customer list (local or cloud depending on toggle)."""
    if config.USE_GOOGLE_SHEETS:
        # Placeholder for Google Sheets connection (to be added later)
        return []
    df = load_csv(config.CUSTOMER_FILE)
    return df


def add_customer(data: dict):
    """Add new customer to the CSV database."""
    df = load_csv(config.CUSTOMER_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_csv(df, config.CUSTOMER_FILE)
    return True


def get_products():
    """Return product list (local or cloud depending on toggle)."""
    if config.USE_GOOGLE_SHEETS:
        return []
    return load_csv(config.PRODUCT_FILE)


def add_product(data: dict):
    """Add new product entry."""
    df = load_csv(config.PRODUCT_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_csv(df, config.PRODUCT_FILE)
    return True


def get_transporters():
    """Return transporter list."""
    if config.USE_GOOGLE_SHEETS:
        return []
    return load_csv(config.TRANSPORTER_FILE)


def add_transporter(data: dict):
    """Add new transporter."""
    df = load_csv(config.TRANSPORTER_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_csv(df, config.TRANSPORTER_FILE)
    return True


def save_invoice(data: dict):
    """Save invoice entry to CSV."""
    df = load_csv(config.INVOICE_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_csv(df, config.INVOICE_FILE)
    return True
