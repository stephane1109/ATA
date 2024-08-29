import streamlit as st
import requests
import os


def telecharger_audio(url, output_directory):
    try:
        # Téléchargement du fichier audio
        st.info("Téléchargement de l'audio en cours...")
        audio_data = requests.get(url).content
        audio_filename = os.path.join(output_directory, os.path.basename(url))

        with open(audio_filename, "wb") as audio_file:
            audio_file.write(audio_data)

        st.success(f"Fichier audio téléchargé avec succès : {audio_filename}")
    except Exception as e:
        st.error(f"Erreur lors du téléchargement de l'audio : {e}")


# Interface Streamlit
def afficher_interface_france_inter_audio():
    st.title("Téléchargement Audio France Inter")

    st.markdown("""
    **Fonctionnement :**

    Si vous avez l'URL directe d'un fichier audio (par exemple un podcast ou une émission de France Inter), vous pouvez la coller ici pour télécharger l'audio directement sur votre machine.
    """)

    # Saisie de l'URL directe de l'audio
    url = st.text_input("Entrez l'URL du fichier audio :")

    # Sélection du répertoire de sortie
    output_directory = st.text_input("Sélectionnez le répertoire de sauvegarde",
                                     value=os.path.expanduser("~/Documents/ATA"))

    # Bouton pour lancer le téléchargement
    if st.button("Télécharger l'audio"):
        if url and output_directory:
            telecharger_audio(url, output_directory)
        else:
            st.error("Veuillez entrer l'URL et choisir un répertoire de sauvegarde.")