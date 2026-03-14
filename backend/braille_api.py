from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess

LOU_TRANSLATE = r"C:\Users\Lenovo\Downloads\liblouis-3.37.0-win64\bin\lou_translate.exe"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        result = subprocess.run(
            [LOU_TRANSLATE, table],
            input=text.encode("utf-8"),
            capture_output=True,
            check=True
        )
        braille_output = result.stdout.decode("utf-8").strip()
        return JSONResponse(content={"braille": braille_output})

    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": e.stderr.decode("utf-8")}, status_code=500)