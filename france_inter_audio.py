##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 29 août 2024
# Version : 0.2.1-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################


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

    Il faut trouver l'URL directe du fichier audio, vous pourrez ainsi la coller dans l'interface ATA.

    ### Comment trouver le lien de l'audio :

    1. Accédez à la page de l'émission sur France Inter.
    2. Faites défiler vers le bas de la page jusqu'à voir le lecteur audio.
    3. **Clique droit** sur le titre de la piste audio.
    4. Sélectionnez **"Inspecter l'élément"** dans le menu contextuel.
    5. Dans l'inspecteur qui s'ouvre, repérez la balise :
       
       ```html
       <audio hidden="" preload="none" crossorigin="anonymous" src="https://media.radiofrance-podcast.net/podcast09/10076-29.08.2024-ITEMA_23842676-2024C36128S0242-21.mp3"></audio>
       ```
    6. **Clique droit** sur le lien mp3 ou mp4 dans la balise `src` et choisissez **"Ouvrir dans un nouvel onglet"**.
    7. Copiez l'URL de l'audio depuis la barre d'adresse du nouvel onglet et collez-la dans l'interface ATA ci-dessous.
    """)

    # Saisie de l'URL directe de l'audio
    url = st.text_input("Entrez l'URL du fichier audio :")

    # Sélection du répertoire de sortie
    output_directory = st.text_input("Sélectionnez le répertoire de sauvegarde",
                                     value=os.path.expanduser("~/Documents"))

    # Bouton pour lancer le téléchargement
    if st.button("Télécharger l'audio"):
        if url and output_directory:
            telecharger_audio(url, output_directory)
        else:
            st.error("Veuillez entrer l'URL et choisir un répertoire de sauvegarde.")

