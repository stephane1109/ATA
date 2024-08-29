# Analyse Textuelle Avancée (ATA)

## Version
Version : 0.1.0-beta
Date : 22 août 2024
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
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
- **MP4 to MP3** : Convertit les fichiers vidéo MP4 en fichiers audio MP3.

- **Scraper site web** : html to text** (En construction) : Récupère le contenu HTML de pages web et le convertit en texte brut.
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

pip install streamlit youtube-transcript-api yt-dlp spacy scikit-learn numpy pandas matplotlib wordcloud google-api-python-client PyMuPDF gensim pyLDAvis sentence-transformers seaborn umap-learn plotly beautifulsoup4 nltk

### Détails des bibliothèques utilisées

    streamlit : Utilisé pour créer l'interface utilisateur de l'application.
    youtube-transcript-api : Permet d'extraire les transcriptions des vidéos YouTube.
    yt-dlp : Utilisé pour télécharger des vidéos YouTube.
    os : Bibliothèque standard Python pour les opérations sur le système de fichiers.
    re : Utilisé pour les expressions régulières.
    spacy : Utilisé pour le traitement du langage naturel.
    scikit-learn : Fournit des outils pour l'extraction de caractéristiques, la classification, le clustering, etc.
    numpy : Bibliothèque pour les opérations mathématiques et la manipulation de tableaux.
    pandas : Utilisé pour la manipulation de données sous forme de DataFrame.
    matplotlib : Utilisé pour la création de graphiques.
    wordcloud : Utilisé pour générer des nuages de mots à partir de texte.
    google-api-python-client : Utilisé pour interagir avec les API de Google, comme l'API YouTube.
    datetime : Bibliothèque standard pour manipuler les dates et les heures.
    fitz (PyMuPDF) : Utilisé pour extraire du texte à partir de fichiers PDF.
    gensim : Fournit des outils pour la modélisation de sujets (LDA) et la construction de phrases.
    pyLDAvis : Utilisé pour visualiser les résultats de l'analyse LDA.
    sentence-transformers : Utilisé pour l'embedding de phrases et le calcul de similarités cosinus.
    umap-learn : Utilisé pour la réduction de dimensionnalité.
    plotly : Utilisé pour la création de graphiques interactifs.
    beautifulsoup4 : Utilisé pour le parsing de documents HTML.
    nltk : Utilisé pour diverses tâches de traitement du langage naturel comme le tokenization et la gestion des stopwords.
    scipy : Utilisé pour des calculs scientifiques, notamment pour le clustering hiérarchique.
    hashlib : Utilisé pour générer des hachages, par exemple pour identifier des doublons.

### Installation détaillée

pip install streamlit
pip install youtube-transcript-api
pip install yt-dlp
pip install spacy
python -m spacy download fr_core_news_lg
pip install scikit-learn
pip install numpy
pip install pandas
pip install matplotlib
pip install wordcloud
pip install google-api-python-client
pip install PyMuPDF
pip install gensim
pip install pyLDAvis
pip install sentence-transformers
pip install umap-learn
pip install plotly
pip install beautifulsoup4
pip install nltk
pip install scipy


### Installation de ffmpeg
L'installation FFmpeg est requis par yt-dlp pour le téléchargement et la manipulation des vidéos.
L'installation peut être delicate surtout sous Mac.
Installation sous macOS
Ouvrez le terminal.
Installez FFmpeg via Homebrew (si Homebrew n'est pas installé, suivez les instructions sur https://brew.sh/) :
bash : brew install ffmpeg

### Lancer l'Application
Dans le terminal python : streamlit run main.py

### Arreter l'application :
Si vous souhaitez arrêter l'application, retournez dans votre terminal et appuyez sur Ctrl + C.
