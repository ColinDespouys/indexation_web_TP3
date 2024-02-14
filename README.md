# Fonctionnement du Programme de Recherche de Documents

Elève : DESPOUYS Colin

Ce programme permet de rechercher des documents dans une collection en utilisant une approche de recherche textuelle. Il prend en entrée une requête de recherche et renvoie les documents pertinents en fonction de cette requête.

## Installation et Utilisation

**Exécution du Programme** : Lancez le programme en exécutant `python main.py`. Assurez-vous que les fichiers de données nécessaires sont présents dans le dossier `data`.

## Explication du Code

### 1. Chargement des Données JSON

Les données JSON, comprenant l'index inversé des termes, les documents et l'index des positions des termes dans les titres, sont chargées depuis les fichiers correspondants.

### 2. Tokenisation de la Requête

La requête de recherche est tokenisée en utilisant une méthode similaire à celle utilisée pour créer l'index inversé.

### 3. Filtrage des Documents

La fonction `filter_documents()` filtre les documents en fonction des tokens de la requête. L'utilisateur peut choisir entre un filtrage de type "ET" (où seuls les documents contenant tous les tokens de la requête sont sélectionnés) ou un filtrage de type "OU" (où les documents contenant au moins un des tokens de la requête sont sélectionnés).

### 4. Classement des Documents

La fonction `rank_documents()` classe les documents filtrés en fonction de leur pertinence par rapport à la requête. Dans l'exemple fourni, nous utilisons une méthode de pondération TF-IDF (Term Frequency-Inverse Document Frequency) pour calculer les scores des documents en fonction des tokens de la requête. Cela permet de donner un poids plus important aux tokens significatifs par rapport aux "stop words".

### 5. Génération du Résultat JSON

Les documents pertinents sont ensuite formatés dans un fichier JSON contenant des informations sur le nombre total de documents, le nombre de documents filtrés et les détails des documents pertinents.

## Fonctionnement du Classement des Documents

Nous avons utilisé une approche de pondération TF-IDF pour classer les documents. TF-IDF est une méthode couramment utilisée pour évaluer l'importance d'un terme dans un document relativement à une collection de documents. Cela permet de mettre en avant les termes les plus discriminants et de réduire l'importance des termes fréquents mais peu discriminants (comme les "stop words"). Ainsi, les documents contenant des termes rares mais significatifs seront mieux classés que ceux contenant des termes fréquents mais peu informatifs.
