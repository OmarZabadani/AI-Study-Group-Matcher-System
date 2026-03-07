from sentence_transformers import SentenceTransformer

def load_model():
    # Load model once
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(model, text_list):
    return model.encode(text_list, convert_to_tensor=False)