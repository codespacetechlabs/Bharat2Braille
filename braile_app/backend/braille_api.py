from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # 🔹 Import CORS middleware
import subprocess

app = FastAPI()

# 🔹 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use ["*"] to allow all origins (less secure)
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

@app.get("/braille/")
def convert_to_braille(
    text: str = Query(..., min_length=1),
    table: str = Query("hi-in-g1.utb")
):
    if table not in SUPPORTED_TABLES:
        return JSONResponse(content={"error": f"Unsupported language table: {table}"}, status_code=400)

    try:
        # Translate text to Braille using liblouis
        result = subprocess.run(
            ["lou_translate", table],
            input=text,
            text=True,
            capture_output=True,
            check=True
        )
        braille_output = result.stdout.strip()

        return JSONResponse(content={"braille": braille_output})

    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": e.stderr}, status_code=500)
