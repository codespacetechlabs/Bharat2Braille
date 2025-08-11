from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import subprocess
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from fastapi.middleware.cors import CORSMiddleware
from reportlab.pdfbase.ttfonts import TTFont
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update if your frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_TABLES = {
    "hi-in-g1.utb": "Hindi",
    "ta-in-g1.utb": "Tamil",
    "ml-in-g1.utb": "Malayalam",
    "mr-in-g1.utb": "Marathi",
    "bn-in-g1.utb": "Bengali",
    "gu-in-g1.utb": "Gujarati"
}

PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

FONT_PATH = "fonts/NotoSansSymbols2-Regular.ttf"
FONT_NAME = "NotoSansSymbols2"
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

@app.get("/braille/pdf")
def convert_to_braille_pdf(
    text: str = Query(..., min_length=1),
    table: str = Query("hi-in-g1.utb")
):
    if table not in SUPPORTED_TABLES:
        return {"error": f"Unsupported language table: {table}"}

    try:
        # Convert to Braille using liblouis
        result = subprocess.run(
            ["lou_translate", table],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        braille_output = result.stdout.strip()

        # Create PDF
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)

        c = canvas.Canvas(pdf_path)
        c.setFont(FONT_NAME, 18)
        c.drawString(100, 750, braille_output)
        c.save()

        return FileResponse(
            path=pdf_path,
            filename="braille_output.pdf",
            media_type="application/pdf"
        )

    except subprocess.CalledProcessError as e:
        return {"error": e.stderr}
