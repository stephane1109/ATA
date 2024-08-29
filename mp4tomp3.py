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


import yt_dlp as youtube_dl
import os
import re
import streamlit as st


# Fonction pour mettre à jour la barre de progression
def update_progress(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        percent_value = re.search(r"([0-9]+(?:\.[0-9]+)?)%", percent)
        if percent_value:
            # Limiter la valeur de progression entre 0 et 100
            progress = min(float(percent_value.group(1)), 100)
            st.session_state.progress_bar.progress(progress / 100.0)  # Convertir en fraction pour Streamlit


# Fonction pour télécharger l'audio à partir de YouTube
def download_audio(url, directory, format):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(directory, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: update_progress(d)],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        st.success(f"L'audio a été téléchargé avec succès dans {directory}")
    except Exception as e:
        st.error(f"Le téléchargement a échoué : {e}")


# Fonction principale pour l'interface Streamlit MP4 to MP3
def afficher_interface_mp4_to_mp3():
    st.title("Téléchargeur d'audio YouTube")

    # Explication du fonctionnement de l'outil
    st.markdown("""
    ### Fonctionnement :

    Cet outil vous permet de récupérer la piste audio (mp3 ou wav) d'une vidéo YouTube pour ensuite réaliser une retranscription automatique (speech to text avec Google par exemple). 

    - **Format d'URL (copier/coller dans la barre de votre navigateur) - Exemple :** : `https://www.youtube.com/watch?v=qBo37puJEQg`
    - **Formats supportés** : Vous pouvez choisir entre MP3 et WAV (WAV est le format optimal pour Google Speech To Text).

    Après l'extraction, vous pouvez utiliser d'autres outils pour convertir l'audio en texte.
    """)

    # Entrée de l'URL
    url = st.text_input("Entrez l'URL de la vidéo YouTube :")

    # Sélection du format de l'audio
    format = st.radio("Sélectionnez le format de l'audio :", ('mp3', 'wav'))

    # Sélection du répertoire de sauvegarde
    save_directory = st.text_input("Définir le répertoire de sauvegarde", value=os.path.expanduser("~/Documents/ATA/MP4TOMP3"))

    # Bouton pour lancer le téléchargement
    if st.button("Télécharger l'audio"):
        if not url:
            st.error("Veuillez entrer une URL valide.")
        elif not save_directory:
            st.error("Veuillez sélectionner un répertoire de sauvegarde.")
        else:
            st.session_state.progress_bar = st.progress(0)  # Initialisation de la barre de progression
            download_audio(url, save_directory, format)
            st.session_state.progress_bar.empty()  # Vider la barre de progression après le téléchargement
