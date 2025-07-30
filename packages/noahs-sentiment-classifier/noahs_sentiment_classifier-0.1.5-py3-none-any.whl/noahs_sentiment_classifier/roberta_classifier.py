from transformers import pipeline

def safe_download():
    try:
        _ = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("[Roberta] Model downloaded.")
    except Exception as e:
        print(f"[Roberta] Failed to preload model: {e}")

safe_download()

_classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def classify_roberta(text):
    result = _classifier(text)[0]
    label = result['label'].lower()
    return {
        'positive': 'friendly',
        'neutral': 'neutral',
        'negative': 'hostile'
    }.get(label, 'neutral')
