from transformers import pipeline

def safe_download():
    try:
        _ = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        print("[Transformers] Model downloaded.")
    except Exception as e:
        print(f"[Transformers] Failed to preload model: {e}")

safe_download()

_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def classify_transformers(text):
    result = _classifier(text)[0]
    label = result['label']
    if label == 'NEGATIVE':
        return "hostile"
    elif label == 'POSITIVE':
        return "friendly"
    else:
        return "neutral"
