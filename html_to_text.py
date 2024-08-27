# dans la main.py
# from html_to_text import afficher_interface_html_to_text
# elif selected == "HTML to Text":
#     afficher_interface_html_to_text()

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


# Fonction pour extraire le texte d'un site web
def extraire_texte_depuis_site(url, output_directory):
    # Configurer ChromeDriver avec WebDriver Manager
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Exécuter Chrome en mode headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Lancer le navigateur
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Charger la page web
        driver.get(url)
        time.sleep(2)  # Attendre que la page soit complètement chargée

        # Extraire le texte de la page
        body = driver.find_element(By.TAG_NAME, 'body')
        texte = body.text

        # Enregistrer le texte dans un fichier
        nom_fichier = f"{output_directory}/texte_extrait.txt"
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write(texte)

        st.success(f"Texte extrait et sauvegardé dans : {nom_fichier}")

    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte : {e}")

    finally:
        driver.quit()


# Interface Streamlit
def afficher_interface_html_to_text():
    st.title("HTML to Text - Extraction de texte depuis un site web")

    st.markdown("""
    **Fonctionnement :**

    Ce script utilise Selenium et ChromeDriver pour scraper le texte d'un site web et le sauvegarder dans un fichier texte.

    ### Installation et Utilisation de ChromeDriver :

    - **Installation Automatique** : Le script utilise `webdriver_manager` pour installer automatiquement ChromeDriver.
    - **Pré-requis** : Vous devez avoir Google Chrome installé sur votre système.
    - **Options** : L'option `headless` est activée par défaut pour exécuter Chrome en arrière-plan sans ouvrir de fenêtre.

    ### Instructions :
    1. Entrez l'URL du site web dont vous souhaitez extraire le texte.
    2. Sélectionnez le répertoire où le fichier texte extrait sera sauvegardé.
    3. Cliquez sur le bouton pour lancer l'extraction.

    """)

    # Saisie de l'URL
    url = st.text_input("Entrez l'URL du site web :")

    # Sélection du répertoire de sortie
    output_directory = st.text_input("Sélectionnez le répertoire de sauvegarde",
                                     value=os.path.expanduser("~/Documents"))

    # Bouton pour lancer l'extraction
    if st.button("Extraire le texte"):
        if url and output_directory:
            extraire_texte_depuis_site(url, output_directory)
        else:
            st.error("Veuillez entrer l'URL du site web et choisir un répertoire de sauvegarde.")

# Appel de la fonction dans le menu principal de votre projet ATA
