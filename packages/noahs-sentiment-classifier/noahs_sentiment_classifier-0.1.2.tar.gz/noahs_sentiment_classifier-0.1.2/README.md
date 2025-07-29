



# Noah's Sentiment Classifier

A simple ensemble sentiment classifier using TextBlob, VADER, and Transformers (including Roberta).

## Installation

```bash
pip install noahs_sentiment_classifier
```

## Code Sample

```python
from noahs_sentiment_classifier import classify, classify_textblob, classify_vader, classify_transformers, classify_roberta

value = classify("i hate you")
# value will be either "hostile","friendly","neutral" 
# or None if there is uncertainty

value2 = classify_textblob("i love you")
# value2 will be either "hostile","friendly","neutral" 

```