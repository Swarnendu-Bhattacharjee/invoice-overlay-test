import os
import asyncio
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from pyppeteer import launch
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates', 'tally_invoice_template.html')
GENERATED_DIR = os.path.join(BASE_DIR, 'generated_invoices')
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_invoice_data(invoice_id):
    invoices = pd.read_csv(os.path.join(DATA_DIR, 'invoices.csv'))
    customers = pd.read_csv(os.path.join(DATA_DIR, 'customers.csv'))
    products = pd.read_csv(os.path.join(DATA_DIR, 'products.csv'))

    inv = invoices[invoices['invoice_id'] == invoice_id].iloc[0].to_dict()
    cust = customers[customers['customer_id'] == inv['customer_id']].iloc[0].to_dict()
    prod = products[products['product_id'].isin(eval(inv['product_ids']))]

    return {
        'invoice': inv,
        'customer': cust,
        'products': prod.to_dict(orient='records')
    }

def render_invoice_html(invoice_context):
    env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')))
    template = env.get_template('tally_invoice_template.html')
    rendered_html = template.render(
        invoice_number=invoice_context['invoice']['invoice_id'],
        invoice_date=datetime.now().strftime('%d-%m-%Y'),
        customer_name=invoice_context['customer']['name'],
        customer_address=invoice_context['customer']['address'],
        customer_gstin=invoice_context['customer'].get('gstin', ''),
        items=invoice_context['products'],
        subtotal=invoice_context['invoice']['subtotal'],
        tax=invoice_context['invoice']['tax'],
        total=invoice_context['invoice']['total']
    )

    temp_html_path = os.path.join(GENERATED_DIR, f"temp_invoice_{invoice_context['invoice']['invoice_id']}.html")
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    return temp_html_path

async def generate_pdf_from_html(input_html, output_pdf):
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(f'file://{input_html}', {'waitUntil': 'networkidle2'})
    await page.pdf({
        'path': output_pdf,
        'format': 'A4',
        'printBackground': True,
        'margin': {'top': '10mm', 'bottom': '10mm', 'left': '10mm', 'right': '10mm'}
    })
    await browser.close()

def generate_invoice(invoice_id):
    print(f"Generating invoice for ID: {invoice_id}")
    ctx = load_invoice_data(invoice_id)
    html_path = render_invoice_html(ctx)
    output_pdf = os.path.join(GENERATED_DIR, f"Invoice_{invoice_id}.pdf")
    asyncio.get_event_loop().run_until_complete(generate_pdf_from_html(html_path, output_pdf))
    print(f"✅ Invoice generated: {output_pdf}")

if __name__ == "__main__":
    invoice_id = input("Enter invoice ID: ").strip()
    generate_invoice(invoice_id)
