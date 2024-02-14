import json

# Charger le JSON depuis le fichier (ou remplacer avec vos données JSON)
with open('TP3/data/documents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data[:50])
