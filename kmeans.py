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


import pandas as pd
import re
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from umap import UMAP
import plotly.express as px
import os
import numpy as np
import streamlit as st
import nltk
from nltk.corpus import stopwords

# Télécharger le corpus de stop words si nécessaire
nltk.download('stopwords')

# Utiliser les stop words français de NLTK
french_stopwords = stopwords.words('french')


# Fonction principale pour afficher l'interface K-Means
def afficher_interface_kmeans():
    st.subheader("Analyse K-Means")

    # Insérer l'explication sous le titre
    st.markdown("""
    ### Explication de l'analyse K-Means

    Le K-Means est une méthode d'apprentissage non supervisé utilisée pour regrouper des données en un certain nombre de clusters (ou groupes) prédéfini. Contrairement à d'autres méthodes, le K-Means ne nécessite pas d'étiquettes pour les données d'entrée, il cherche plutôt à regrouper les données en fonction de leurs similarités intrinsèques.

    Dans le cadre de l'analyse textuelle, le K-Means est particulièrement utile pour la fouille de texte, permettant de révéler des **insights** cachés au sein d'un grand corpus de documents. En définissant à l'avance le nombre de clusters, vous contrôlez la granularité des résultats.

    Il est important de noter que le nombre de clusters (k) doit être déterminé en amont, ce qui peut parfois être délicat. Pour vous aider, la méthode de la courbe "elbow" (ou coude) est souvent utilisée. Cette méthode consiste à exécuter plusieurs fois le K-Means avec différents nombres de clusters et à observer le point où l'ajout de clusters supplémentaires n'améliore plus significativement l'inertie (une mesure de la cohésion au sein des clusters).

    Il est conseillé de réaliser plusieurs essais avec différents nombres de clusters pour identifier la solution la plus pertinente. Ce test est particulièrement utilisé pour explorer les données textuelles et identifier des thèmes ou sujets récurrents dans un corpus, en facilitant l'extraction de **insights** utiles.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte pour K-Means", type="txt")
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file.getvalue().decode("utf-8")
        st.session_state['file_name'] = uploaded_file.name
        st.success(f"Fichier {st.session_state['file_name']} chargé avec succès.")

        save_directory = st.text_input("Définir le répertoire de sauvegarde",
                                       value=os.path.expanduser("~/Documents/ATA/KMEANS"))
        n_clusters = st.slider("Choisissez le nombre de clusters", 2, 20, 5)
        min_df = st.slider("Minimum document frequency (min_df)", 0.0, 1.0, 0.1)
        max_df = st.slider("Maximum document frequency (max_df)", 0.0, 1.0, 0.9)

        if st.button("Lancer l'Analyse K-Means"):
            analyse_kmeans(st.session_state['uploaded_file'], save_directory, n_clusters, min_df, max_df)


# Fonction pour extraire le contenu des articles
def parse_article(article_text):
    lines = article_text.strip().split('\n')
    # Filtrer les lignes qui commencent par ****
    lines = [line for line in lines if not line.startswith('****')]
    content = ' '.join(lines) if len(lines) > 1 else ''
    return {'content': content}


# Fonction pour prétraiter le texte
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text


# Fonction pour créer le concordancier
def create_concordance(df, clusters):
    concordance_df = pd.DataFrame({
        'Document': df['content'],
        'Cluster': [f'Cluster {c + 1}' for c in clusters]
    })
    grouped_concordance = concordance_df.groupby('Cluster')['Document'].apply(lambda x: ' '.join(x)).reset_index()
    return grouped_concordance


# Fonction pour télécharger un DataFrame en CSV
def save_csv(dataframe, filename, directory):
    path = os.path.join(directory, f"{filename}.csv")
    dataframe.to_csv(path, index=False, encoding='utf-8')


# Fonction pour afficher et télécharger la matrice de similarité cosinus entre les clusters
def display_similarity_matrix(embeddings, cluster_labels, directory):
    cluster_centers = [embeddings[cluster_labels == i].mean(axis=0) for i in range(max(cluster_labels) + 1)]
    similarity_matrix = cosine_similarity(cluster_centers)

    cluster_names = [f'Cluster {i + 1}' for i in range(len(cluster_centers))]
    similarity_df = pd.DataFrame(similarity_matrix, columns=cluster_names, index=cluster_names)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(similarity_df, cmap='coolwarm', ax=ax, annot=True, fmt=".2f", xticklabels=cluster_names,
                yticklabels=cluster_names)
    plt.title("Carte Thermique de Similarité entre les Clusters")
    plt.savefig(os.path.join(directory, "kmeans_similarity_heatmap.png"))
    st.pyplot(fig)
    plt.close(fig)

    save_csv(similarity_df, "kmeans_cluster_similarity_matrix", directory)


# Fonction pour afficher les nuages de mots pour chaque cluster
def display_wordclouds(df, cluster_labels, directory):
    for cluster in set(cluster_labels):
        cluster_data = df['content'][cluster_labels == cluster]
        wordcloud_text = ' '.join(cluster_data)
        wordcloud = WordCloud(width=800, height=400, background_color='white',
                              stopwords=set(french_stopwords)).generate(wordcloud_text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Topic {cluster + 1}')
        plt.savefig(os.path.join(directory, f"kmeans_wordcloud_topic_{cluster + 1}.png"))
        st.pyplot(plt)
        plt.close()


# Fonction pour afficher la visualisation des clusters en 2D
def display_cluster_visualization(embeddings, labels, directory):
    umap_model = UMAP(n_components=2, random_state=42)
    reduced_embeddings = umap_model.fit_transform(embeddings)

    viz_df = pd.DataFrame({
        'x': reduced_embeddings[:, 0],
        'y': reduced_embeddings[:, 1],
        'Cluster': labels
    })

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=viz_df, x='x', y='y', hue='Cluster', palette='viridis', s=50, alpha=0.7, ax=ax)
    plt.title("Visualisation des Clusters K-Means")
    plt.savefig(os.path.join(directory, "kmeans_cluster_2D.png"))
    st.pyplot(fig)
    plt.close(fig)


# Fonction pour visualiser les centroides des clusters
def display_centroid_visualization(embeddings, cluster_labels, directory):
    cluster_centers = np.array([embeddings[cluster_labels == i].mean(axis=0) for i in range(max(cluster_labels) + 1)])
    umap_model = UMAP(n_components=2, random_state=42)
    reduced_centroids = umap_model.fit_transform(cluster_centers)

    df_centroids = pd.DataFrame({
        'x': reduced_centroids[:, 0],
        'y': reduced_centroids[:, 1],
        'Cluster': range(1, len(cluster_centers) + 1),
        'Size': [10] * len(cluster_centers)
    })

    fig = px.scatter(
        df_centroids, x='x', y='y', size='Size', color='Cluster',
        title='Visualisation des Centroides des Clusters',
        labels={'x': 'Dimension 1', 'y': 'Dimension 2', 'Cluster': 'Clusters'},
        hover_data={'Size': False}
    )
    fig.write_image(os.path.join(directory, "kmeans_centroid_visualization.png"))
    st.plotly_chart(fig)


# Fonction pour visualiser les clusters regroupés en bulles
def display_grouped_bubble_chart(embeddings, cluster_labels, directory):
    umap_model = UMAP(n_components=2, random_state=42)
    reduced_embeddings = umap_model.fit_transform(embeddings)
    df = pd.DataFrame({
        'x': reduced_embeddings[:, 0],
        'y': reduced_embeddings[:, 1],
        'Cluster': cluster_labels
    })

    cluster_sizes = df['Cluster'].value_counts().sort_index()
    df['Size'] = df['Cluster'].map(cluster_sizes)

    fig = px.scatter(
        df, x='x', y='y', size='Size', color='Cluster',
        hover_data=['Cluster'], opacity=0.6, size_max=50,
        title='Visualisation des Clusters Regroupés en Forme de Bulles'
    )
    fig.write_image(os.path.join(directory, "kmeans_grouped_bubble_chart.png"))
    st.plotly_chart(fig)


# Fonction pour calculer la courbe du coude
def plot_elbow_curve(embeddings, save_directory):
    # Créer le répertoire s'il n'existe pas
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    inertia = []
    K = range(2, 21)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(embeddings)
        inertia.append(kmeans.inertia_)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(K, inertia, 'bx-')
    ax.set_xlabel('Nombre de Clusters (k)')
    ax.set_ylabel('Inertie')
    ax.set_title('Méthode du Coude Pour Déterminer le Nombre Optimal de Clusters')
    st.pyplot(fig)

    # Enregistrer la figure dans le répertoire de sauvegarde
    plt.savefig(os.path.join(save_directory, "elbow_method.png"))
    plt.close(fig)
    st.success(f"Graphique de la méthode du coude enregistré : {os.path.join(save_directory, 'elbow_method.png')}")


# Fonction principale pour l'analyse KMeans
def analyse_kmeans(file_content, save_directory, n_clusters, min_df, max_df):
    articles = file_content.strip().split('****')
    articles_data = [parse_article(article) for article in articles if article.strip()]

    df = pd.DataFrame(articles_data)
    df['content'] = df['content'].apply(preprocess_text)

    # Vectorisation des documents avec les paramètres min_df et max_df
    vectorizer = CountVectorizer(stop_words=french_stopwords, min_df=min_df, max_df=max_df)
    X = vectorizer.fit_transform(df['content'])

    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(df['content'].tolist(), show_progress_bar=True)

    # Afficher la courbe du coude
    plot_elbow_curve(embeddings, save_directory)

    # Appliquer KMeans avec les paramètres fournis
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_labels = kmeans.fit_predict(embeddings)
    df['Cluster'] = kmeans_labels

    display_centroid_visualization(embeddings, kmeans_labels, save_directory)
    display_grouped_bubble_chart(embeddings, kmeans_labels, save_directory)
    display_cluster_visualization(embeddings, kmeans_labels, save_directory)
    display_similarity_matrix(embeddings, kmeans_labels, save_directory)
    display_wordclouds(df, kmeans_labels, save_directory)

    concordance_kmeans = create_concordance(df, kmeans_labels)
    save_csv(concordance_kmeans, "kmeans_concordance", save_directory)

    df.to_csv(os.path.join(save_directory, "kmeans_final_result.csv"), index=False)

    st.write("### Concordancier KMeans")
    st.dataframe(concordance_kmeans)

    st.write("### Résultats finaux de l'analyse KMeans")
    st.dataframe(df)
