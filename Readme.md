       Adobe Hackathon 2025 – Round 1B  
### *Persona-Driven Document Intelligence*

---

## 🎯 Objective

Build a smart PDF processor that extracts and ranks the most **relevant sections and subsections** from a **collection of PDFs** based on:

- A given **persona**
- A clearly defined **job-to-be-done**

The goal is to enable intelligent document summarization and analysis based on user intent.

---

## 🔄 Processing Pipeline (Overall Flow)

###   Step 1: Extract Relevant Sections (`extract_sections.py`)
- For each PDF in the input collection:
  - Analyze headings using text style cues (boldness, casing, position)
  - Select top 1–2 most relevant **section headings**
  - Save them with page number and importance rank

###   Step 2: Subsection Refinement (`analyze_subsections.py`)
- For each top-ranked section:
  - Extract full page text from the PDF
  - Store it as refined text for deeper context

###   Step 3: Combine & Save Output
- `challenge1b_output.json` is created in the same input folder
- Contains:
  -  Metadata (persona, job-to-be-done, doc list)
  -  Extracted sections with ranks
  -  Subsection text snippets

---

## 💻 How to Run the Code Locally (Python)

Make sure you have **Python 3.10+** installed.

```bash
# 1. Install required packages

pip install -r requirements.txt

# 2. Run the processing pipeline

python run_all_collections.py
```

This will:
- Automatically go through all folders under `input/`
- Generate a `challenge1b_output.json` inside each collection folder

---

##   How to Run with Docker

###   Build Docker Image

```bash
docker build -t round1b .
```

###   Run the Docker Container

#### For Windows (PowerShell):

```bash
docker build -t round1b .
```

```bash
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" round1b
```

#### For Windows (CMD):
```cmd
docker run --rm -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" round1b
```

#### For macOS/Linux:
```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" round1b
```

---
 

Built for Round 1B of Adobe Hackathon 2025 – Empowering intelligent PDF understanding!
