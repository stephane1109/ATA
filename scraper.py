import streamlit as st
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import os


# Fonction pour nettoyer les emojis tout en conservant les accents
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)  # Supprime les emojis du texte


def get_video_details(youtube, video_id):
    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    if not response['items']:
        return None, None  # Si aucune vidéo n'est trouvée
    video_details = response['items'][0]['snippet']
    title = remove_emojis(video_details['title'])  # Supprime les emojis du titre
    published_at = video_details['publishedAt']
    return title, published_at


def fetch_comments(youtube, video_id, max_results=100):
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=max_results,
            order="time"  # Récupère également les réponses aux commentaires, triées par date
        ).execute()
        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comment = remove_emojis(comment).lower()  # Nettoyer les emojis et passer en minuscules
                comments.append(comment)
            if 'nextPageToken' in response:
                response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    textFormat="plainText",
                    maxResults=max_results
                ).execute()
            else:
                break
    except HttpError as e:
        st.error(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    return comments


def get_channel_name(youtube, video_id):
    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    if not response['items']:
        return None
    channel_title = response['items'][0]['snippet']['channelTitle']
    return channel_title


def save_data_to_file(title, published_at, channel_name, comments, output_directory, options):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    filename = os.path.join(output_directory, 'youtube_comments.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        if not options.get('remove_metadata'):
            published_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').date()
            file.write(
                f'Channel: {channel_name}\nTitle: {title}\n\nComments:\n\n')

        for comment in comments:
            if options.get('prepend_hash'):
                comment = f'# {comment}'
            if options.get('remove_special_characters'):
                # Remplace les caractères non alphanumériques à l'exception des accents et des apostrophes
                comment = re.sub(r'[^a-zA-Z0-9\s\'éàèùâêîôûç]', '', comment)
            file.write(comment + "\n\n")
    st.success(f"Les commentaires ont été sauvegardés dans {filename}")


def afficher_interface_scraper_youtube_comments():
    st.title("Scraper les commentaires YouTube")

    st.markdown("""
    ### Fonctionnement :

    1. **Obtenir une clé API YouTube :**
        - Connectez-vous à [Google Cloud Console](https://console.cloud.google.com/).
        - Créez un projet ou sélectionnez un projet existant.
        - Activez l'API "YouTube Data API v3" dans la bibliothèque d'APIs.
        - Allez dans "API et services" > "Identifiants", et créez une "Clé API".
        - Copiez la clé API générée, qui ressemblera à quelque chose comme `AIzaSyD3V-4XX5D5XXX5XXXXXvM79HHp5XXXXXxg`.

    2. **Utiliser la clé API dans le script :**
        - Collez la clé API obtenue dans le champ approprié du script.
        - Remplacez l'URL de la vidéo par celle que vous souhaitez scraper.

    ### Exemple :
    - Pour l'URL `https://youtube.com/shorts/WraeFTmQ-Sg?si=748QYhUIU0760x6V`, extrayez l'ID `748QYhUIU0760x6V`.
    - Saisissez cet ID dans le champ "ID de la vidéo" pour scraper les commentaires de cette vidéo.

    **Note :** Assurez-vous de protéger votre clé API, car elle permet d'accéder aux services YouTube Data API.
    """)

    api_key = st.text_input("Entrez votre clé API YouTube :")
    url_video = st.text_input("Entrez l'URL de la vidéo YouTube :")
    max_results = st.number_input("Nombre maximal de commentaires à récupérer :", min_value=1, max_value=100, value=100)
    output_directory = st.text_input("Définir le répertoire de sauvegarde",
                                     value=os.path.expanduser("~/Documents/ATA/YoutubeComments"))

    prepend_hash = st.checkbox("Ajouter un # devant chaque commentaire")
    remove_special_characters = st.checkbox(
        "Nettoyer les caractères spéciaux (supprime tout sauf les accents et les apostrophes)")
    remove_metadata = st.checkbox("Supprimer le nom de l'auteur et la date")

    options = {
        "prepend_hash": prepend_hash,
        "remove_special_characters": remove_special_characters,
        "remove_metadata": remove_metadata
    }

    if st.button("Scraper les commentaires"):
        if not api_key or not url_video:
            st.error("Veuillez entrer une clé API et une URL de vidéo valides.")
            return

        match = re.search(r"((?<=[?&]v=)|(?<=/videos/)|(?<=/shorts/))([a-zA-Z0-9_-]+)", url_video)
        if not match:
            st.error("L'URL de la vidéo ne semble pas valide.")
            return

        video_id = match.group(2)
        youtube = build('youtube', 'v3', developerKey=api_key)

        title, published_at = get_video_details(youtube, video_id)
        channel_name = get_channel_name(youtube, video_id)

        if title is None or published_at is None or channel_name is None:
            st.error("Impossible de récupérer les détails de la vidéo.")
        else:
            comments = fetch_comments(youtube, video_id, max_results=max_results)
            save_data_to_file(title, published_at, channel_name, comments, output_directory, options)
