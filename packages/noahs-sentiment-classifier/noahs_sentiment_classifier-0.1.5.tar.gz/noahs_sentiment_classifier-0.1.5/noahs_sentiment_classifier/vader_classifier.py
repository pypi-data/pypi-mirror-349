import os
import nltk
import requests
import zipfile
from nltk.sentiment import SentimentIntensityAnalyzer

def safe_download():
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    vader_dir = os.path.join(nltk_data_dir, 'sentiment')
    vader_path = os.path.join(vader_dir, 'vader_lexicon')
    vader_zip_path = os.path.join(vader_dir, 'vader_lexicon.zip')

    os.makedirs(vader_dir, exist_ok=True)

    if not os.path.exists(vader_path):
        print("[VADER] Downloading lexicon manually...")
        url = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/sentiment/vader_lexicon.zip"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(vader_zip_path, 'wb') as f:
                f.write(response.content)
            with zipfile.ZipFile(vader_zip_path, 'r') as zip_ref:
                zip_ref.extractall(vader_dir)
            print("[VADER] Lexicon downloaded and extracted.")
        except Exception as e:
            print(f"[VADER] Failed to download lexicon: {e}")
    else:
        print("[VADER] Lexicon already present.")

    nltk.data.path.append(nltk_data_dir)

safe_download()

def classify_vader(text, friendly_threshold=0.3, hostile_threshold=-0.3):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)['compound']
    if score < hostile_threshold:
        return "hostile"
    elif score > friendly_threshold:
        return "friendly"
    else:
        return "neutral"







