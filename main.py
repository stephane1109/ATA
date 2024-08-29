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

from config import *  # Importer la configuration de la page
from streamlit_option_menu import option_menu
from kmeans import afficher_interface_kmeans  # Importer seulement l'interface K-Means
from cah import analyse_cah
from cah import afficher_interface_cah
from tfidf import afficher_interface_tfidf
from europresse import afficher_interface_europresse
from pdf_traitement import traitement_pdf
from gestion_doublons import afficher_interface_recherche_doublons
from lda import afficher_interface_lda
from scraper import afficher_interface_scraper_youtube_comments
from analyse_cooccurrences import afficher_interface_cooccurrences
from youtube_transcription import afficher_interface_youtube_transcription
from mp4tomp3 import afficher_interface_mp4_to_mp3
from faq import afficher_faq
import os

# Configuration de la page est déjà gérée dans config.py

# Titre principal
st.title("ATA - Analyse Textuelle Avancée")

# Sous-titre avec la version et les liens
st.markdown("**ATA - Version 0.1.0 Beta - [Dépôt Github](https://github.com/stephane1109/ATA) - [Site web](http://www.codeandcortex.fr)**")


# Menu horizontal principal
selected = option_menu(
    None, ["Accueil", "Data", "Scraper", "K-Means", "CAH", "TF-IDF", "LDA", "Cooccu", "FAQ"],
    icons=['house', 'file-earmark-text', 'file-earmark-text', 'bar-chart', 'bar-chart', 'bar-chart', 'bar-chart', 'bar-chart', 'search'],
    menu_icon="cast", default_index=0, orientation="horizontal"  # Assurez-vous que "Accueil" est la page par défaut
)

# Accueil
if selected == "Accueil":
    st.subheader("Bienvenue dans l'application d'analyse textuelle avancée.")

    st.markdown("""
    **Version Bêta 0.1.0**

    Cette interface regroupe plusieurs scripts Python que j'ai développés individuellement au fil du temps, maintenant réunis pour vous offrir des outils  d'analyse textuelle.

    Vous y trouverez des algorithmes NLP courants comme **TF-IDF**, **K-MEANS**, **LDA** et bien d'autres. L'idée est de vous donner une plateforme pratique pour explorer, analyser et interpréter vos données textuelles.

    Actuellement, le modèle **SpaCy large** en français est utilisé pour le traitement du texte (NLP), offrant une "relative" précision et (surtout) exploitable avec n'importe quel Mac/PC. 
    
    Mais restez à l'affût, car cette version Bêta est encore en développement et pourrait s'enrichir d'autres fonctionnalités et améliorations.

    Explorez les différentes options du menu pour commencer et n'oubliez pas de me faire part de vos retours. C'est grâce à vous que cette application pourra s'améliorer !

    """)

# Ajout d'une image GIF depuis un répertoire local
    st.image("/Users/stephanemeurisse/Documents/Recherche/Kmeans-CAH-1/CAH-KMEANS-1/KMEANS.gif", use_column_width=True)  # Remplacez "path/to/your_image.gif" par le chemin relatif ou absolu de votre GIF

# Préparation des Données (renommé "Data")
elif selected == "Data":
    prep_option = option_menu(
        None, ["Europresse html to text", "PDF to text", "Recherche de doublons", "MP4 to MP3", "Voice to text"],
        icons=['file-earmark', 'file-pdf', 'search', 'mic'],
        menu_icon="file-earmark", default_index=0, orientation="horizontal"
    )

    if prep_option == "Europresse html to text":
        afficher_interface_europresse()

    elif prep_option == "PDF to text":
        traitement_pdf()


    elif prep_option == "Recherche de doublons":
        afficher_interface_recherche_doublons()


    elif prep_option == "MP4 to MP3":
        afficher_interface_mp4_to_mp3()

    elif prep_option == "Voice to text":
        afficher_interface_youtube_transcription()


# Cooccurrences
elif selected == "Cooccu":
    afficher_interface_cooccurrences()

# K-Means
elif selected == "K-Means":
    afficher_interface_kmeans()

# CAH
elif selected == "CAH":
    afficher_interface_cah()

# TF-IDF
elif selected == "TF-IDF":
    afficher_interface_tfidf()

# LDA
elif selected == "LDA":
    afficher_interface_lda()

# SCRAPER
elif selected == "Scraper":
    scraper_option = option_menu(
        None, ["Scraper les commentaires YouTube"],
        icons=['search'],
        menu_icon="search", default_index=0, orientation="horizontal"
    )

    if scraper_option == "Scraper les commentaires YouTube":
        afficher_interface_scraper_youtube_comments()


# FAQ
elif selected == "FAQ":
    afficher_faq()
