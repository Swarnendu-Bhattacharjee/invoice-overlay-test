from flask import Flask, render_template, request, send_file, Response
import json, os, uuid, decimal
from overlay_utils import create_overlay_pdf, merge_overlay_with_template
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COORD_PATH = os.path.join(BASE_DIR, 'overlays', 'coordinates.json')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates', 'blank_invoice.pdf')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
SIG_DIR = os.path.join(BASE_DIR, 'static', 'signatures')
os.makedirs(SIG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
def load_json(p): return json.load(open(p,'r',encoding='utf-8'))
def to_decimal(s):
    try:
        return decimal.Decimal(str(s).replace(',','').replace('₹',''))
    except:
        return decimal.Decimal('0')
def num_to_words_val(n):
    n=int(decimal.Decimal(n).to_integral_value())
    ones=['','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
    tens=['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
    def two(u):
        if u<20: return ones[u]
        return tens[u//10] + ('' if u%10==0 else ' '+ones[u%10])
    def three(u):
        h=u//100
        r=u%100
        if h and r:
            return ones[h]+' Hundred '+two(r)
        if h and not r:
            return ones[h]+' Hundred'
        return two(r)
    parts=[]
    crore=n//10000000
    if crore:
        parts.append(three(crore)+' Crore'); n%=10000000
    lakh=n//100000
    if lakh:
        parts.append(three(lakh)+' Lakh'); n%=100000
    thousand=n//1000
    if thousand:
        parts.append(three(thousand)+' Thousand'); n%=1000
    if n:
        parts.append(three(n))
    return (' '.join(parts) + ' Only') if parts else 'Zero Only'
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
@app.route('/')
def index():
    buyers=[]; consignees=[]
    bf=os.path.join(BASE_DIR,'overlays','buyers.json')
    cf=os.path.join(BASE_DIR,'overlays','consignees.json')
    if os.path.exists(bf): buyers=json.load(open(bf,'r',encoding='utf-8'))
    if os.path.exists(cf): consignees=json.load(open(cf,'r',encoding='utf-8'))
    return render_template('form.html', buyers=buyers, consignees=consignees)
@app.route('/_numtowords')
def _numtowords():
    n = request.args.get('num','0')
    try:
        nint = int(float(n))
    except:
        nint = 0
    return Response('Rupees ' + num_to_words_val(nint), mimetype='text/plain')
@app.route('/generate', methods=['POST'])
def generate():
    coords = load_json(COORD_PATH)
    form = request.form
    data = {}
    for key in form:
        data[key] = form.get(key)
    items_count = 5
    taxable_total = decimal.Decimal('0')
    for i in range(1, items_count+1):
        qty = to_decimal(form.get(f'qty_{i}','0'))
        rate = to_decimal(form.get(f'rate_{i}','0'))
        amount = qty * rate
        if not form.get(f'amount_{i}'):
            data[f'amount_{i}'] = str(amount.quantize(decimal.Decimal('0.01')))
        else:
            data[f'amount_{i}'] = form.get(f'amount_{i}')
            amount = to_decimal(data[f'amount_{i}'])
        taxable_total += amount
    try:
        cgst_p = decimal.Decimal(str(form.get('cgst_rate','9%')).replace('%',''))
    except:
        cgst_p = decimal.Decimal('0')
    try:
        sgst_p = decimal.Decimal(str(form.get('sgst_rate','9%')).replace('%',''))
    except:
        sgst_p = decimal.Decimal('0')
    cgst_amount = (taxable_total * cgst_p / decimal.Decimal('100')).quantize(decimal.Decimal('0.01'))
    sgst_amount = (taxable_total * sgst_p / decimal.Decimal('100')).quantize(decimal.Decimal('0.01'))
    tax_total = (cgst_amount + sgst_amount).quantize(decimal.Decimal('0.01'))
    grand_total = (taxable_total + tax_total).quantize(decimal.Decimal('0.01'))
    data['taxable_value'] = str(taxable_total)
    data['cgst_amount'] = str(cgst_amount)
    data['sgst_amount'] = str(sgst_amount)
    data['tax_total'] = str(tax_total)
    data['tax_amount_total'] = '₹' + str(grand_total)
    data['total_amount'] = '₹' + str(grand_total)
    words = 'Rupees ' + num_to_words_val(grand_total)
    data['amount_in_words_footer'] = words
    data['amount_in_words_top'] = words
    sig_file = request.files.get('authorised_sign_file')
    sig_path = None
    if sig_file and sig_file.filename:
        ext = os.path.splitext(sig_file.filename)[1].lower()
        name = f"{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(SIG_DIR, name)
        sig_file.save(save_path)
        sig_path = save_path
    if sig_path:
        data['authorised_sign_image'] = sig_path
    overlay_path = os.path.join(BASE_DIR, 'overlays', 'overlay_temp.pdf')
    filename = f"Invoice_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(OUTPUT_DIR, filename)
    create_overlay_pdf(TEMPLATE_PATH, overlay_path, coords, data, pages=3)
    merge_overlay_with_template(TEMPLATE_PATH, overlay_path, output_path)
    return send_file(output_path, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
