import streamlit as st
import fitz  # PyMuPDF
import os


# Fonction pour traiter le PDF et le convertir en texte
def convertir_pdf_en_texte(pdf_path, output_directory, join_hyphenated_words=False, convert_to_lowercase=False,
                           pages='all'):
    # Définir le chemin de sortie du fichier texte
    output_path = os.path.join(output_directory, os.path.splitext(os.path.basename(pdf_path))[0] + '.txt')

    # Ouvrir le fichier PDF
    pdf_document = fitz.open(pdf_path)

    # Déterminer les pages à extraire
    if pages == 'all':
        pages_to_extract = range(len(pdf_document))
    else:
        try:
            pages_to_extract = [int(page) - 1 for page in pages.split(',')]
        except ValueError:
            st.error(
                "Numéros de pages invalides. Veuillez entrer des numéros de pages valides séparés par des virgules.")
            return

    # Initialiser une chaîne de caractères pour contenir le texte extrait
    text = ""

    # Parcourir les pages spécifiées du PDF
    for page_num in pages_to_extract:
        if page_num < len(pdf_document):
            page = pdf_document.load_page(page_num)
            blocks = page.get_text("blocks")  # Récupérer les blocs de texte

            # Trier les blocs par position verticale, puis par position horizontale
            blocks.sort(key=lambda b: (b[1], b[0]))

            # Extraire le texte de chaque bloc
            for block in blocks:
                block_text = block[4].replace('\n', ' ')
                text += block_text + "\n"
        else:
            st.warning(f"Page {page_num + 1} ignorée car elle n'existe pas dans le document.")

    # Post-traitement pour joindre les lignes
    lines = text.splitlines()
    joined_text = ""
    for i, line in enumerate(lines):
        if line.strip():  # S'il ne s'agit pas d'une ligne vide
            if join_hyphenated_words and joined_text.endswith(
                    '-'):  # Si la ligne précédente se termine par un trait d'union et l'option est activée
                joined_text = joined_text[:-1] + line.strip()  # Joindre sans le trait d'union
            elif i > 0 and not joined_text.endswith(
                    ('.', '!', '?')):  # Si la ligne précédente ne se termine pas par une ponctuation
                joined_text += " " + line.strip()
            else:
                joined_text += "\n" + line.strip()
        else:
            joined_text += "\n"

    # Suppression des espaces autour des traits d'union
    if join_hyphenated_words:
        joined_text = joined_text.replace('- ', '').replace(' -', '')

    # Conversion en minuscules
    if convert_to_lowercase:
        joined_text = joined_text.lower()

    # Écrire le texte extrait dans un fichier .txt
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(joined_text.strip())

    st.success(f"Le fichier texte a été créé : {output_path}")


# Interface Streamlit
def traitement_pdf():
    st.title("Convertisseur PDF en Texte")

    # Explication du fonctionnement
    st.markdown("""
    **Fonctionnement :**

    Ce script vous permet de convertir un fichier PDF en texte brut. Vous pouvez sélectionner le nombre de colonnes de votre document PDF (1, 2 ou 3) et choisir d'extraire toutes les pages ou seulement certaines pages spécifiques en les spécifiant.

    - **Toutes les pages** : Convertit l'intégralité du document PDF en texte.
    - **Pages spécifiques** : Vous pouvez entrer les numéros des pages que vous souhaitez extraire, séparés par des virgules (ex: `1,3,5-7`).

    Vous avez également la possibilité d'unir les mots coupés à la fin des lignes et de convertir le texte en minuscules.
    """)

    # Téléchargement du fichier PDF
    uploaded_pdf = st.file_uploader("Sélectionnez le fichier PDF", type="pdf")

    # Sélection du répertoire de sortie
    output_directory = st.text_input("Sélectionnez le répertoire de sortie", os.path.expanduser("~/Documents"))

    # Choix du nombre de colonnes
    columns = st.radio("Nombre de colonnes dans le PDF", options=[1, 2, 3], index=0)

    # Options de traitement
    join_hyphenated_words = st.checkbox('Unir les mots coupés', value=True)
    convert_to_lowercase = st.checkbox('Convertir en minuscules', value=False)

    # Choix des pages à extraire
    pages_option = st.radio("Choisissez les pages à extraire :", options=['Toutes les pages', 'Pages spécifiques'])
    pages = 'all' if pages_option == 'Toutes les pages' else st.text_input("Spécifiez les pages (ex: 1,3,5-7):")

    if uploaded_pdf and output_directory:
        # Sauvegarder temporairement le PDF téléchargé
        temp_pdf_path = os.path.join(output_directory, uploaded_pdf.name)
        with open(temp_pdf_path, "wb") as temp_pdf:
            temp_pdf.write(uploaded_pdf.getbuffer())

        # Bouton de conversion
        if st.button("Convertir le PDF en Texte"):
            convertir_pdf_en_texte(temp_pdf_path, output_directory, join_hyphenated_words, convert_to_lowercase, pages)

