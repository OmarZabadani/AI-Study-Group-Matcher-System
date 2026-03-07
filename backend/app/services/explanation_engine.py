# services/explanation_engine.py

from .skill_extractor import extract_skills_from_text, compare_skills

def generate_match_explanation(resume_text, job_object, top_n_skills=20):
    """
    Generate a human-readable explanation of how a resume matches a job.

    Args:
        resume_text (str): Text extracted from a resume
        job_object (dict): Job data with keys 'title' and 'raw_text'
        top_n_skills (int): Number of top keywords to extract as skills

    Returns:
        dict: Explanation including matched/missing skills and match score
    """
    # Extract dynamic skills
    resume_skills = extract_skills_from_text(resume_text, top_n=top_n_skills)
    job_skills = extract_skills_from_text(job_object["raw_text"], top_n=top_n_skills)

    # Compare skills
    matched, missing = compare_skills(resume_skills, job_skills)

    # Compute a simple match score based on skills overlap
    match_score = (len(matched) / len(job_skills) * 100) if job_skills else 0

    # Prepare explanation dictionary
    explanation = {
        "job_title": job_object.get("title", "Unknown"),
        "match_score": f"{match_score:.1f}%",
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": resume_skills,
        "job_skills": job_skills
    }

    return explanation