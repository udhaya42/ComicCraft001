from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from fpdf import FPDF
from PIL import Image

BASE_DIR=Path(__file__).resolve().parents[2]
EXPORT_DIR=BASE_DIR/"static"/"exports"; EXPORT_DIR.mkdir(parents=True,exist_ok=True)

def save_pdf(layout, title="ComicCraft Comic"):
    out=EXPORT_DIR/f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf=FPDF(); pdf.set_auto_page_break(auto=True,margin=15)
    for p in layout:
        pdf.add_page(); pdf.set_font("Helvetica","B",18)
        pdf.multi_cell(0,10,f"Panel {p['panel_number']}: {p['title']}"); pdf.ln(2)
        img=BASE_DIR/urlparse(p["image_path"]).path.lstrip("/")
        if not img.exists(): raise FileNotFoundError(f"Panel image missing: {img}")
        with Image.open(img) as im: w,h=im.size
        scale=min(180/w,115/h); pdf.image(str(img),w=w*scale,h=h*scale); pdf.ln(5)
        pdf.set_font("Helvetica","I",10); pdf.multi_cell(0,6,p["scene_description"]); pdf.ln(2)
        pdf.set_font("Helvetica","B",11); pdf.multi_cell(0,7,p["caption"])
        pdf.set_font("Helvetica","",11); pdf.multi_cell(0,7,p["narration"])
    pdf.output(str(out)); return f"/static/exports/{out.name}"
