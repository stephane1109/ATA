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


import streamlit as st
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Chargement du modèle français de SpaCy
nlp = spacy.load('fr_core_news_lg')
nlp.max_length = 8000000  # Augmenter la limite de caractères


# Fonction pour lemmatiser le texte et retirer les stopwords
def lemmatize_and_remove_stopwords(text, nlp, stopwords):
    doc = nlp(text)
    lemmatized_text = " ".join(
        [token.lemma_ for token in doc if token.text.lower() not in stopwords and not token.is_punct]
    )
    return lemmatized_text


# Interface principale pour Streamlit
def afficher_interface_tfidf():
    st.title("Analyse TF-IDF des Documents Textuels")

    # Explication du fonctionnement
    st.markdown("""
    **Fonctionnement :**
    Le TF-IDF (Term Frequency-Inverse Document Frequency) est une méthode couramment utilisée en traitement automatique du langage naturel pour évaluer l'importance d'un mot dans un document par rapport à un corpus de documents.
    
    Contrairement aux simples méthodes de distribution en fréquence, telles que les nuages de mots, qui mettent en avant les mots les plus fréquents, le TF-IDF redonne du poids aux mots rares, les considérant souvent comme plus révélateurs de la spécificité d'un document.

    **Format requis pour le test TF-IDF**
    Ce test fonctionne avec un corpus où chaque article commence par **#** suivi d'un texte. Chaque article doit être séparé par une nouvelle ligne commençant également par # suivi du texte.
    
    Cela permet au script de distinguer correctement les différents articles dans le corpus.
    Il est important de noter que pour le moment, ce test ne fonctionne pas avec un encodage de type IRAMUTEQ où chaque article commence par ****. 
    
    Par conséquent, veuillez vous assurer que votre corpus est formaté correctement pour que le test puisse être exécuté sans problème.
    """)

    # Téléchargement du fichier texte
    uploaded_file = st.file_uploader("Téléchargez un fichier texte pour TF-IDF", type="txt")

    if uploaded_file is not None:
        # Extension des stopwords
        spacy_stopwords = set(nlp.Defaults.stop_words)
        custom_stopwords = st.text_area("Entrez des stopwords personnalisés (séparés par une virgule):", value="")
        if custom_stopwords:
            spacy_stopwords.update(custom_stopwords.split(','))

        # Bouton pour lancer l'analyse
        if st.button("Lancer l'Analyse TF-IDF"):
            # Chargement et préparation du fichier texte
            content = uploaded_file.getvalue().decode("utf-8")
            content = re.sub(r'\n+', '\n', content).strip()
            messages = content.split('\n#')
            st.write(f"Nombre initial de messages divisés : {len(messages)}")

            # Lemmatisation et suppression des stopwords
            corpus_lemmatized_and_cleaned = [
                lemmatize_and_remove_stopwords(msg, nlp, spacy_stopwords) for msg in messages if msg.strip()
            ]
            st.write(f"Nombre de documents après traitement : {len(corpus_lemmatized_and_cleaned)}")

            # Exportation au format CSV du corpus lemmatisé/stopword
            df_corpus_cleaned = pd.DataFrame(corpus_lemmatized_and_cleaned, columns=['Document Text'])
            save_directory = st.text_input("Définir le répertoire de sauvegarde",
                                           value=os.path.expanduser("~/Documents/ATA/TFIDF"))
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            csv_output_path = os.path.join(save_directory, "corpus_lemmatised_and_cleaned.csv")
            df_corpus_cleaned.to_csv(csv_output_path, index_label='Document Number')
            st.success(f"Le corpus lemmatisé et nettoyé a été exporté dans le fichier: {csv_output_path}")

            # Lecture du fichier CSV contenant le corpus lemmatisé et nettoyé
            corpus_from_csv = df_corpus_cleaned['Document Text'].tolist()

            # Choix du calcul des scores TF-IDF
            normalisation = st.selectbox("Choisissez la méthode de normalisation pour TF-IDF:", ["Aucune", "L2"])
            norm = 'l2' if normalisation == "L2" else None
            tfidf_vectorizer = TfidfVectorizer(norm=norm, use_idf=True)
            tfidf_matrix_from_csv = tfidf_vectorizer.fit_transform(corpus_from_csv)
            feature_names_from_csv = tfidf_vectorizer.get_feature_names_out()

            # Création d'un DataFrame pour les scores TF-IDF
            tfidf_df_from_csv = pd.DataFrame(tfidf_matrix_from_csv.toarray(), columns=feature_names_from_csv)
            tfidf_df_from_csv['Document Number'] = range(1, len(tfidf_df_from_csv) + 1)
            tfidf_df_from_csv['Top TF-IDF Term'] = tfidf_df_from_csv[feature_names_from_csv].idxmax(axis=1)

            # Exportation des scores TF-IDF dans un fichier CSV
            csv_path_scores = os.path.join(save_directory, "resultats_doc_final.csv")
            tfidf_df_from_csv.to_csv(csv_path_scores, index=False)
            st.success(f"Les scores TF-IDF pour chaque document ont été sauvegardés dans {csv_path_scores}")

            # Choisir le nombre de termes à exporter
            top_n = st.slider("Choisissez le nombre de termes à exporter:", min_value=5, max_value=100, value=20)
            top_scores = tfidf_df_from_csv[feature_names_from_csv].max().nlargest(top_n)

            # Exportation du top N des scores TF-IDF dans un fichier CSV
            top_n_terms = pd.DataFrame({'Term': top_scores.index, 'TF-IDF Score': top_scores.values})
            csv_path_top_n = os.path.join(save_directory, f"top_{top_n}_terms_final.csv")
            top_n_terms.to_csv(csv_path_top_n, index=False)
            st.success(
                f"Les {top_n} termes les plus importants basés sur les scores TF-IDF ont été sauvegardés dans {csv_path_top_n}")

            # Génération et affichage de nuages de mots
            def generate_wordcloud(words, title, file_path):
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(words)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title(title)
                plt.savefig(file_path)
                st.pyplot(plt)

            # Nuage de mots pour tous les termes
            generate_wordcloud(dict(zip(feature_names_from_csv, np.mean(tfidf_matrix_from_csv.toarray(), axis=0))),
                               "Global TF-IDF", os.path.join(save_directory, "global_tfidf_final.png"))

            # Nuage de mots pour le top N des termes
            generate_wordcloud(top_n_terms.set_index('Term')['TF-IDF Score'].to_dict(),
                               f"Top {top_n} TF-IDF Terms", os.path.join(save_directory, f"top{top_n}_tfidf_final.png"))

            # Loi de Zipf à partir des résultats TF-IDF
            tfidf_sum = np.array(tfidf_matrix_from_csv.sum(axis=0)).flatten()
            sorted_tfidf_sum = np.sort(tfidf_sum)[::-1]  # Trier les scores TF-IDF en ordre décroissant
            ranks = np.arange(1, len(sorted_tfidf_sum) + 1)  # Créer un tableau de rangs
            plt.figure(figsize=(10, 6))
            plt.loglog(ranks, sorted_tfidf_sum, marker="o")
            plt.title("Loi de Zipf - Fréquence des termes vs Rang")
            plt.xlabel("Rang du terme")
            plt.ylabel("Fréquence (Somme des scores TF-IDF)")
            st.pyplot(plt)


