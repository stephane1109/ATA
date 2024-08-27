# pip install streamlit
# pip install streamlit-option-menu

import streamlit as st

def afficher_faq():
    st.markdown("""
    En traitement du langage naturel (NLP), clustering et classification sont deux techniques d'analyse de données utilisées pour organiser et catégoriser des données textuelles, mais elles diffèrent par leur objectif, leur méthode et leur application.

### 1. Clustering

Le clustering est une **technique d'apprentissage non supervisé** qui vise à regrouper des données similaires en groupes appelés clusters. 

Dans le cadre du NLP, le clustering est souvent utilisé pour regrouper des documents, des phrases ou des mots ayant des similitudes sémantiques ou textuelles.

    K-Means et CAH (Classification Ascendante Hiérarchique) sont des méthodes de clustering.

    K-Means :
        Le K-Means divise les données en un nombre prédéfini de clusters (k).
        L'algorithme cherche à minimiser la distance intra-cluster (la distance entre les points de données et le centre du cluster).
        Le nombre de clusters doit être fixé à l'avance. Une fois les clusters formés, les documents appartenant à un même cluster sont supposés être similaires entre eux.

    CAH :
        La CAH crée une hiérarchie de clusters. Elle ne nécessite pas de spécifier le nombre de clusters à l'avance.
        L'algorithme construit un arbre ou dendrogramme, qui peut être coupé à un certain niveau pour déterminer les clusters finaux.
        Cette méthode est plus flexible que K-Means car elle permet de visualiser les relations entre les différents clusters à différents niveaux de granularité.

En résumé le clustering, utilisé par K-Means et CAH, est une méthode exploratoire qui regroupe des données sans étiquettes prédéfinies, permettant de découvrir des structures cachées dans les données textuelles. 

### 2. Classification

La classification est une technique d'apprentissage supervisé qui consiste à assigner des étiquettes ou catégories prédéfinies à de nouvelles données en se basant sur un modèle formé à partir de données étiquetées.

    Exemple en NLP :
        Classer des emails en "spam" ou "non-spam".
        Attribuer des sentiments "positifs", "négatifs" ou "neutres" à des critiques de produits.

Contrairement au clustering, la classification nécessite un jeu de données d'entraînement où chaque donnée est déjà associée à une étiquette (ou catégorie). 
Le modèle apprend les caractéristiques des données dans chaque catégorie et utilise ces connaissances pour classer de nouvelles données.

Différences Clés

    Type d'Apprentissage :
        Clustering : Non supervisé (pas besoin d'étiquettes)
        Classification : Supervisé (nécessite des étiquettes)

    Objectif :
        Clustering : Découvrir des groupes naturels ou structures cachées dans les données.
        Classification : Prédire la catégorie ou l'étiquette d'une nouvelle donnée.
    
    
### 3. Préparation des Données

    Avant d'appliquer l'algorithme K-Means++ ou CAH, il est crucial de préparer correctement vos données. 
    Le script a été conçu pour fonctionner avec des articles provenant de la plateforme **Europresse**, et est compatible avec le logiciel **Iramuteq**. 
    Pour garantir un traitement adéquat, chaque article doit être précédé d'une ligne de démarcation commençant par ****. 
    Cette structure est essentielle pour que le script puisse identifier et traiter chaque article distinctement.

    - **Format d'entrée :**
      - **Fichiers Texte :** Les fichiers doivent être en format texte, avec des articles séparés par ****.

### 2. Algorithmes K-Means++ et CAH

    #### K-Means++ :

    - **Initialisation Améliorée :**
      - Contrairement à l'initialisation aléatoire de K-Means, K-Means++ choisit les centroïdes initiaux de manière stratégique. 
      Le premier centroïde est sélectionné aléatoirement, et les suivants sont choisis en fonction de leur distance par rapport aux centroïdes déjà sélectionnés, favorisant une répartition plus uniforme.

    - **Assignation des Points :**
      - Chaque point de données est assigné au cluster avec le centroïde le plus proche, calculé avec la distance euclidienne.

    - **Mise à jour des Centroïdes :**
      - Pour chaque cluster, le centroïde est recalculé comme la moyenne de tous les points assignés à ce cluster.

    - **Convergence :**
      - L'algorithme répète les étapes d'assignation et de mise à jour jusqu'à ce que les centroïdes se stabilisent ou qu'un nombre maximal d'itérations soit atteint.

    #### CAH :

    - **Construction de la Hiérarchie :**
      - La CAH commence par considérer chaque point comme un cluster individuel. 
      Les clusters les plus similaires sont ensuite fusionnés de manière itérative jusqu'à ce qu'il ne reste qu'un seul cluster contenant tous les points.

    - **Dendrogramme :**
      - La hiérarchie est représentée sous forme de dendrogramme, qui montre les niveaux auxquels les clusters ont été fusionnés. 
      L'utilisateur peut choisir un seuil pour couper le dendrogramme, déterminant ainsi le nombre final de clusters.

    - **Assignation des Points :**
      - En fonction du seuil choisi, les points sont assignés à des clusters, similaires à ceux de K-Means.

    #### Visualisation des Résultats :

    - **Centroides et Clusters :**
      - Le script génère plusieurs graphiques pour visualiser les clusters et leurs centroïdes :
        - **Graphique des Centroides :** Visualisation des positions moyennes des clusters après convergence (pour K-Means).
        - **Carte Thermique de Similarité :** Visualisation des similarités entre les clusters, basée sur la distance entre les centroïdes.
        - **Nuages de Mots :** Mots-clés caractéristiques de chaque cluster, permettant de comprendre le contenu textuel de chaque groupe.
        - **Dendrogramme :** Pour CAH, le dendrogramme visualise la hiérarchie des clusters.


### 3. Paramètres des Algorithmes :

    """)

if __name__ == "__main__":
    afficher_faq()
