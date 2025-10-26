---

### 🧾 **README.md — Invoice Overlay Test**

```markdown
# 📍 Invoice Overlay Calibration Utility

### Overview
The **Invoice Overlay Test** project provides an advanced interface for **PDF coordinate calibration** and **overlay testing** for invoice generation systems.  
It enables precise mapping of text and field coordinates (customer name, invoice number, amount, etc.) on a base PDF layout — such as company invoice templates — to ensure **pixel-perfect rendering** of generated invoices.

---

## 🚀 Features

- **Interactive Coordinate Picker:**  
  Built using `Streamlit` and `PyMuPDF (fitz)` for real-time coordinate detection on static PDF templates.

- **Seamless Integration with Invoice Engines:**  
  Directly compatible with the **PIPL Accounting System** and any other `wkhtmltopdf`/`pdfkit`-based PDF renderer.

- **Dynamic Template Validation:**  
  Provides visual coordinate testing before committing final coordinates into production templates.

- **Non-destructive Testing Environment:**  
  The overlay calibration does **not modify original templates**, maintaining integrity of design assets.

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| UI Framework | [Streamlit](https://streamlit.io/) | Interactive web interface |
| PDF Engine | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) | PDF rendering and coordinate extraction |
| Image Processing | [Pillow (PIL)](https://python-pillow.org/) | Conversion of PDF to interactive images |
| State Handling | `streamlit-image-coordinates` | Coordinate fetching and event mapping |
| Deployment | Local / WSL Environment | Debug, preview and overlay testing |

---

## 🧠 Functional Architecture

```

+---------------------------+
|   blank_invoice.pdf       |
|   (Static Template)       |
+------------+--------------+
|
v
+---------------------------+
| PDF to Image (fitz, PIL)  |
|  → Render page visually   |
+------------+--------------+
|
v
+---------------------------+
| Streamlit Interactive App |
|  → Capture mouse clicks   |
|  → Display (x, y) coords  |
|  → Log coordinates         |
+------------+--------------+
|
v
+---------------------------+
| Export / Apply Coordinates |
|  → Used in final overlay   |
|  → Map onto invoice fields |
+---------------------------+

````

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Swarnendu-Bhattacharjee/invoice-overlay-test.git
cd invoice-overlay-test
````

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux / macOS
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Access the app locally at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 📂 Directory Structure

```
invoice-overlay-test/
├── app.py                          # Main Streamlit application
├── templates/
│   └── blank_invoice.pdf           # Reference invoice layout for calibration
├── static/
│   └── samples/                    # Optional visual test outputs
├── requirements.txt                # Dependency list
└── README.md                       # Project documentation
```

---

## 🔧 Configuration Parameters

| Variable      | Description                                         | Default                       |
| ------------- | --------------------------------------------------- | ----------------------------- |
| `PDF_PATH`    | Absolute or relative path to the target invoice PDF | `templates/blank_invoice.pdf` |
| `PAGE_NUMBER` | PDF page index (0-indexed)                          | `0`                           |
| `ZOOM_LEVEL`  | Rendering zoom ratio (for high-res templates)       | `2.0`                         |

---

## 🧪 Usage Workflow

1. Launch the Streamlit app.
2. Click anywhere on the invoice layout to get `(x, y)` coordinates.
3. Copy and save these coordinates to your invoice template configuration (`overlay_config.json` or `utils.py`).
4. Test generated invoices in the PIPL Accounting System with verified alignment.

---

## 📊 Example Output

```
Clicked at (x=172.3, y=415.8)
Clicked at (x=398.5, y=732.6)
```

These coordinate pairs correspond to **fields like name, date, amount, or QR location** within the invoice layout.

---

## 🛠 Troubleshooting

| Issue                                | Possible Cause                  | Resolution                                                    |
| ------------------------------------ | ------------------------------- | ------------------------------------------------------------- |
| `Permission denied` when opening PDF | WSL path or file not accessible | Move file under `/home/<user>/invoice-overlay-test/templates` |
| Blank Streamlit screen               | Missing dependency              | Run `pip install streamlit_image_coordinates`                 |
| PDF not rendering                    | Incorrect path or corrupt file  | Verify file path and re-export PDF                            |

---

## 🧩 Future Enhancements

* Multi-page coordinate calibration
* Overlay preview with field labels
* JSON export for auto-integration into template engines
* Batch calibration for multiple templates

---

## 🧾 License

This project is proprietary and maintained under **Panchmahal Insulations Pvt. Ltd. (R&D Division)**.
All usage and redistribution must adhere to internal developer policies.

---

## 👨‍💻 Maintainer

**Swarnendu Bhattacharjee (Sentinel)**
Developer, AI & Backend Systems — *PIPL Accounting Software Division*
📧 [Contact available on GitHub Profile](https://github.com/Swarnendu-Bhattacharjee)

````

---


