


from textblob.download_corpora import download_all
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from collections import Counter

import os
import nltk
import zipfile
import requests

# ==================== Setup and Downloads ====================

def safe_download():
    # Set up paths
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    vader_dir = os.path.join(nltk_data_dir, 'sentiment')
    vader_path = os.path.join(vader_dir, 'vader_lexicon')
    vader_zip_path = os.path.join(vader_dir, 'vader_lexicon.zip')

    # Ensure directory exists
    os.makedirs(vader_dir, exist_ok=True)

    # Download VADER lexicon if not already present
    if not os.path.exists(vader_path):
        print("Downloading VADER lexicon manually...")
        url = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/sentiment/vader_lexicon.zip"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(vader_zip_path, 'wb') as f:
                f.write(response.content)

            with zipfile.ZipFile(vader_zip_path, 'r') as zip_ref:
                zip_ref.extractall(vader_dir)
            print("VADER lexicon downloaded and extracted.")
        except Exception as e:
            print(f"Failed to download VADER lexicon: {e}")
    else:
        print("VADER lexicon already present.")

    # Download TextBlob corpora if needed
    try:
        _ = TextBlob("test").sentiment
    except:
        print("Downloading TextBlob corpora...")
        download_all()
        print("TextBlob corpora downloaded.")

    # Trigger Roberta download through pipeline
    print("Preloading CardiffNLP Roberta model via pipeline...")
    try:
        _ = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("Roberta model and tokenizer downloaded.")
    except Exception as e:
        print(f"Failed to preload Roberta model: {e}")

# Run setup on import
safe_download()

# ==================== Load Models ====================

transformers_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

roberta_classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

# ==================== Classifiers ====================

def classify_textblob(text, friendly_threshold=0.3, hostile_threshold=-0.3):
    polarity = TextBlob(text).sentiment.polarity
    if polarity < hostile_threshold:
        return "hostile"
    elif polarity > friendly_threshold:
        return "friendly"
    else:
        return "neutral"

def classify_vader(text, friendly_threshold=0.3, hostile_threshold=-0.3):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)['compound']
    if score < hostile_threshold:
        return "hostile"
    elif score > friendly_threshold:
        return "friendly"
    else:
        return "neutral"

def classify_transformers(text):
    result = transformers_classifier(text)[0]
    label = result['label']
    if label == 'NEGATIVE':
        return "hostile"
    elif label == 'POSITIVE':
        return "friendly"
    else:
        return "neutral"

def classify_roberta(text):
    result = roberta_classifier(text)[0]
    label = result['label'].lower()  # 'negative', 'neutral', 'positive'
    return {
        'positive': 'friendly',
        'neutral': 'neutral',
        'negative': 'hostile'
    }.get(label, 'neutral')

# ==================== Majority Vote Classifier ====================

def classify(text, friendly_threshold=0.3, hostile_threshold=-0.3):
    results = [
        classify_textblob(text, friendly_threshold, hostile_threshold),
        classify_transformers(text),
        classify_roberta(text)
    ]
    counts = Counter(results)
    most_common = counts.most_common(1)[0]
    return most_common[0] if most_common[1] >= 2 else None














