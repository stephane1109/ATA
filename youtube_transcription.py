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
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp as youtube_dl
import os

# Définir la langue par défaut
DEFAULT_LANG = "fr"  # Par exemple, "fr" pour le français

def download_and_transcribe(video_id, directory, format):
    try:
        # Téléchargement des sous-titres de la vidéo YouTube avec la langue par défaut
        st.info("Téléchargement des sous-titres en cours...")
        transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=[DEFAULT_LANG])
        if transcripts:
            # Joindre le texte sans sauts de ligne
            transcript_text = " ".join([part['text'].replace('\n', ' ') for part in transcripts])
            transcript_file_path = os.path.join(directory, "transcript.txt")
            with open(transcript_file_path, 'w', encoding='utf-8') as file:
                file.write(transcript_text)
            st.success("Les sous-titres ont été téléchargés avec succès.")

            # Téléchargement de l'audio depuis YouTube avec yt-dlp
            st.info("Téléchargement de l'audio en cours...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(directory, f'audio.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format,
                    'preferredquality': '192',
                }]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

            final_audio_path = os.path.join(directory, f'audio.{format}')
            st.success(f"L'audio a été téléchargé avec succès en format {format.upper()}.")
            st.info(f"Audio sauvegardé à : {final_audio_path}")

        else:
            st.warning("Aucun sous-titre disponible pour cette vidéo.")

    except Exception as e:
        # Afficher l'erreur uniquement si aucun fichier n'a été généré
        if not os.path.exists(os.path.join(directory, "transcript.txt")):
            st.error(f"Une erreur s'est produite : {e}")
        else:
            st.warning("Une erreur s'est produite, mais le fichier a bien été généré.")


def afficher_interface_youtube_transcription():
    st.title("Speech to Text avec YoutubeTranscript")

    st.markdown("""
    **Comment fonctionne le script :**

    - Il faut uniquement entrer l'ID de la vidéo YouTube, et non l'URL entière.
    - Par exemple, pour l'URL `https://www.youtube.com/watch?v=qBo37puJEQg`, l'ID de la vidéo est `qBo37puJEQg`.
    - Assurez-vous de bien sélectionner l'ID, sinon le script ne fonctionnera pas correctement.
    """)

    # Saisie de l'ID de la vidéo YouTube
    video_id = st.text_input("Entrez l'ID de la vidéo YouTube :")

    # Choix du format audio (MP3 ou WAV)
    format = st.radio("Choisissez le format audio :", options=["mp3", "wav"], index=0)

    # Sélection du répertoire de sauvegarde
    directory = st.text_input("Définir le répertoire de sauvegarde",
                              value=os.path.expanduser("~/Documents/ATA/Youtube TRANSCRIPT"))

    # Bouton pour démarrer le téléchargement et la transcription
    if st.button("Télécharger et Transcrire"):
        if video_id and directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
            download_and_transcribe(video_id, directory, format)
        else:
            st.error("Veuillez entrer l'ID de la vidéo YouTube et choisir un répertoire de sauvegarde.")

