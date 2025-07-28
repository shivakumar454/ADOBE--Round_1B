import os
import json
import fitz
import re
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "input")

HEADING_PATTERNS = {
    "H1": [r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$"],
    "H2": [r"^[A-Z][a-z]+:$"],
}

def detect_heading(line):
    t = line.strip()
    for lvl, pats in HEADING_PATTERNS.items():
        for pat in pats:
            if re.match(pat, t):
                return lvl
    return None

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    found = []
    for pno, page in enumerate(doc, start=1):
        for L in page.get_text().splitlines():
            if detect_heading(L):
                found.append({"text": L.strip(), "page": pno})
    return found

def extract_section_text(pdf_path, heading_text, page_no):
    doc = fitz.open(pdf_path)
    if not (1 <= page_no <= len(doc)):
        return ""
    lines = doc[page_no - 1].get_text().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if heading_text in l)
    except StopIteration:
        return ""
    excerpt = []
    for L in lines[start + 1:]:
        if not L.strip():
            break
        if detect_heading(L):
            break
        excerpt.append(L.strip())
    return " ".join(excerpt)

def process_collection(coll_dir):
    input_path = os.path.join(coll_dir, "challenge1b_input.json")
    inp = json.load(open(input_path, encoding="utf-8"))
    pdf_dir = os.path.join(coll_dir, "PDFs")
    out = {
        "metadata": {
            "input_documents": [d["filename"] for d in inp["documents"]],
            "persona": inp["persona"]["role"],
            "job_to_be_done": inp["job_to_be_done"]["task"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for d in inp["documents"]:
        path = os.path.join(pdf_dir, d["filename"])
        heads = extract_headings(path)
        for rank, H in enumerate(heads[:2], start=1):
            out["extracted_sections"].append({
                "document": d["filename"],
                "section_title": H["text"],
                "importance_rank": rank,
                "page_number": H["page"]
            })

    for sec in out["extracted_sections"]:
        path = os.path.join(pdf_dir, sec["document"])
        txt = extract_section_text(path, sec["section_title"], sec["page_number"])
        out["subsection_analysis"].append({
            "document": sec["document"],
            "refined_text": txt,
            "page_number": sec["page_number"]
        })

    out_path = os.path.join(coll_dir, "challenge1b_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("✔️  Done:", coll_dir)

if __name__ == "__main__":
    for name in os.listdir(INPUT_DIR):
        folder = os.path.join(INPUT_DIR, name)
        if os.path.isdir(folder) and name.startswith("Collection"):
            process_collection(folder)
