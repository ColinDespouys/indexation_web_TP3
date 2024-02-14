import json
import re
from collections import defaultdict, Counter
import nltk

# 1. Lire le fichier JSON
# Charger les données JSON avec l'encodage correct
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Ajout de 'encoding="utf-8"'
        return json.load(file)

index = load_json('TP3/data/content_pos_index.json')
documents = load_json('TP3/data/documents.json')
title_pos = load_json('TP3/data/title_pos_index.json')

# print(index['provisions'])

# for i in range(5):
#     print(documents[i])

#print(title_pos['provisions'])
    
# Tokeniser la requête
def tokenize_query(query):
    # Ici, utilisez la même méthode de tokenisation que celle utilisée pour créer l'index
    return query.lower().split()

# Filtrer les documents qui contiennent tous les tokens de la requête
def filter_documents(query_tokens, index):
    relevant_docs = set()
    for token in query_tokens:
        if token in index:
            if not relevant_docs:
                relevant_docs = set(index[token].keys())
            else:
                relevant_docs.intersection_update(index[token].keys())
    return relevant_docs

# Fonction de ranking linéaire
def rank_documents(relevant_docs, index, query_tokens):
    ranked_docs = []
    for doc_id in relevant_docs:
        score = 0
        for token in query_tokens:
            if token in index and doc_id in index[token]:
                token_info = index[token][doc_id]
                score += token_info['count']  # Modifier selon les critères de ranking souhaités
        ranked_docs.append((doc_id, score))
    return sorted(ranked_docs, key=lambda x: x[1], reverse=True)  # Classement par score décroissant

# Renvoyer les résultats au format JSON
def create_results_json(query, documents, index):
    query_tokens = tokenize_query(query)
    relevant_docs_ids = filter_documents(query_tokens, index)
    ranked_docs = rank_documents(relevant_docs_ids, index, query_tokens)
    
    results = {'total_documents': len(documents), 'filtered_documents': len(relevant_docs_ids), 'documents': []}
    for doc_id, _ in ranked_docs:
        doc_info = next((doc for doc in documents if doc['id'] == int(doc_id)), None)
        if doc_info:
            results['documents'].append({'title': doc_info['title'], 'url': doc_info['url']})
    
    with open('results.json', 'w', encoding='utf-8') as file:  # Spécifier l'encodage UTF-8
        json.dump(results, file, indent=4, ensure_ascii=False)  # Assurez-vous que les caractères non-ASCII ne soient pas échappés


# Exemple d'utilisation
query = "dvd"
create_results_json(query, documents, index)