# AI-Powered Resume & Job Matching System

An intelligent recruitment tool that matches resumes to job descriptions using semantic NLP embeddings, skill gap analysis, and multi-job ranking — built with Hugging Face Transformers and Gradio.

---

## What It Does

Most resume matching tools just search for keyword overlap. This system uses **sentence embeddings** to understand the *meaning* behind both the resume and job description — matching candidates to roles even when exact keywords don't align.

### Features
- **Semantic Matching** — Uses `all-MiniLM-L6-v2` sentence embeddings and cosine similarity to score resume-job compatibility beyond simple keyword matching
- **Skill Gap Analysis** — Identifies exactly which skills from the job description are present in the resume and which are missing
- **Multi-Job Ranking** — Upload one resume against multiple job descriptions and get a ranked list of best-fit roles
- **PDF Support with OCR Fallback** — Extracts text from any PDF resume, including scanned documents using OCR
- **Batch Resume Processing** — Upload and evaluate multiple resumes simultaneously

---

## How to Use

### Input
| Field | Format | Description |
|---|---|---|
| Resumes | PDF (multiple) | Candidate resumes to evaluate |
| Job Descriptions | CSV or Excel | Must contain `job_title` and `job_description` columns |

### Output
- Similarity score for each resume-job pair
- Top 3 matched jobs per resume
- Skill gap breakdown: matched skills vs missing skills

### Job Description File Format
Your CSV/Excel file must have these columns:
```
job_title          | job_description
-------------------|-----------------------------
Data Scientist     | We are looking for...
NLP Engineer       | Strong Python and NLP...
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` |
| Similarity | `scikit-learn` cosine similarity |
| PDF Extraction | `PyMuPDF (fitz)` + `pytesseract` OCR |
| NLP Preprocessing | `NLTK` — tokenization, stopword removal |
| UI | `Gradio` |
| Language | Python 3.10+ |

---

## Installation & Local Run

```bash
# Clone the repository
git clone https://github.com/your-username/resume-job-matcher
cd resume-job-matcher

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open `http://localhost:7860` in your browser.

---

## Requirements

```
gradio
sentence-transformers
scikit-learn
pandas
nltk
pymupdf
pytesseract
Pillow
openpyxl
```

---

## How It Works

```
Resume PDF → Text Extraction → Preprocessing → Embedding Vector
                                                        ↓
Job Description CSV → Preprocessing → Embedding Vectors → Cosine Similarity → Ranked Results
                                                        ↓
                                              Skill Gap Analysis
```

1. **Text Extraction** — Resume text is extracted from PDF. If the PDF is scanned/image-based, OCR is applied automatically.
2. **Preprocessing** — Text is lowercased, punctuation removed, and stopwords filtered.
3. **Embedding** — Both resume and job description texts are converted to dense semantic vectors using `all-MiniLM-L6-v2`.
4. **Similarity Scoring** — Cosine similarity is computed between the resume vector and all job vectors.
5. **Skill Gap Analysis** — A curated skills dictionary is used to extract and compare skills present in both documents.
6. **Ranking** — Jobs are sorted by similarity score and the top matches are returned with explanations.

---

## Example Output

```
Resume: john_doe_resume.pdf
  → Job: NLP Engineer        | Similarity: 0.8921
      Matched Skills: python, nlp, transformers, fastapi
      Missing Skills: docker, aws, kubernetes

  → Job: Data Scientist      | Similarity: 0.7643
      Matched Skills: python, scikit-learn, pandas
      Missing Skills: spark, tableau, sql

  → Job: ML Engineer         | Similarity: 0.7102
      Matched Skills: python, pytorch, machine learning
      Missing Skills: mlflow, docker, terraform
```

---

## Roadmap

- [ ] Upgrade to `BAAI/bge-large-en-v1.5` for improved domain accuracy
- [ ] Resume improvement suggestions based on job description
- [ ] ATS compatibility score
- [ ] Interactive web dashboard with visual skill charts
- [ ] REST API endpoint for integration with recruitment platforms

---

## Author

**Omar Zbadani** — AI & Data Science Engineer

---

## License

This project is open source and available under the [MIT License](LICENSE).
