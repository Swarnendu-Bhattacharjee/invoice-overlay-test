import fitz
import os
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image
import io

st.set_page_config(page_title="PDF Coordinate Picker", layout="wide")
st.title("📍 PDF Coordinate Picker (Click to get coordinates)")

# --- Auto-detect invoice template path ---
possible_paths = [
    "templates/blank_invoice.pdf",
    "/home/swarnendu/innovative-bill/templates/blank_invoice.pdf",
    "/home/swarnendu/invoice-overlay-test/templates/blank_invoice.pdf"
]

PDF_PATH = None
for path in possible_paths:
    if os.path.exists(path):
        PDF_PATH = path
        break

if PDF_PATH is None:
    st.error("❌ No 'blank_invoice.pdf' found in standard locations.")
    uploaded = st.file_uploader("Upload your invoice PDF", type=["pdf"])
    if uploaded:
        temp_path = "/tmp/temp_invoice.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded.read())
        PDF_PATH = temp_path

if PDF_PATH is None:
    st.stop()

st.success(f"✅ Using PDF: {PDF_PATH}")
doc = fitz.open(PDF_PATH)
page = doc.load_page(0)
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
page_w_pts, page_h_pts = page.rect.width, page.rect.height
scale_x = pix.width / page_w_pts
scale_y = pix.height / page_h_pts

st.caption(f"Page size: {page_w_pts:.2f} × {page_h_pts:.2f} points")
st.info("🖱️ Click on the image to get precise PDF coordinates (bottom-left origin).")

# --- Floating tooltip to show coordinates near cursor ---
st.markdown(
    """
    <style>
    .tooltip {
        position: fixed;
        background: rgba(0,0,0,0.75);
        color: white;
        padding: 4px 7px;
        border-radius: 4px;
        font-size: 13px;
        pointer-events: none;
        z-index: 9999;
        display: none;
    }
    </style>

    <div id="tooltip" class="tooltip"></div>

    <script>
    const tooltip = document.getElementById('tooltip');
    document.addEventListener('mousemove', function(e) {
        tooltip.style.left = (e.pageX + 15) + 'px';
        tooltip.style.top = (e.pageY - 20) + 'px';
    });

    const coordBox = document.querySelector('[data-testid="stMarkdownContainer"]');
    const observer = new MutationObserver(() => {
        const coordText = coordBox?.innerText?.match(/X\\s*=\\s*([0-9.]+)\\s*,\\s*Y\\s*=\\s*([0-9.]+)/);
        if (coordText) {
            tooltip.innerText = `X: ${coordText[1]}, Y: ${coordText[2]}`;
            tooltip.style.display = 'block';
        } else {
            tooltip.style.display = 'none';
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """,
    unsafe_allow_html=True,
)


# this component handles clicks automatically
coord = streamlit_image_coordinates(img, key="coord_picker")

if coord is not None:
    x_px = coord["x"]
    y_px = coord["y"]
    pdf_x = x_px / scale_x
    pdf_y = page_h_pts - (y_px / scale_y)
    st.success(f"📍 PDF Coordinates: X = {pdf_x:.2f} , Y = {pdf_y:.2f}")
    st.code(f'"field_name": {{"x": {pdf_x:.2f}, "y": {pdf_y:.2f}, "font_size": 10, "align": "left"}}', language="json")

st.markdown(
    """
    <style>
    .tooltip {
        position: fixed;
        background: rgba(0,0,0,0.75);
        color: white;
        padding: 4px 7px;
        border-radius: 4px;
        font-size: 13px;
        pointer-events: none;
        z-index: 9999;
        display: none;
    }
    </style>

    <div id="tooltip" class="tooltip"></div>

    <script>
    const tooltip = document.getElementById('tooltip');
    document.addEventListener('mousemove', function(e) {
        tooltip.style.left = (e.pageX + 15) + 'px';
        tooltip.style.top = (e.pageY - 20) + 'px';
    });

    const coordBox = document.querySelector('[data-testid="stMarkdownContainer"]');
    const observer = new MutationObserver(() => {
        const coordText = coordBox?.innerText?.match(/X\\s*=\\s*([0-9.]+)\\s*,\\s*Y\\s*=\\s*([0-9.]+)/);
        if (coordText) {
            tooltip.innerText = `X: ${coordText[1]}, Y: ${coordText[2]}`;
            tooltip.style.display = 'block';
        } else {
            tooltip.style.display = 'none';
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """,
    unsafe_allow_html=True,
)
