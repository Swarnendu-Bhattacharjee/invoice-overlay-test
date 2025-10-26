# tools/pdf_grid.py
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys

PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else "templates/blank_invoice.pdf"
OUT_PNG = sys.argv[2] if len(sys.argv) > 2 else "templates/blank_invoice_grid.png"
GRID_STEP = int(sys.argv[3]) if len(sys.argv) > 3 else 50  # points step for grid lines

if not os.path.exists(PDF_PATH):
    print("ERROR: PDF not found at", PDF_PATH)
    sys.exit(1)

doc = fitz.open(PDF_PATH)
page = doc.load_page(0)
pix = page.get_pixmap(matrix=fitz.Matrix(2,2))  # render at 2x for clarity
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

page_rect = page.rect
page_w_pts = page_rect.width
page_h_pts = page_rect.height

scale_x = pix.width / page_w_pts
scale_y = pix.height / page_h_pts

draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 12)
except Exception:
    font = ImageFont.load_default()

# Draw vertical grid and x labels
for x_pt in range(0, math.ceil(page_w_pts)+1, GRID_STEP):
    x_px = int(x_pt * scale_x)
    draw.line([(x_px, 0), (x_px, pix.height)], fill=(200,200,200), width=1)
    draw.text((x_px+2, 2), f"{x_pt}", fill=(80,80,80), font=font)

# Draw horizontal grid and y labels (labels show PDF pts)
for y_pt in range(0, math.ceil(page_h_pts)+1, GRID_STEP):
    y_px = int(pix.height - (y_pt * scale_y))
    draw.line([(0, y_px), (pix.width, y_px)], fill=(200,200,200), width=1)
    draw.text((2, y_px-12), f"{y_pt}", fill=(80,80,80), font=font)

# Page size box
box_text = f"Page size (pts): {page_w_pts:.2f} x {page_h_pts:.2f}"
draw.rectangle([(5, pix.height-40), (max(350, 10+len(box_text)*6), pix.height-5)], fill=(255,255,255,200))
draw.text((10, pix.height-34), box_text, fill=(0,0,0), font=font)

os.makedirs(os.path.dirname(OUT_PNG) or ".", exist_ok=True)
img.save(OUT_PNG)
print("Grid image written to:", OUT_PNG)
print("Page size (points):", page_w_pts, page_h_pts)

