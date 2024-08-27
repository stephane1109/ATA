import streamlit as st
import spacy
import pandas as pd
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.phrases import Phrases, Phraser
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import os
from streamlit.components.v1 import html

# Chargement du modèle SpaCy pour le français
nlp = spacy.load('fr_core_news_lg')


# Fonction pour le prétraitement des textes avec options de filtrage
def preprocess_text(text, remove_stopwords=True, pos_filter=None, custom_stopwords=None):
    doc = nlp(text)
    tokens = [
        token.lemma_.lower() for token in doc
        if token.is_alpha
           and (not token.is_stop if remove_stopwords else True)
           and (token.pos_ not in pos_filter if pos_filter else True)
           and (token.text.lower() not in custom_stopwords if custom_stopwords else True)
    ]
    return tokens


# Fonction principale pour l'interface Streamlit LDA
def afficher_interface_lda():
    st.title("Analyse LDA (Latent Dirichlet Allocation)")

    # Explication du fonctionnement du test LDA
    st.markdown("""
    ### Explication de l'analyse LDA

    **Latent Dirichlet Allocation (LDA)** est une méthode d'apprentissage non supervisé utilisée pour identifier des thèmes ou sujets cachés dans un grand corpus de textes. 

    Contrairement au K-Means, qui assigne chaque document à un seul cluster, LDA est un modèle probabiliste qui associe chaque document à plusieurs sujets, chacun avec un certain poids.

    LDA suppose que chaque document est une combinaison de plusieurs sujets, et chaque sujet est une distribution sur les mots du vocabulaire.

    ### Paramètres du modèle LDA

    - **Nombre de sujets (k)** : Ce paramètre, défini avant l'exécution de LDA, influence la granularité des résultats.
    Le choix de ce paramètre peut affecter les résultats et doit être déterminé en fonction de l'analyse souhaitée.

    ### Remarque :

    LDA fonctionne mieux lorsque les documents sont relativement longs et contiennent une certaine diversité de contenu pour permettre la différenciation des sujets.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte pour LDA", type="txt")

    if uploaded_file is not None:
        save_directory = st.text_input("Définir le répertoire de sauvegarde",
                                       value=os.path.expanduser("~/Documents/ATA/LDA"))
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Sélection des types de mots à exclure (NOUN, ADJ, VERB, PROPN, etc.)
        pos_filter = st.multiselect(
            "Exclure certains types de mots (POS tags)",
            options=["NOUN", "ADJ", "VERB", "PROPN", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NUM", "PART", "PRON",
                     "SCONJ", "SYM", "PUNCT"],
            default=["PUNCT"]
        )

        # Champ libre pour ajouter des stopwords personnalisés
        custom_stopwords_input = st.text_area(
            "Ajouter des stopwords personnalisés (un mot par ligne)",
            value=""
        )
        custom_stopwords = set(custom_stopwords_input.split())

        # Bouton pour lancer le test LDA
        if st.button("Lancer l'analyse LDA"):
            # Lecture des données et prétraitement
            articles = []
            file_content = uploaded_file.getvalue().decode("utf-8").splitlines()
            article_content = []
            progress_bar = st.progress(0)

            for line in file_content:
                if line.startswith('****'):
                    if article_content:
                        preprocessed_text = ' '.join(preprocess_text(" ".join(article_content), pos_filter=pos_filter,
                                                                     custom_stopwords=custom_stopwords))
                        articles.append(preprocessed_text)
                        article_content = []
                else:
                    article_content.append(line.strip())
            if article_content:
                preprocessed_text = ' '.join(preprocess_text(" ".join(article_content), pos_filter=pos_filter,
                                                             custom_stopwords=custom_stopwords))
                articles.append(preprocessed_text)

            st.write(f"Nombre d'articles traités : {len(articles)}")

            # Mise à jour de la barre de progression
            progress_bar.progress(20)

            # Transformation des articles en listes de mots pour la détection des bigrammes
            texts = [article.split() for article in articles]
            phrases = Phrases(texts, min_count=5, threshold=10)
            bigram = Phraser(phrases)
            texts_with_bigrams = [bigram[text] for text in texts]

            # Mise à jour de la barre de progression
            progress_bar.progress(40)

            # Création du dictionnaire et du corpus pour LDA, utilisant les textes avec bigrammes
            dictionary = corpora.Dictionary(texts_with_bigrams)

            # Filtrage des termes rares ou trop fréquents
            no_below = st.slider("Exclure les termes rares (minimum occurrences)", 0, 5, 0)
            no_above = st.slider("Exclure les termes fréquents (fraction maximum)", 0.1, 1.0, 0.6)
            dictionary.filter_extremes(no_below=no_below, no_above=no_above)

            corpus = [dictionary.doc2bow(text) for text in texts_with_bigrams]

            # Mise à jour de la barre de progression
            progress_bar.progress(60)

            # Paramètres LDA
            num_topics = st.slider("Nombre de topics à extraire:", 2, 20, 12)

            # Application de LDA
            lda = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

            # Mise à jour de la barre de progression
            progress_bar.progress(80)

            # Préparation des données pour la visualisation LDA
            lda_display = gensimvis.prepare(lda, corpus, dictionary, sort_topics=False)

            # Sauvegarde des résultats
            visualization_path = os.path.join(save_directory, "lda_visualization.html")
            pyLDAvis.save_html(lda_display, visualization_path)
            st.success(f"Visualisation LDA sauvegardée dans {visualization_path}")

            # Mise à jour de la barre de progression
            progress_bar.progress(100)

            # Affichage de la visualisation LDA directement dans Streamlit
            st.markdown("### Visualisation LDA")
            with open(visualization_path, 'r') as file:
                lda_html = file.read()
            html(lda_html, height=800)

            # Exportation des résultats en CSV
            topics_data = [{'Topic': topic_id + 1, 'Word': word, 'Probability': round(prob, 4)}
                           for topic_id, topic_words in
                           lda.show_topics(formatted=False, num_topics=num_topics, num_words=10)
                           for word, prob in topic_words]
            df_topics = pd.DataFrame(topics_data)
            csv_path = os.path.join(save_directory, "lda_topics.csv")
            df_topics.to_csv(csv_path, index=False)
            st.success(f"Les topics ont été sauvegardés dans {csv_path}")

            # Nuages de mots
            st.write("Nuages de mots pour chaque topic:")
            for topic_num, topic_words in lda.show_topics(formatted=False, num_topics=num_topics, num_words=20):
                plt.figure(figsize=(10, 7))
                plt.title(f"Topic #{topic_num + 1}")
                dict_words = dict(topic_words)
                wordcloud = WordCloud(width=800, height=560, background_color='white').generate_from_frequencies(
                    dict_words)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt)
                wordcloud.to_file(os.path.join(save_directory, f"topic_{topic_num + 1}_wordcloud.png"))


