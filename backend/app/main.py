import re
import io
import fitz  # PyMuPDF
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import pytesseract
import gradio as gr
 
# Download NLTK stopwords
nltk.download("stopwords")
 
# ------------------- Helper Functions -------------------
 
def preprocess(text):
    """Clean and tokenize text."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in text.split() if word not in stop_words])
 
def extract_text_from_pdf(file_bytes):
    """Extract text from a PDF, using OCR if needed."""
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text().strip()
            if page_text:
                text += page_text + "\n"
            else:
                # Use OCR if no text is found
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                text += pytesseract.image_to_string(img) + "\n"
    except Exception as e:
        return f"Error extracting text: {e}"
    return text
 
def detect_doc_type(data):
    """Determine if input is a resume or job application."""
    if isinstance(data, str):
        return "resume"
    elif isinstance(data, pd.DataFrame):
        lower_cols = {col.lower() for col in data.columns}
        if {"job_title", "job_description"}.issubset(lower_cols):
            return "job_application"
    return None
 
def create_document_object(data, id_prefix, file_name):
    """Create structured object from resume or job data."""
    doc_type = detect_doc_type(data)
 
    if doc_type == "resume":
        clean_text = preprocess(data)
        return {
            "id": f"{id_prefix}_resume",
            "title": file_name,
            "raw_text": data,
            "clean_text": clean_text,
            "privacy_info": None
        }, doc_type
 
    elif doc_type == "job_application":
        job_objects = []
        data = data.head(1000)
        for idx, row in data.iterrows():
            jd = str(row.get("job_description", "")).strip()
            jt = str(row.get("job_title", "")).strip()
            if not jd or not jt:
                continue
            job_objects.append({
                "id": f"{id_prefix}_job_{idx}",
                "title": jt,
                "raw_text": jd,
                "clean_text": preprocess(jd),
                "privacy_info": None
            })
        return job_objects, doc_type
 
    return None, None
 
def embed_texts(text_list):
    """Generate sentence embeddings for a list of texts."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text_list, convert_to_tensor=False)
 
def rank_similar_jobs(query_vector, job_vectors):
    """Rank job descriptions based on similarity to the resume vector."""
    scores = cosine_similarity([query_vector], job_vectors)[0]
    return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
 
# ------------------- Main Logic -------------------
 
def process_files(resume_files, job_file):
    data_store = {"resumes": [], "job_applications": []}
 
    # --- Process job file ---
    if not job_file:
        return "Please upload a job application file.", ""
    try:
        if job_file.name.lower().endswith(".csv"):
            job_data = pd.read_csv(job_file)
        else:
            job_data = pd.read_excel(job_file)
    except Exception as e:
        return f"Failed to read job file: {e}", ""
 
    jobs_obj, job_type = create_document_object(job_data, "job", job_file.name)
    if job_type != "job_application":
        return "Job file must contain columns: job_title and job_description.", ""
    data_store["job_applications"].extend(jobs_obj)
 
    # --- Process resume files ---
    if not resume_files:
        return "Please upload at least one resume PDF.", ""
 
    for i, resume_file in enumerate(resume_files):
      try:
        with open(resume_file.name, "rb") as f:
            content = f.read()
        resume_text = extract_text_from_pdf(content)
        resume_obj, doc_type = create_document_object(resume_text, f"resume_{i+1}", resume_file.name)
        if doc_type == "resume":
            data_store["resumes"].append(resume_obj)
        else:
            return f"File {resume_file.name} is not recognized as a resume.", ""
      except Exception as e:
        return f"Error processing file {resume_file.name}: {e}", ""
 
 
    # --- Compute Embeddings ---
    job_vectors = embed_texts([job["clean_text"] for job in data_store["job_applications"]])
 
    # --- Match resumes to jobs ---
    results_output = ""
    for resume in data_store["resumes"]:
        resume_vec = embed_texts([resume["clean_text"]])[0]
        ranked_jobs = rank_similar_jobs(resume_vec, job_vectors)[:3]
        results_output += f"Resume: {resume['title']}\n"
        for idx, score in ranked_jobs:
            job = data_store["job_applications"][idx]
            results_output += f"  → Job: {job['title']} | Similarity: {score:.4f}\n"
        results_output += "\n"
 
    return "✅ Matching Completed Successfully", results_output
 
# ------------------- Gradio UI -------------------
 
iface = gr.Interface(
    fn=process_files,
    inputs=[
        gr.File(label="Upload Resumes (PDF)", file_types=[".pdf"], file_count="multiple"),
        gr.File(label="Upload Job Descriptions (CSV or Excel)", file_types=[".csv", ".xlsx", ".xls"])
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Textbox(label="Top Matches", lines=20)
    ],
    title="AI-Powered Resume & Job Matching System",
    description="Upload multiple resumes and a job description file. The system matches each resume to the most relevant job roles using NLP embeddings."
)
 
if __name__ == "__main__":
    iface.launch()
 
 