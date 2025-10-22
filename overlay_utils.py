from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
def _ensure_font():
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    except:
        pass
def get_page_size(template_path):
    r=PdfReader(template_path)
    page=r.pages[0]
    return float(page.mediabox.width), float(page.mediabox.height)
def create_overlay_pdf(template_path, overlay_path, coords, data, pages=3):
    w,h=get_page_size(template_path)
    _ensure_font()
    c=Canvas(overlay_path, pagesize=(w,h))
    for p in range(pages):
        for key,meta in coords.items():
            if key.startswith('_'): continue
            x=meta.get('x',0); y=meta.get('y',0)
            size=int(meta.get('size',10))
            align=meta.get('align','left')
            text=str(data.get(key,''))
            c.setFont('DejaVuSans',size)
            if align=='center':
                width=pdfmetrics.stringWidth(text,'DejaVuSans',size)
                c.drawString(x-width/2,y,text)
            elif align=='right':
                width=pdfmetrics.stringWidth(text,'DejaVuSans',size)
                c.drawString(x-width,y,text)
            else:
                c.drawString(x,y,text)
        c.showPage()
    c.save()
def merge_overlay_with_template(template_path, overlay_path, out_path):
    t=PdfReader(template_path)
    o=PdfReader(overlay_path)
    w=PdfWriter()
    for i,page in enumerate(t.pages):
        if i < len(o.pages):
            page.merge_page(o.pages[i])
        w.add_page(page)
    with open(out_path,'wb') as f:
        w.write(f)
