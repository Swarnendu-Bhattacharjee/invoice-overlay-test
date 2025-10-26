import datetime

# ------------------------------------------------------------
# UTILITY FUNCTIONS — General helpers for PIPL Accounting
# ------------------------------------------------------------

def num_to_words(num):
    """Convert numeric amount to words (simple Indian system)."""
    from num2words import num2words
    try:
        return num2words(num, lang='en_IN').title() + " Only"
    except Exception:
        return str(num)

def format_date(dt):
    """Return date in DD/MM/YYYY format."""
    if isinstance(dt, (datetime.date, datetime.datetime)):
        return dt.strftime("%d/%m/%Y")
    return str(dt)

def safe_float(val):
    """Convert any numeric field safely to float."""
    try:
        return float(val)
    except Exception:
        return 0.0

def calc_total(qty, rate):
    """Calculate total for line item."""
    try:
        return round(float(qty) * float(rate), 2)
    except Exception:
        return 0.0

def timestamp():
    """Return a clean timestamp string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
