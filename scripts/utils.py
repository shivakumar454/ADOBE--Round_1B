import fitz   
import re

HEADING_PATTERNS = {
    "H1": [
        r'^(?:[A-Z][a-z]+)(?:\s+[A-Z][a-z]+)+$',
    ],
    "H2": [
        r'^[A-Z][a-z]+$',
    ],
    "H3": [
        r'.+:\s*$',
    ]
}

def detect_heading(text_line):
    clean = text_line.strip()
    for level, patterns in HEADING_PATTERNS.items():
        for pat in patterns:
            if re.match(pat, clean):
                print(f" [DEBUG] Matched {level}: “{clean}”")
                return level
    return None

def extract_headings_from_pdf(pdf_path):
    print(f"\n [DEBUG] Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        for line in page.get_text().splitlines():
            if line.strip():
                level = detect_heading(line)
                if level:
                    sections.append({
                        "level": level,
                        "text": line.strip(),
                        "page": page_num
                    })

    print(f" [DEBUG] Total headings found: {len(sections)}\n")
    return sections
