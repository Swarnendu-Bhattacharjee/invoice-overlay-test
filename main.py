import json
import argparse
from overlay_utils import create_overlay_pdf, merge_overlay_with_template

def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--template', required=True)
    p.add_argument('--coords', required=True)
    p.add_argument('--data', required=True)
    p.add_argument('--out', required=True)
    args=p.parse_args()
    coords=load_json(args.coords)
    data=load_json(args.data)
    overlay_path='overlays/overlay_temp.pdf'
    create_overlay_pdf(args.template, overlay_path, coords, data, pages=3)
    merge_overlay_with_template(args.template, overlay_path, args.out)

if __name__=='__main__':
    main()
