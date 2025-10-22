#!/bin/bash
source venv/bin/activate
pip install -r requirements.txt
python3 main.py \
--template templates/blank_invoice.pdf \
--coords overlays/coordinates.json \
--data overlays/sample_data.json \
--out output/Invoice_0001.pdf
