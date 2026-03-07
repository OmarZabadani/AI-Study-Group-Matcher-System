import gradio as gr
from backend.app.resume_parser import extract_text_from_pdf
from backend.app.job_loader import load_job_file
from backend.app.matcher import rank_jobs
from backend.app.models.embedding_model import load_model
from backend.app.explanation_engine import generate_explanation

model = load_model()

def process_files(resume_files, job_file):
    # Load jobs
    jobs = load_job_file(job_file)

    results = ""
    for resume_file in resume_files:
        with open(resume_file.name, "rb") as f:
            resume_text = extract_text_from_pdf(f.read())
        ranked_jobs = rank_jobs(resume_text, jobs, model)[:3]

        for job, score in ranked_jobs:
            explanation = generate_explanation(resume_text, job)
            results += f"Resume: {resume_file.name}\n"
            results += f"Job: {job['title']} | Score: {score:.2f}\n"
            results += f"Matched Skills: {explanation['matched_skills']}\n"
            results += f"Missing Skills: {explanation['missing_skills']}\n\n"
    return results

iface = gr.Interface(
    fn=process_files,
    inputs=[
        gr.File(file_types=[".pdf"], file_count="multiple", label="Upload Resumes"),
        gr.File(file_types=[".csv",".xlsx"], label="Upload Jobs")
    ],
    outputs=gr.Textbox(label="Top Matches", lines=20)
)

if __name__ == "__main__":
    iface.launch()