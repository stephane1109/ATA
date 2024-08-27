##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@example.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 22 août 2024
# Version : 0.1.0-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################

import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords

# Télécharger le corpus de stop words si nécessaire
nltk.download('stopwords')

# Utiliser les stop words français de NLTK
french_stopwords = stopwords.words('french')

# Fonction principale pour afficher l'interface CAH
def afficher_interface_cah():
    # Insérer le titre de l'application
    st.title("Analyse CAH")

    # Insérer l'explication sous le titre
    st.markdown("""
    ### Explication de l'analyse CAH

    La Classification Ascendante Hiérarchique (CAH) est une méthode d'apprentissage non supervisé qui regroupe les données en clusters hiérarchiques. Contrairement à la méthode K-Means, où vous devez spécifier le nombre de clusters à l'avance, la CAH crée une hiérarchie complète de clusters imbriqués, représentée sous la forme d'un dendrogramme.

    Le dendrogramme vous permet de visualiser la manière dont les clusters se forment et de choisir le niveau de regroupement qui vous semble le plus pertinent. La méthode de liaison utilisée ici est celle de Ward, qui minimise la variance intracluster.

    **Format des données** : Ce script fonctionne avec un corpus de texte où chaque article commence par une ligne contenant "****" suivie d'une ligne avec les variables étoilées. Cela permet de traiter directement des corpus déjà formatés pour IRaMuTeQ, sans nécessiter de retouches supplémentaires.

    **Modèle utilisé** : Le test est paramétré avec le modèle `all-MiniLM-L6-v2`. Ce modèle, bien que moins précis que BERT (ou CamemBERT pour le français), est très rapide et flexible. De plus, il est multilingue, ce qui le rend particulièrement adapté à des corpus comprenant plusieurs langues.

    Ce type d'analyse est particulièrement utile dans l'exploration de données textuelles pour identifier des groupes thématiques ou des tendances récurrentes, en fournissant une perspective hiérarchique sur la structure des données.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte pour l'analyse CAH", type="txt")
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file.getvalue().decode("utf-8")
        st.session_state['file_name'] = uploaded_file.name
        st.success(f"Fichier {st.session_state['file_name']} chargé avec succès.")

        save_directory = st.text_input("Définir le répertoire de sauvegarde",
                                       value=os.path.expanduser("~/Documents/ATA/CAH"))

        if st.button("Lancer l'Analyse CAH"):
            analyse_cah(st.session_state['uploaded_file'], save_directory)


# Fonction pour extraire le contenu des articles
def parse_article(article_text):
    lines = article_text.strip().split('\n')
    content = '\n'.join(lines[1:]) if len(lines) > 1 else ''
    return {'content': content}

# Fonction pour prétraiter le texte
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

# Fonction pour créer le dendrogramme et effectuer la CAH
def create_dendrogram_and_cah(embeddings, save_directory, threshold=1.0):
    # Appliquer la CAH
    Z = linkage(embeddings, method='ward')

    # Tracer le dendrogramme
    fig, ax = plt.subplots(figsize=(10, 7))
    dendrogram(Z, ax=ax)
    plt.title('Dendrogramme de la Classification Ascendante Hiérarchique')
    plt.xlabel('Index des observations')
    plt.ylabel('Distance')
    plt.savefig(os.path.join(save_directory, "cah_dendrogram.png"))
    st.pyplot(fig)
    plt.close(fig)

    # Créer les clusters à partir du dendrogramme
    clusters = fcluster(Z, t=threshold, criterion='distance')
    return clusters

# Fonction pour sauvegarder les résultats
def save_results(df, clusters, save_directory):
    df['Cluster'] = clusters
    save_csv(df, "cah_final_result", save_directory)

    concordance_cah = create_concordance(df, clusters)
    save_csv(concordance_cah, "cah_concordance", save_directory)

    st.write("### Concordancier CAH")
    st.dataframe(concordance_cah)

    st.write("### Résultats finaux de l'analyse CAH")
    st.dataframe(df)

# Fonction pour créer un concordancier
def create_concordance(df, clusters):
    concordance_df = pd.DataFrame({
        'Document': df['content'],
        'Cluster': [f'Cluster {c + 1}' for c in clusters]
    })
    grouped_concordance = concordance_df.groupby('Cluster')['Document'].apply(lambda x: ' '.join(x)).reset_index()
    return grouped_concordance

# Fonction pour télécharger un DataFrame en CSV
def save_csv(dataframe, filename, directory):
    """Enregistre un DataFrame en CSV dans un répertoire donné."""
    path = os.path.join(directory, f"{filename}.csv")
    dataframe.to_csv(path, index=False, encoding='utf-8')

# Fonction principale pour l'analyse CAH
def analyse_cah(file_content, save_directory):
    # Séparation des articles par la ligne ****
    articles = file_content.strip().split('****')
    articles_data = [parse_article(article) for article in articles if article.strip()]

    # Convertir en DataFrame
    df = pd.DataFrame(articles_data)
    df['content'] = df['content'].apply(preprocess_text)

    # Initialiser SentenceTransformer pour créer des embeddings
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(df['content'].tolist(), show_progress_bar=True)

    # Créer le dendrogramme et effectuer la CAH
    clusters = create_dendrogram_and_cah(embeddings, save_directory)

    # Sauvegarder les résultats
    save_results(df, clusters, save_directory)

