from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_embedding(sentence):
    embed = model.encode(sentence)
    return embed

def get_similarity(query, sentence):
    query_embedding = get_embedding(query)
    sentence_embedding = get_embedding(sentence)
    return cosine_similarity(query_embedding, sentence_embedding)

def get_top_k_similar(query, sentences, k=5):
    similarities = []
    for sentence in sentences:
        similarity = get_similarity(query, sentence)
        similarities.append(similarity)
    similarities = np.array(similarities)
    top_k_indices = np.argsort(similarities, axis=0)[-k:]
    return top_k_indices

if __name__ == "__main__":
	pass