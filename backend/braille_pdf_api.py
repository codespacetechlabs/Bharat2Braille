from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
import subprocess, uuid, os, regex

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# =========================
# Fonts
# =========================
DEV_FONT_NAME = "Devanagari"
BRAILLE_FONT_NAME = "Braille"

pdfmetrics.registerFont(TTFont(DEV_FONT_NAME, "fonts/NotoSansDevanagari-Regular.ttf"))
pdfmetrics.registerFont(TTFont(BRAILLE_FONT_NAME, "fonts/NotoSansSymbols2-Regular.ttf"))

# =========================
# Helpers
# =========================
def mm_to_pt(mm: float) -> float:
    return mm * 72.0 / 25.4

def liblouis_translate(text: str, table: str) -> str:
    """
    Use liblouis (cli) to translate Devanagari to Braille.
    """
    res = subprocess.run(
        ["lou_translate", table],
        input=text,
        text=True,
        capture_output=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"liblouis translation failed: {res.stderr.strip()}")
    return res.stdout.strip()

def split_braille_cells(braille: str):
    """
    Prefer splitting on spaces if liblouis emits space-separated cells;
    otherwise fall back to per-character (each dot pattern).
    """
    parts = [p for p in braille.split(" ") if p != ""]
    if len(parts) > 1:
        return parts
    return [ch for ch in braille if not ch.isspace()]

# --- Devanagari akshara decomposition ---
# Unicode blocks/ranges used in logic
DEVANAGARI_START = 0x0900
DEVANAGARI_END   = 0x097F
VIRAMA           = "\u094D"

# Dependent vowels (matras)
DEPENDENT_VOWELS = set(chr(c) for c in range(0x093E, 0x094D))  # 093E..094C
# Signs that should stick to preceding akshara
NUKTA            = "\u093C"
ANUSVARA         = "\u0902"
VISARGA          = "\u0903"
CHANDRABINDU     = "\u0901"
AVAGRAHA         = "\u093D"
BINDING_SIGNS    = {NUKTA, ANUSVARA, VISARGA, CHANDRABINDU, AVAGRAHA}

# Independent vowels (standalone aksharas)
INDEPENDENT_VOWELS = set(chr(c) for c in range(0x0904, 0x0915))  # 0904..0914

# Consonants
CONSONANTS = set(chr(c) for c in range(0x0915, 0x093A))  # 0915..0939

# Common ligature → constituent consonants (optional boost for nicer splits)
# This helps cases where shaping might hide explicit virama in source text.
DECOMPOSE_OVERRIDES = {
    # Swaras (Vowels)
    "⠁": "अ",   # a
    "⠃": "आ",   # aa
    "⠊": "इ",   # i
    "⠑": "ई",   # ii
    "⠥": "उ",   # u
    "⠳": "ऊ",   # uu
    "⠌": "ऋ",   # ri
    "⠜": "ए",   # e
    "⠪": "ऐ",   # ai
    "⠕": "ओ",   # o
    "⠕⠃": "औ", # au (sometimes encoded as ⠪⠕ depending on table)

    # Consonants (Vyanjan)
    "⠅": "क",   # ka
    "⠈⠅": "ख", # kha
    "⠛": "ग",   # ga
    "⠈⠛": "घ", # gha
    "⠬": "ङ",   # ṅa

    "⠉": "च",   # ca
    "⠈⠉": "छ", # cha
    "⠚": "ज",   # ja
    "⠈⠚": "झ", # jha
    "⠴": "ञ",   # ña

    "⠞": "ट",   # ṭa
    "⠈⠞": "ठ", # ṭha
    "⠙": "ड",   # ḍa
    "⠈⠙": "ढ", # ḍha
    "⠌⠙": "ण", # ṇa

    "⠞⠁": "त", # ta
    "⠈⠞⠁": "थ", # tha
    "⠙⠁": "द", # da
    "⠈⠙⠁": "ध", # dha
    "⠝": "न",   # na

    "⠏": "प",   # pa
    "⠈⠏": "फ", # pha
    "⠃⠛": "ब", # ba
    "⠈⠃⠛": "भ", # bha
    "⠍": "म",   # ma

    "⠽": "य",   # ya
    "⠗": "र",   # ra
    "⠇": "ल",   # la
    "⠧": "व",   # va
    "⠎": "श",   # śa
    "⠯": "ष",   # ṣa
    "⠓": "ह",   # ha

    # Additional consonants
    "⠟": "क्ष", # kṣa
    "⠽⠛": "ज्ञ", # jña

    # Matras (Vowel signs)
    "⠁": "ा",   # aa matra
    "⠊": "ि",   # i matra
    "⠑": "ी",   # ii matra
    "⠥": "ु",   # u matra
    "⠳": "ू",   # uu matra
    "⠌": "ृ",   # ri matra
    "⠜": "े",   # e matra
    "⠪": "ै",   # ai matra
    "⠕": "ो",   # o matra
    "⠕⠃": "ौ", # au matra

    # Other signs
    "⠂": "ं",   # anusvara
    "⠄": "ः",   # visarga
    "⠆": "ँ",   # chandrabindu
    "⠤": "्",   # halant / virama
    "⠿": "।",   # danda
}


def is_devanagari(ch: str) -> bool:
    cp = ord(ch)
    return DEVANAGARI_START <= cp <= DEVANAGARI_END

def segment_aksharas(text: str):
    """
    Split into grapheme clusters, then decompose conjuncts into constituent
    consonants while keeping dependent vowels and signs with the correct base.

    Output: list of Devanagari aksharas like ["भा","र","त"] or
            ["क","ष","म","ा"] depending on conjuncts.
    """
    # First expand known ligatures using overrides (max munch)
    # We do this on the raw text to expose consonants if shaping hid viramas.
    i = 0
    expanded = []
    while i < len(text):
        matched = False
        # Try longest override (length 2–3 typical)
        for L in (3, 2):
            if i + L <= len(text):
                chunk = text[i:i+L]
                if chunk in DECOMPOSE_OVERRIDES:
                    expanded.extend(DECOMPOSE_OVERRIDES[chunk])
                    i += L
                    matched = True
                    break
        if matched:
            continue
        expanded.append(text[i])
        i += 1

    # Now walk through expanded text building aksharas.
    aksharas = []
    cur = ""  # current akshara being built

    def flush():
        nonlocal cur
        if cur != "":
            aksharas.append(cur)
            cur = ""

    idx = 0
    while idx < len(expanded):
        ch = expanded[idx]

        if not is_devanagari(ch):
            # Non-Devanagari: treat as its own akshara
            flush()
            aksharas.append(ch)
            idx += 1
            continue

        if ch in INDEPENDENT_VOWELS:
            # Independent vowel starts a new akshara
            flush()
            cur = ch
            # attach any following signs (anusvara/visarga/chandrabindu/avagraha)
            j = idx + 1
            while j < len(expanded) and expanded[j] in BINDING_SIGNS:
                cur += expanded[j]
                j += 1
            idx = j
            flush()
            continue

        if ch in CONSONANTS:
            # Start with consonant (may be followed by nukta, matras, virama chain, signs)
            flush()
            cur = ch
            j = idx + 1

            # Nukta immediately after a consonant belongs with it
            if j < len(expanded) and expanded[j] == NUKTA:
                cur += expanded[j]
                j += 1

            # If we have a virama + consonant chain, we SPLIT into separate aksharas.
            # We *do not* keep the virama char (we show base consonants only).
            while j + 1 < len(expanded) and expanded[j] == VIRAMA and expanded[j+1] in CONSONANTS:
                # finalize current consonant akshara (no matras can come before chain ends)
                flush()
                # next consonant becomes new akshara
                cur = expanded[j+1]
                # possible nukta after the new consonant
                k = j + 2
                if k < len(expanded) and expanded[k] == NUKTA:
                    cur += expanded[k]
                    j = k + 1
                else:
                    j = j + 2
                # continue loop to see if more virama+consonant follow
            # After chain ends, attach dependent vowels (matras) and signs
            while j < len(expanded) and (expanded[j] in DEPENDENT_VOWELS or expanded[j] in BINDING_SIGNS):
                cur += expanded[j]
                j += 1

            idx = j
            flush()
            continue

        # Standalone signs or others inside Devanagari block:
        # Attach to previous akshara if possible; else as its own.
        if ch in (DEPENDENT_VOWELS | BINDING_SIGNS):
            if aksharas:
                aksharas[-1] += ch
            else:
                aksharas.append(ch)
            idx += 1
            continue

        # Default fallback
        flush()
        aksharas.append(ch)
        idx += 1

    flush()
    return aksharas

def adapt_to_braille(dev_aksharas, braille_cells):
    """
    Ensure a 1:1 alignment list with braille cells.
    - If fewer aksharas than braille: pad with thin spaces.
    - If more aksharas: merge adjacent aksharas to fit.
    """
    target = len(braille_cells)
    items = list(dev_aksharas)

    if len(items) == target:
        return items

    if not items:
        return ["\u2009"] * target

    if len(items) < target:
        items += ["\u2009"] * (target - len(items))
        return items

    # Merge extras as evenly as possible from left to right
    merged = []
    idx, remain, slots_left = 0, len(items), target
    while idx < len(items) and len(merged) < target:
        extra = remain - slots_left
        take = 1 + (1 if extra > 0 else 0)
        seg = "".join(items[idx:idx+take])
        merged.append(seg)
        idx += take
        remain -= take
        slots_left -= 1

    while len(merged) < target:
        merged.append("\u2009")

    return merged[:target]
# =========================
# Braille → Devanagari Mapping
# =========================
BRAILLE_TO_DEVANAGARI = {
    # Independent vowels (स्वर)
    "⠁": "अ",   # 1
    "⠜": "आ",   # 345
    "⠊": "इ",   # 24
    "⠔": "ई",   # 35
    "⠥": "उ",   # 136
    "⠳": "ऊ",   # 1256
    "⠗": "ऋ",   # 5,1235 (handled as one codepoint here per Bharati usage)
    "⠑": "ए",   # 15
    "⠌": "ऐ",   # 34
    "⠕": "ओ",   # 135
    "⠪": "औ",   # 246

    # Consonants (व्यंजन)
    "⠅": "क",   # 13
    "⠣": "ख",   # 46
    "⠛": "ग",   # 1245
    "⠦": "घ",   # 126
    "⠬": "ङ",   # 346

    "⠉": "च",   # 14
    "⠧": "छ",   # 16
    "⠚": "ज",   # 245
    "⠶": "झ",   # 356
    "⠴": "ञ",   # 25

    "⠾": "ट",   # 23456
    "⠮": "ठ",   # 2456
    "⠙": "ड",   # 1246
    "⠯": "ढ",   # 123456
    "⠻": "ण",   # 3456

    "⠞": "त",   # 2345
    "⠖": "थ",   # 1456
    "⠙⠁": "द", # 145  (table shows 145 for द; some schemas encode d+a to disambiguate)
    "⠷": "ध",   # 2346
    "⠝": "न",   # 1345

    "⠏": "प",   # 1234
    "⠟": "फ",   # 235
    "⠃": "ब",   # 12
    "⠇⠃": "भ", # map 45; using dedicated key below as well
    "⠭": "भ",   # 45
    "⠍": "म",   # 134

    "⠽": "य",   # 13456
    "⠗": "र",   # 1235  (note: same braille cell also used above for ऋ in table; context-sensitive)
    "⠇": "ल",   # 123
    "⠺": "ळ",   # 456
    "⠧": "व",   # 1236

    "⠩": "श",   # 146
    "⠯": "ष",   # 12346
    "⠉⠗": "स", # 234 (see dedicated mapping below)
    "⠣⠁": "ह", # 125 (see dedicated mapping below)
    "⠎": "स",   # 234
    "⠓": "ह",   # 125

    # Nukta and nukta letters
    "⠐": "़",       # nukta (5)
    "⠙⠐": "ड़",    # 095C (1246 + nukta -> 12456)
    "⠯⠐": "ढ़",    # 095D (123456 + nukta -> 5,12456)

    # Signs (चिह्न)
    "⠆": "ँ",   # chandrabindu (3 in table; Bharati cell ⠆ is dots 23—here use per table symbol list)
    "⠂": "ं",   # anusvara (56)
    "⠄": "ः",   # visarga (6)
    "⠤": "्",   # virama/halant (4)
    "⠄⠕": "ऽ",# avagraha (2) — depending keyboard, often ⠂; mapping provided as alias
    "⠐⠳": "ॐ",# OM (5,1256)
    "⠫": "̄",   # anudatta Vedic stress (12356) combining mark

    # Dependent vowel signs ( मात्राएँ )
    "⠜": "ा",   # 093E (345)
    "⠊": "ि",   # 093F (24, visually left-placed)
    "⠔": "ी",   # 0940 (35)
    "⠥": "ु",   # 0941 (136)
    "⠳": "ू",   # 0942 (1256)
    "⠗": "ृ",   # 0943 (5,1235)
    "⠑": "े",   # 0947 (15)
    "⠌": "ै",   # 0948 (34)
    "⠕": "ो",   # 094B (135)
    "⠪": "ौ",   # 094C (246)

    # Additional vowel signs from table
    "⠖": "ॄ",   # 0944 (6,1235) mapped via dedicated key; context may vary
    "⠗⠇": "ॢ", # 0962 (5,123)
    "⠖⠇": "ॣ", # 0963 (6,123)
    "⠖⠗": "ॠ", # 0960 (6,1235) independent vocalic RR
    "⠗⠇⠗": "ॡ",# 0961 (5,123) independent vocalic LL

    # Punctuation
    "⠿": "।",   # danda
    "⠿⠿": "॥", # double danda

    # Digits (use number sign ⠼ then a-j)
    "⠼⠚": "०",  # 0
    "⠼⠁": "१",
    "⠼⠃": "२",
    "⠼⠉": "३",
    "⠼⠙": "४",
    "⠼⠑": "५",
    "⠼⠋": "६",
    "⠼⠛": "७",
    "⠼⠓": "८",
    "⠼⠊": "९",

    # Common conjuncts listed
    "⠟": "क्ष",     # from table entry (also used above as फ in standard; here allocated to क्ष per table)
    "⠽⠛": "ज्ञ",   # jña
    "⠞⠗": "त्र",   # ta + ra (explicit in table)
    "⠩⠗": "श्र",   # śra

    # Aliases to resolve overlaps (context-sensitive in real parser)
    # Prefer consonant + virama + consonant for general conjunct formation.
}



def map_braille_to_devanagari(braille_cells: list[str]) -> list[str]:
    """
    Map each Braille cell into Devanagari using dictionary.
    If no match is found, return the Braille cell as-is.
    """
    out = []
    for cell in braille_cells:
        out.append(BRAILLE_TO_DEVANAGARI.get(cell, cell))
    return out

# =========================
# Endpoint
# =========================
@app.get("/braille/pdf")
def make_pdf(
    text: str = Query(..., min_length=1),
    table: str = Query("hi-in-g1.utb"),
    debug: bool = Query(False)
):
    # 1) Liblouis → Braille
    braille_out = liblouis_translate(text, table)
    braille_cells = split_braille_cells(braille_out)

    # 2) Map Braille → Devanagari letters
    dev_slots = map_braille_to_devanagari(braille_cells)

    # 3) PDF setup (unchanged)
    pdf_path = os.path.join(PDF_DIR, f"{uuid.uuid4().hex}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    left_margin = mm_to_pt(20)
    right_margin = mm_to_pt(20)
    usable_width = width - left_margin - right_margin

    top_y = height - mm_to_pt(60)
    line_gap = mm_to_pt(28)

    DEV_SIZE = 28   # smaller Hindi
    BRL_SIZE = 20   # Braille stays same

    # Colors with adjusted transparency
    braille_gray = Color(0, 0, 0, alpha=0.8)   # more visible Braille
    hindi_gray   = Color(0, 0, 0, alpha=0.5)   # lighter Hindi

    x = left_margin
    y = top_y

    for hc, bc in zip(dev_slots, braille_cells):
        cell_w = max(
            pdfmetrics.stringWidth(hc, DEV_FONT_NAME, DEV_SIZE),
            pdfmetrics.stringWidth(bc, BRAILLE_FONT_NAME, BRL_SIZE),
            mm_to_pt(6)
        )

        if x + cell_w > left_margin + usable_width:
            x = left_margin
            y -= line_gap

        cx = x + cell_w / 2.0

        # Draw Hindi (bottom, lighter + smaller)
        c.setFont(DEV_FONT_NAME, DEV_SIZE)
        c.setFillColor(hindi_gray)
        c.drawCentredString(cx, y, hc)

        # Draw Braille (top, darker + slightly transparent)
        c.setFont(BRAILLE_FONT_NAME, BRL_SIZE)
        c.setFillColor(braille_gray)
        c.drawCentredString(cx, y, bc)

        if debug:
            c.setStrokeGray(0.85)
            c.rect(x, y - DEV_SIZE, cell_w, DEV_SIZE * 1.9, stroke=1, fill=0)

        x += cell_w + mm_to_pt(5)


    c.save()
    return FileResponse(pdf_path, media_type="application/pdf", filename="braille_overlay.pdf")
