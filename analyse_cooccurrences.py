##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 22 août 2024
# Version : 0.1.0-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import os

# Charger les ressources NLTK
nltk.download('punkt')
nltk.download('punkt_tab') # ????? pas certain
nltk.download('stopwords')

# Variables globales
french_stopwords = set(nltk_stopwords.words('french'))
french_stopwords.update(["encore", "plus", "cela", "entre", "si", "très", "comme"])  # Stopwords supplémentaires


# Fonction pour prétraiter le texte
def preprocess_text(doc):
    tokens = word_tokenize(doc, language='french')
    filtered_tokens = [token.lower() for token in tokens if
                       token.lower().isalnum() and token.lower() not in french_stopwords]
    return filtered_tokens


# Fonction pour lire et prétraiter le fichier
def read_and_preprocess_file(file_content):
    articles = []
    current_article = []
    for line in file_content.splitlines():
        if line.startswith('****'):
            if current_article:
                articles.append(' '.join(current_article).strip())
                current_article = []
        else:
            current_article.append(line)
    if current_article:
        articles.append(' '.join(current_article).strip())
    return articles


# Fonction pour calculer les cooccurrences
def calculate_cooccurrences(articles, keyword, window_size=10):
    cooccurrence_counter = Counter()
    for article in articles:
        tokens = preprocess_text(article)
        keyword_indices = [i for i, token in enumerate(tokens) if token == keyword]
        for index in keyword_indices:
            window_start = max(0, index - window_size)
            window_end = min(len(tokens), index + window_size + 1)
            context_tokens = tokens[window_start:index] + tokens[index + 1:window_end]
            for token in context_tokens:
                if token != keyword:
                    cooccurrence_counter[token] += 1
    return cooccurrence_counter


# Fonction pour générer un fichier CSV des cooccurrences
def generate_csv(cooccurrences, output_directory, keyword):
    df = pd.DataFrame(cooccurrences.items(), columns=['Cooccurrence', 'Frequency'])
    csv_path = os.path.join(output_directory, f"cooccurrences_{keyword}.csv")
    df.to_csv(csv_path, index=False)
    return csv_path


# Fonction pour générer un nuage de mots
def generate_wordcloud(cooccurrences, output_directory, keyword, top_n):
    top_cooccurrences = dict(cooccurrences.most_common(top_n))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_cooccurrences)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Top {top_n} Cooccurrences for '{keyword}'")
    plt_path = os.path.join(output_directory, f"wordcloud_{keyword}.png")
    plt.savefig(plt_path, bbox_inches='tight')
    st.pyplot(plt)
    return plt_path


# Fonction pour afficher l'interface utilisateur
def afficher_interface_cooccurrences():
    st.title("Analyse de Cooccurrences à partir d'un mot-clé")

    # Explications sur le fonctionnement du script
    st.markdown("""
    - Ce script permet d'analyser les cooccurrences d'un mot-clé spécifique dans un fichier texte.
    - Assurez-vous que le fichier texte est correctement formaté avec chaque article commençant par '****'.
    - Vous pouvez entrer des mots à exclure supplémentaires dans le champ dédié.
    - Sélectionnez le nombre de cooccurrences à afficher et lancez l'analyse.
    - Le script génère un fichier CSV des cooccurrences et un nuage de mots.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte", type="txt")

    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")

        keyword = st.text_input("Entrez le mot-clé pour l'analyse:")
        stopwords_str = st.text_area("Entrez des mots à exclure supplémentaires (séparés par une virgule):", value="")
        if stopwords_str:
            custom_stopwords = [word.strip().lower() for word in stopwords_str.split(',')]
            french_stopwords.update(custom_stopwords)

        top_n_cooccurrences = st.number_input("Nombre de co-occurrences à afficher:", min_value=1, max_value=100,
                                              value=10)

        if keyword:
            output_directory = st.text_input("Définir le répertoire de sauvegarde",
                                             value=os.path.expanduser("~/Documents/ATA/Cooccurrences"))
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            if st.button("Lancer l'Analyse"):
                articles = read_and_preprocess_file(file_content)
                cooccurrences = calculate_cooccurrences(articles, keyword)

                if cooccurrences:
                    st.success("Analyse terminée avec succès.")
                    csv_path = generate_csv(cooccurrences, output_directory, keyword)
                    st.write(f"Les co-occurrences ont été sauvegardées dans {csv_path}")

                    wordcloud_path = generate_wordcloud(cooccurrences, output_directory, keyword, top_n_cooccurrences)
                    st.write(f"Nuage de mots sauvegardé dans {wordcloud_path}")
                else:
                    st.error("Aucune co-occurrence trouvée pour ce mot-clé.")


# Lancer l'application Streamlit
if __name__ == "__main__":
    afficher_interface_cooccurrences()
