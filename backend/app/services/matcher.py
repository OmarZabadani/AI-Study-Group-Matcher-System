from models.embedding_model import load_model, get_embeddings
from utils.similarity import cosine_sim

def rank_jobs(resume_text, job_objects, model):
    resume_vec = get_embeddings(model, [resume_text])[0]
    job_vecs = get_embeddings(model, [job["clean_text"] for job in job_objects])
    
    scores = cosine_sim(resume_vec, job_vecs)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(job_objects[i], score) for i, score in ranked]