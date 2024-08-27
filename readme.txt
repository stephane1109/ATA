# Analyse Textuelle Avancée (ATA)

## Version
Version : 0.1.0-beta
Date : 22 août 2024
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@example.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3

## Présentation
Mon objectif est de rendre les outils d'analyse textuelle accessibles et efficaces pour tous.
Vous pouvez en savoir plus sur mon travail sur mon site web [Code & Cortex](http://www.codeandcortex.fr) ou consulter mon profil [LinkedIn](https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/).


## Description
L'application **Analyse Textuelle Avancée (ATA)** est un outil de traitement automatique du langage naturel (NLP) conçu pour faciliter l'analyse de textes volumineux.
Elle intègre plusieurs algorithmes et techniques d'analyse textuelle, notamment le K-Means, la Classification Ascendante Hiérarchique (CAH), TF-IDF, LDA, ainsi que d'autres outils avancés pour la fouille de texte.

### Fonctionnalités principales
- **K-Means** : Regroupe les documents en clusters en fonction de leur similarité textuelle.
- **CAH (Classification Ascendante Hiérarchique)** : Crée des clusters de documents avec une approche hiérarchique.
- **TF-IDF** : Évalue l'importance des termes dans un corpus.
- **LDA (Latent Dirichlet Allocation)** : Identifie les sujets récurrents dans les documents.
- **Cooccurrence** : à partir d'un mot clé
- **Extraction de commentaires YouTube** : Récupère les commentaires des vidéos YouTube pour analyse.
- **Europress html to text** : Convertit les fichiers HTML issus d'Europresse en texte brut.
- **PDF to text** : Extrait le texte des fichiers PDF pour analyse.
- **Recherche de doublons Europresse** : Identifie les doublons et les articles courts dans les fichiers Europresse.
- **Voice to text** : Convertit les fichiers audio en texte (transcription vocale).
- **Scraper les commentaires YouTube** : Récupère les commentaires des vidéos YouTube pour analyse.

- **MP4 to MP3** (En construction) : Convertit les fichiers vidéo MP4 en fichiers audio MP3.
- **Scraper** : html to text** (En construction) : Récupère le contenu HTML de pages web et le convertit en texte brut.
- **AFC** : Analyse Factorielle de Correspondance (En construction)
- **Adaptation des scripts au modèle Camembert** (En construction)
- **Analyse de graph** (En construction)

## Installation des librairies

### Installation de Spacy
Spacy est l'une des librairies principales utilisées dans ce projet pour le traitement du langage naturel. Pour installer Spacy, suivez les étapes ci-dessous :

1. **Installer Spacy** :
    pip install spacy

2. **Installer le modèle de langue large** :
    Pour le français : python -m spacy download fr_core_news_lg


### Installation des autres librairies
Outre Spacy, le projet ATA nécessite d'autres librairies pour fonctionner correctement.
Vous pouvez installer toutes les librairies nécessaires en une seule commande :

pip install streamlit pandas scikit-learn sentence-transformers seaborn matplotlib wordcloud requests nltk umap-learn plotly scipy beautifulsoup4 lxml html5lib numpy streamlit-option-menu pyLDAvis
pip install yt-dlp streamlit -> mp4TOmp3

## Lancer l'Application
Dans le terminal python : streamlit run main.py

## Arreter l'application :
Si vous souhaitez arrêter l'application, retournez dans votre terminal et appuyez sur Ctrl + C.
