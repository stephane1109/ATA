##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 29 août 2024
# Version : 0.3.1-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################

import whisper
import streamlit as st
import os
import subprocess

def convertir_audio_en_wav(audio_path, wav_path):
    """Convertir un fichier audio (m4a, mp3, etc.) en WAV en utilisant ffmpeg."""
    command = f"ffmpeg -i {audio_path} -ar 16000 -ac 1 -c:a pcm_s16le {wav_path}"
    subprocess.run(command, shell=True, check=True)

def convertir_audio_en_texte_whisper(audio_path, output_directory):
    # Créer le chemin pour le fichier WAV
    wav_path = os.path.join(output_directory, "temp_audio.wav")

    # Convertir l'audio en WAV
    convertir_audio_en_wav(audio_path, wav_path)

    # Charger le modèle Whisper
    model = whisper.load_model("base")

    # Transcription
    result = model.transcribe(wav_path)
    texte = result["text"]

    # Sauvegarder la transcription
    transcription_path = os.path.join(output_directory, "transcription_whisper.txt")
    with open(transcription_path, 'w', encoding='utf-8') as file:
        file.write(texte.strip())

    st.success(f"Le fichier texte a été créé : {transcription_path}")

    # Supprimer le fichier WAV temporaire
    os.remove(wav_path)

def afficher_interface_audio_to_text_whisper():
    st.title("Audio to Text avec Whisper (OpenAI)")

    st.markdown("""
    **Fonctionnement :**
    Ce script permet de convertir un fichier audio (MP3 ou M4A) en texte en utilisant le modèle Whisper d'OpenAI.
    Whisper est un modèle de reconnaissance vocale qui offre une haute précision et fonctionne localement sur votre machine.

    ### Instructions :
    1. Téléchargez un fichier audio MP3 ou M4A.
    2. Sélectionnez un répertoire de sortie.
    3. Cliquez sur "Convertir l'audio en Texte" pour démarrer la transcription.
    """)

    uploaded_audio = st.file_uploader("Sélectionnez le fichier audio (MP3 ou M4A)", type=["mp3", "m4a"])

    user_home_directory = os.path.expanduser("~")
    default_output_directory = os.path.join(user_home_directory, "Documents", "ATA", "Audio_to_Text_Whisper")
    output_directory = st.text_input("Sélectionnez le répertoire de sauvegarde", value=default_output_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if st.button("Convertir l'audio en Texte"):
        if uploaded_audio and output_directory:
            temp_audio_path = os.path.join(output_directory, uploaded_audio.name)
            with open(temp_audio_path, "wb") as temp_audio:
                temp_audio.write(uploaded_audio.getbuffer())

            convertir_audio_en_texte_whisper(temp_audio_path, output_directory)

if __name__ == "__main__":
    afficher_interface_audio_to_text_whisper()
