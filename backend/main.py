from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from braille_api import app as braille_app
from braille_pdf_api import app as braille_pdf_app

app = FastAPI(title="Bharti2Braille API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api/braille", braille_app)
app.mount("/api/pdf", braille_pdf_app)


@app.get("/")
def root():
    return {
        "message": "Bharti2Braille API is running",
        "endpoints": {
            "braille_text": "/api/braille/braille/",
            "braille_pdf": "/api/pdf/braille/pdf",
        },
    }