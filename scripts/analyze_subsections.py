import os
import json
import fitz   

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "../output/challenge1b_output.json")
PDF_DIR = os.path.join(BASE_DIR, "../input/pdfs")

def extract_text_from_page(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    if 0 <= page_number - 1 < len(doc):
        return doc[page_number - 1].get_text().strip()
    return ""

def analyze_subsections(data):
    analysis = []

    for section in data.get("extracted_sections", []):
        doc_name = section["document"]
        page_number = section["page_number"]
        pdf_path = os.path.join(PDF_DIR, doc_name)

        text = extract_text_from_page(pdf_path, page_number)

        analysis.append({
            "document": doc_name,
            "refined_text": text,
            "page_number": page_number
        })

    return analysis

def update_json_file(analysis):
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["subsection_analysis"] = analysis

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(" Subsection analysis added successfully!")

if __name__ == "__main__":
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    analysis = analyze_subsections(output_data)
    update_json_file(analysis)
