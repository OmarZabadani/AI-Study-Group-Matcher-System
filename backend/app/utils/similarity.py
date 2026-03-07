from sklearn.metrics.pairwise import cosine_similarity

def cosine_sim(vec, vec_list):
    return cosine_similarity([vec], vec_list)[0]