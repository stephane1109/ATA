##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 22 août 2024
# Version : 0.1.1-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################

import streamlit as st
import hashlib

# Longueur minimale par défaut des articles
LONGUEUR_MINIMALE_PAR_DEFAUT = 300

# Fonction pour détecter les doublons et les articles trop courts dans un fichier texte
def detecter_doublons(file_content, longueur_minimale):
    articles_uniques = {}
    articles_doublons = []
    articles_courts = []
    contenu_article = []
    entete_article = ''
    debut_article = False

    lines = file_content.splitlines()

    for ligne in lines:
        if ligne.startswith('**** '):  # Ligne de début d'article
            if debut_article:  # Si on est déjà dans un article
                corps_article = ''.join(contenu_article)
                texte_article = entete_article + corps_article
                hash_article = hashlib.sha256(corps_article.encode('utf-8')).hexdigest()
                # Vérification des doublons
                if hash_article in articles_uniques:
                    if len(corps_article) > len(articles_uniques[hash_article][1]):
                        articles_doublons.append((articles_uniques[hash_article][0], articles_uniques[hash_article][1]))
                        articles_uniques[hash_article] = (entete_article, corps_article)
                    else:
                        articles_doublons.append((entete_article, corps_article))
                else:
                    articles_uniques[hash_article] = (entete_article, corps_article)
                # Vérification de la longueur minimale
                if len(corps_article) < longueur_minimale:
                    articles_courts.append((entete_article, corps_article))
                contenu_article = []
                entete_article = ligne
            else:
                debut_article = True
                entete_article = ligne
        else:
            contenu_article.append(ligne)

    # Traitement du dernier article
    if contenu_article:
        corps_article = ''.join(contenu_article)
        texte_article = entete_article + corps_article
        hash_article = hashlib.sha256(corps_article.encode('utf-8')).hexdigest()
        if hash_article in articles_uniques:
            if len(corps_article) > len(articles_uniques[hash_article][1]):
                articles_doublons.append((articles_uniques[hash_article][0], articles_uniques[hash_article][1]))
                articles_uniques[hash_article] = (entete_article, corps_article)
            else:
                articles_doublons.append((entete_article, corps_article))
        else:
            articles_uniques[hash_article] = (entete_article, corps_article)
        if len(corps_article) < longueur_minimale:
            articles_courts.append((entete_article, corps_article))

    return articles_uniques, articles_doublons, articles_courts

# Fonction pour extraire un texte à partir d'un article
def extraire_texte(texte_article, longueur=50):
    lignes = texte_article.split('\n')
    if len(lignes) > 1:
        return lignes[1][:longueur] + '...' if len(lignes[1]) > longueur else lignes[1]
    return texte_article[:longueur] + '...' if len(texte_article) > longueur else texte_article

# Interface Streamlit pour la recherche de doublons
def afficher_interface_recherche_doublons():
    st.title("Gestion des doublons et articles courts")

    # Explication du fonctionnement
    st.markdown("""
    **Fonctionnement :**

    Ce script vous permet de détecter les doublons dans un fichier texte d'articles provenant d'Europresse, formaté avec une première ligne commençant par `****`.

    Il recherche également les articles trop courts en comparant leur longueur avec un seuil défini. 
    Vous pouvez ajuster ce seuil en déterminant le nombre de caractères minimum pour qu'un article soit considéré comme valide. 
    Cela peut par exemple être utile pour supprimer des exports Europresse qui incluent des éditos ou des articles très courts qui ne sont pas pertinents pour votre analyse.
    """)

    uploaded_file = st.file_uploader("Téléchargez un fichier texte", type="txt")

    longueur_minimale = st.number_input("Longueur minimale des articles :", min_value=0,
                                        value=LONGUEUR_MINIMALE_PAR_DEFAUT)

    if uploaded_file:
        file_content = uploaded_file.getvalue().decode("utf-8")

        if st.button("Analyser les doublons et les articles courts"):
            articles_uniques, articles_doublons, articles_courts = detecter_doublons(file_content, longueur_minimale)

            st.write(f"### Nombre d'articles en double : {len(articles_doublons)}")
            st.write(f"### Nombre d'articles trop courts : {len(articles_courts)}")

            if articles_doublons:
                st.subheader("Articles en double")
                for entete, corps in articles_doublons:
                    texte_article = entete + corps
                    st.text_area("Article en double", value=extraire_texte(texte_article, 200), height=100)

            if articles_courts:
                st.subheader("Articles trop courts")
                for entete, corps in articles_courts:
                    texte_article = entete + corps
                    st.text_area("Article trop court", value=extraire_texte(texte_article, 200), height=100)
