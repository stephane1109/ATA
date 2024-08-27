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

import os
import re
import html
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import streamlit as st

# Définir la locale pour interpréter les dates en français
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


# Fonction pour nettoyer le nom du journal
def nettoyer_nom_journal(nom_journal):
    nom_journal_sans_numero = nom_journal.split(",")[0]
    nom_journal_sans_numero = re.sub(r"[ ']", "_", nom_journal_sans_numero)
    nom_journal_nettoye = f"*source_{nom_journal_sans_numero}"
    return nom_journal_nettoye


# Fonction pour extraire le texte du fichier HTML
def extraire_texte_html(contenu_html, chemin_txt, chemin_csv, variable_suppl_texte, nom_journal_checked,
                        date_annee_mois_jour_checked, date_annee_mois_checked, date_annee_checked, methode_extraction):
    soup = BeautifulSoup(contenu_html, 'html.parser')
    articles = soup.find_all('article')
    texte_final = ""
    data_for_csv = []

    for article in articles:
        # Suppression des balises non nécessaires
        for element in article.find_all(["head", "aside", "footer", "img", "a"]):
            element.decompose()
        for element in article.find_all("div", class_=["apd-wrapper"]):
            element.decompose()
        for element in article.find_all("p", class_="sm-margin-bottomNews"):
            element.decompose()

        nom_journal_formate = ""  # Valeur par défaut
        texte_article = article.get_text(" ", strip=True)

        # Choix de la méthode d'extraction du nom du journal
        if methode_extraction == 0:
            div_journal = article.find("div", class_="rdp__DocPublicationName")
            if div_journal:
                span_journal = div_journal.find("span", class_="DocPublicationName")
                if span_journal:
                    nom_journal = span_journal.get_text(strip=True)
                    nom_journal_formate = nettoyer_nom_journal(nom_journal)
        elif methode_extraction == 1:
            div_journal = article.find("div", class_="rdp__DocPublicationName")
            if div_journal:
                span_journal = div_journal.find("span", class_="DocPublicationName")
                if span_journal:
                    content_list = list(span_journal.stripped_strings)
                    if content_list:
                        nom_journal = content_list[0]
                    else:
                        nom_journal = ""
                    nom_journal_formate = nettoyer_nom_journal(nom_journal)

        # Suppression du nom du journal du texte de l'article si nécessaire
        texte_article = texte_article.replace(nom_journal_formate, '').strip()

        if div_journal:
            div_journal.decompose()

        # Extraire la date
        span_date = article.find("span", class_="DocHeader")
        date_texte = html.unescape(span_date.get_text()) if span_date else ""
        date_formattee = am_formattee = annee_formattee = ""
        if span_date:
            match = re.search(r'\d{1,2} \w+ \d{4}', date_texte)
            if match:
                date_str = match.group()
                try:
                    date_obj = datetime.strptime(date_str, '%d %B %Y')
                    date_formattee = date_obj.strftime('*date_%Y-%m-%d')
                    am_formattee = date_obj.strftime('*am_%Y-%m')
                    annee_formattee = date_obj.strftime('*annee_%Y')
                except ValueError:
                    pass
            span_date.decompose()

        # Nettoyer les expressions de liens
        texte_article = re.sub(r'\(lien : https?://[^)]+\)', '', texte_article)

        # Traiter spécifiquement la balise <p class="sm-margin-TopNews titreArticleVisu rdp__articletitle">
        if article.find("p", class_="sm-margin-TopNews titreArticleVisu rdp__articletitle"):
            titre_article = article.find("p", class_="sm-margin-TopNews titreArticleVisu rdp__articletitle").get_text(
                strip=True)
            texte_article = texte_article.replace(titre_article, titre_article + "\n", 1)

        # Nettoyer les informations après la première ligne étoilée
        if date_formattee:
            texte_article = texte_article.replace(date_texte, "").strip()

        # Traitement des lignes pour ajouter un point à la première ligne et supprimer l'espace en début de chaque ligne
        lignes = texte_article.splitlines()
        if lignes and not lignes[0].endswith('.'):  # Vérifier si la première ligne n'a pas déjà un point
            lignes[0] += '.'  # Ajouter un point à la fin de la première ligne
        lignes = [ligne.strip() for ligne in lignes]  # Supprimer les espaces en début de chaque ligne
        texte_article = '\n'.join(lignes)  # Rejoindre les lignes en une seule chaîne de texte

        # Construire info_debut basé sur les cases à cocher
        info_debut = "****"
        if nom_journal_checked:
            info_debut += f" {nom_journal_formate}"
        if date_annee_mois_jour_checked:
            info_debut += f" {date_formattee}"
        if date_annee_mois_checked:
            info_debut += f" {am_formattee}"
        if date_annee_checked:
            info_debut += f" {annee_formattee}"
        if variable_suppl_texte:
            info_debut += f" *{variable_suppl_texte}"
        info_debut += "\n"

        # Ajouter le texte traité de chaque article à texte_final
        texte_final += info_debut + texte_article + "\n\n"

        # Préparer les données pour l'export CSV
        data_for_csv.append({
            'Journal': nom_journal_formate,
            'Date': date_formattee,
            'Article': texte_article
        })

    # Écrire le texte final dans le fichier de sortie .txt
    with open(chemin_txt, 'w', encoding='utf-8') as fichier_txt:
        fichier_txt.write(texte_final)

    # Écrire les données dans un fichier .csv
    with open(chemin_csv, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=['Journal', 'Date', 'Article'])
        writer.writeheader()
        for row in data_for_csv:
            writer.writerow(row)

    st.success(f"Le fichier a été traité et enregistré en tant que : {chemin_txt} et {chemin_csv}")


# Interface Streamlit
def afficher_interface_europresse():
    st.title("Traitement des fichiers Europresse")

    # Explication des méthodes
    st.markdown("""
    Ce script Python vise à convertir les fichiers au format html provenant du site Europresse au format texte (.txt) pour le logiciel IRAMUTEQ.
    Le script effectue un nettoyage du corpus et formate la première ligne de chaque article selon les exigences du logiciel.

    Le script affiche en première ligne de tous les articles les variables étoilées suivantes :
    **** *source_nomdujournal *date_2023-12-22 *am_2023-12 *annee_2023

    Vous pouvez activer les variables ci-dessous et ajouter une variable (champ texte).

    ### Explication des méthodes d'extraction :
    - **Méthode 0** : Extraction simple du nom du journal depuis un `div` avec la classe `rdp__DocPublicationName`.
    - **Méthode 1** : Extraction du nom du journal avec un traitement supplémentaire pour gérer les cas où le contenu est une liste de chaînes.
    """)

    # Drag and drop pour uploader le fichier HTML
    uploaded_file = st.file_uploader("Télécharger un fichier HTML Europresse", type="html")
    if uploaded_file:
        chemin_txt = st.text_input("Définir le nom du fichier texte de sortie", value="europresse_output.txt")
        chemin_csv = st.text_input("Définir le nom du fichier CSV de sortie", value="europresse_output.csv")
        save_directory = st.text_input("Définir le répertoire de sortie",
                                       value=os.path.expanduser("~/Documents/ATA/Europresse"))

        variable_suppl_texte = st.text_input(
            "Votre variable supplémentaire (Laisser le champ vide si pas nécessaire) :")
        nom_journal_checked = st.checkbox("Inclure le nom du journal")
        date_annee_mois_jour_checked = st.checkbox("Inclure la date (année-mois-jour)")
        date_annee_mois_checked = st.checkbox("Inclure la date (année-mois)")
        date_annee_checked = st.checkbox("Inclure l'année uniquement")

        methode_extraction = st.radio("Sélectionnez la méthode d'extraction du nom du journal", [
            "Méthode classique (On touche à rien et on exporte!)",
            "Méthode 2 : (conseillée) Texte avant la balise <br> - permet de raccourcir le nom du journal"
        ])

        if st.button("Lancer la préparation Europresse"):
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            chemin_txt = os.path.join(save_directory, chemin_txt)
            chemin_csv = os.path.join(save_directory, chemin_csv)
            contenu_html = uploaded_file.getvalue().decode("utf-8")
            extraire_texte_html(contenu_html, chemin_txt, chemin_csv, variable_suppl_texte, nom_journal_checked,
                                date_annee_mois_jour_checked, date_annee_mois_checked, date_annee_checked,
                                0 if methode_extraction == "Méthode classique (On touche à rien et on exporte!)" else 1)
