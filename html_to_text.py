##########################################
# Projet : Analyse Textuelle Avancée (ATA)
# Auteur : Stéphane Meurisse
# Contact : stephane.meurisse@gmail.com
# Site Web : https://www.codeandcortex.fr
# LinkedIn : https://www.linkedin.com/in/st%C3%A9phane-meurisse-27339055/
# Date : 22 août 2024
# Version : 0.2.1-beta
# Licence : Ce programme est un logiciel libre : vous pouvez le redistribuer selon les termes de la Licence Publique Générale GNU v3
##########################################

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup

# Fonction pour extraire le texte d'un site web avec défilement automatique
def extraire_texte_depuis_site(url, output_directory, supprimer_balises_html):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Défilement de la page pour charger le contenu dynamique
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Attendre que la page se charge
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extraire le texte de la page
        body = driver.find_element(By.TAG_NAME, 'body')
        texte = body.get_attribute('innerHTML') if not supprimer_balises_html else body.text

        if supprimer_balises_html:
            # Si l'utilisateur a choisi de supprimer les balises HTML, on utilise BeautifulSoup pour le faire
            soup = BeautifulSoup(texte, 'html.parser')
            texte = soup.get_text()

        # Sauvegarder le texte extrait dans un fichier
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        nom_fichier = os.path.join(output_directory, "texte_extrait.txt")
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

    Ce script utilise Selenium et ChromeDriver pour scraper le texte d'un site web et le sauvegarder dans un fichier texte. Un défilement automatique est inclus pour permettre de charger dynamiquement le contenu de la page.

    ### Installation et Utilisation de ChromeDriver :

    - **Installation Automatique** : Le script utilise `webdriver_manager` pour installer automatiquement ChromeDriver.
    - **Pré-requis** : Vous devez avoir Google Chrome installé sur votre système.

    ### Options de ChromeDriver :

    - **`--headless`** : Exécute Chrome sans interface graphique.


    ### Options d'extraction :
    - Vous pouvez choisir d'extraire le texte brut ou de conserver les balises HTML/CSS.

    ### Instructions :
    1. Entrez l'URL du site web dont vous souhaitez extraire le texte.
    2. Sélectionnez le répertoire où le fichier texte extrait sera sauvegardé.
    3. Choisissez si vous souhaitez supprimer les balises HTML/CSS.
    4. Cliquez sur le bouton pour lancer l'extraction.

    ### Exemple d'URL :
    Vous pouvez essayer avec l'URL suivante pour tester l'extraction de texte :
    `https://www.radiofrance.fr/franceinter/podcasts/la-terre-au-carre/la-terre-au-carre-du-mercredi-28-aout-2024-3188623`
    """)

    # Saisie de l'URL
    url = st.text_input("Entrez l'URL du site web :")

    # Sélection du répertoire de sortie
    output_directory = st.text_input("Sélectionnez le répertoire de sauvegarde",
                                     value=os.path.expanduser("~/Documents/ATA"))

    # Option pour supprimer les balises HTML
    supprimer_balises_html = st.checkbox("Supprimer les balises HTML/CSS", value=True)

    # Bouton pour lancer l'extraction
    if st.button("Extraire le texte"):
        if url and output_directory:
            extraire_texte_depuis_site(url, output_directory, supprimer_balises_html)
        else:
            st.error("Veuillez entrer l'URL du site web et choisir un répertoire de sauvegarde.")
