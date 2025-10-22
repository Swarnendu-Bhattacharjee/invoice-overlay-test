from flask import Flask, render_template, request, send_file
import json, os, uuid, decimal
from overlay_utils import create_overlay_pdf, merge_overlay_with_template
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
COORD_PATH=os.path.join(BASE_DIR,'overlays','coordinates.json')
TEMPLATE_PATH=os.path.join(BASE_DIR,'templates','blank_invoice.pdf')
OUTPUT_DIR=os.path.join(BASE_DIR,'output')
def load_json(p): return json.load(open(p,'r',encoding='utf-8'))
def to_decimal(s):
    try:
        return decimal.Decimal(str(s).replace(',','').replace('₹',''))
    except:
        return decimal.Decimal('0')
def num_to_words(n):
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
    return ' '.join(parts) + ' Only' if parts else 'Zero Only'
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('form.html')
@app.route('/generate',methods=['POST'])
def generate():
    coords=load_json(COORD_PATH)
    form=request.form
    data={}
    for key in form:
        data[key]=form.get(key)
    items_count=5
    taxable_total=decimal.Decimal('0')
    for i in range(1,items_count+1):
        qty=to_decimal(form.get(f'qty_{i}','0'))
        rate=to_decimal(form.get(f'rate_{i}','0'))
        amount=qty*rate
        if not form.get(f'amount_{i}'):
            data[f'amount_{i}']=str(amount.quantize(decimal.Decimal('0.01')))
        else:
            data[f'amount_{i}']=form.get(f'amount_{i}')
            amount=to_decimal(data[f'amount_{i}'])
        taxable_total += amount
    cgst_rate_str=form.get('cgst_rate','9%')
    sgst_rate_str=form.get('sgst_rate','9%')
    try:
        cgst_p=decimal.Decimal(str(cgst_rate_str).replace('%',''))
    except:
        cgst_p=decimal.Decimal('0')
    try:
        sgst_p=decimal.Decimal(str(sgst_rate_str).replace('%',''))
    except:
        sgst_p=decimal.Decimal('0')
    cgst_amount=(taxable_total*cgst_p/decimal.Decimal('100')).quantize(decimal.Decimal('0.01'))
    sgst_amount=(taxable_total*sgst_p/decimal.Decimal('100')).quantize(decimal.Decimal('0.01'))
    tax_total=(cgst_amount+sgst_amount).quantize(decimal.Decimal('0.01'))
    grand_total=(taxable_total + tax_total).quantize(decimal.Decimal('0.01'))
    data['taxable_value']=str(taxable_total)
    data['cgst_amount']=str(cgst_amount)
    data['sgst_amount']=str(sgst_amount)
    data['tax_total']=str(tax_total)
    data['tax_amount_total']='₹' + str(grand_total)
    data['total_amount']='₹' + str(grand_total)
    data['amount_in_words']='Rupees ' + num_to_words(grand_total)
    overlay_path=os.path.join(BASE_DIR,'overlays','overlay_temp.pdf')
    filename=f"Invoice_{uuid.uuid4().hex[:8]}.pdf"
    output_path=os.path.join(OUTPUT_DIR,filename)
    create_overlay_pdf(TEMPLATE_PATH,overlay_path,coords,data,pages=3)
    merge_overlay_with_template(TEMPLATE_PATH,overlay_path,output_path)
    return send_file(output_path,as_attachment=True)
if __name__=='__main__':
    app.run(debug=True,port=5000,host='127.0.0.1')
