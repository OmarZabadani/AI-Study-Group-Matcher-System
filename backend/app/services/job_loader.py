import pandas as pd
from utils.text_cleaner import clean_text

def load_job_file(file):
    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    job_objects = []
    for idx, row in df.iterrows():
        title = str(row.get("job_title","")).strip()
        desc = str(row.get("job_description","")).strip()
        if title and desc:
            job_objects.append({
                "id": f"job_{idx}",
                "title": title,
                "raw_text": desc,
                "clean_text": clean_text(desc)
            })
    return job_objects