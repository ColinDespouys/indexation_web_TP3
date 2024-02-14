import json
import re
from collections import defaultdict, Counter
import nltk

# 1. Lire le fichier JSON
# Charger les données JSON avec l'encodage correct
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Ajout de 'encoding="utf-8"'
        return json.load(file)

index = load_json('data/content_pos_index.json')
documents = load_json('data/documents.json')
title_pos = load_json('data/title_pos_index.json')
    
# Tokeniser la requête
def tokenize_query(query):
    # Ici, utilisez la même méthode de tokenisation que celle utilisée pour créer l'index
    return query.lower().split()

# Filtrer les documents qui contiennent tous les tokens de la requête
def filter_documents(query_tokens, index, filter_type='ET'):  # Ajout du paramètre filter_type avec la valeur par défaut 'ET'
    relevant_docs = set()
    for token in query_tokens:
        if token in index:
            if filter_type == 'ET':  # Filtrage de type ET
                if not relevant_docs:
                    relevant_docs = set(index[token].keys())
                else:
                    relevant_docs.intersection_update(index[token].keys())
            elif filter_type == 'OU':  # Filtrage de type OU
                relevant_docs.update(index[token].keys())
    return relevant_docs

# Fonction de ranking linéaire
from math import log

# Fonction de ranking avec TF-IDF
def rank_documents(relevant_docs, index, query_tokens, documents):
    k1 = 1.5
    b = 0.75
    avg_doc_length = sum(len(doc['title']) for doc in documents) / len(documents)
    num_documents = len(documents)
    doc_lengths = {doc['id']: len(doc['title']) for doc in documents}
    idf_scores = defaultdict(float)

    # Calculer IDF pour chaque token dans la requête
    for token in query_tokens:
        if token in index:
            idf_scores[token] = log((num_documents - len(index[token]) + 0.5) / (len(index[token]) + 0.5) + 1)

    # Calculer le score pour chaque document
    ranked_docs = []
    for doc_id in relevant_docs:
        score = 0
        for token in query_tokens:
            if token in index and doc_id in index[token]:
                token_info = index[token][doc_id]
                # Calcul de BM25 pour le token dans le document
                tf = token_info['count']
                doc_length = doc_lengths[doc_id]
                idf = idf_scores[token]
                score += idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avg_doc_length))))
        ranked_docs.append((doc_id, score))

    return sorted(ranked_docs, key=lambda x: x[1], reverse=True)

# Renvoyer les résultats au format JSON
def create_results_json(query, documents, index, filter_type):
    query_tokens = tokenize_query(query)
    relevant_docs_ids = filter_documents(query_tokens, index, filter_type)
    ranked_docs = rank_documents(relevant_docs_ids, index, query_tokens, documents)
    
    results = {'total_documents': len(documents), 'filtered_documents': len(relevant_docs_ids), 'documents': []}
    for doc_id, _ in ranked_docs:
        doc_info = next((doc for doc in documents if doc['id'] == int(doc_id)), None)
        if doc_info:
            results['documents'].append({'title': doc_info['title'], 'url': doc_info['url']})
    
    with open('result/results.json', 'w', encoding='utf-8') as file:  # Spécifier l'encodage UTF-8
        json.dump(results, file, indent=4, ensure_ascii=False)  # Assurez-vous que les caractères non-ASCII ne soient pas échappés


# Exemple d'utilisation
query = "dvd erreur"
filter_type = 'OU'
create_results_json(query, documents, index, filter_type)