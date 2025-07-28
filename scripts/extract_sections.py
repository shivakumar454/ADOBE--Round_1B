import os
import json
from datetime import datetime
from utils import extract_headings_from_pdf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "../input")
OUTPUT_DIR = os.path.join(BASE_DIR, "../output")
PDF_DIR = os.path.join(INPUT_DIR, "pdfs")
INPUT_JSON = os.path.join(INPUT_DIR, "challenge1b_input.json")
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "challenge1b_output.json")

def load_input():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_output(input_data):
    metadata = {
        "input_documents": [doc["filename"] for doc in input_data["documents"]],
        "persona": input_data["persona"]["role"],
        "job_to_be_done": input_data["job_to_be_done"]["task"],
        "processing_timestamp": datetime.now().isoformat()
    }

    extracted_sections = []

    for doc in input_data["documents"]:
        pdf_path = os.path.join(PDF_DIR, doc["filename"])
        print(f"🔍 Extracting from: {doc['filename']}")

        try:
            headings = extract_headings_from_pdf(pdf_path)

            for rank, section in enumerate(headings[:2], start=1):   
                extracted_sections.append({
                    "document": doc["filename"],
                    "section_title": section["text"],
                    "importance_rank": rank,
                    "page_number": section["page"]
                })

        except Exception as e:
            print(f" Failed to process {doc['filename']}: {e}")

    return {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": []
    }

def save_output(output_data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_data = load_input()
    output_data = generate_output(input_data)
    save_output(output_data)
    print(" Extraction complete! Output written to:", OUTPUT_JSON)
