import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

nltk.download('stopwords')

# Combine NLTK and sklearn stop words
stop_words = set(stopwords.words('english')).union(set(stopwords.words('german')), set(stopwords.words('french')), ENGLISH_STOP_WORDS)

def preprocess_text(text):
    """
    Preprocesses the input text by converting to lowercase, removing special characters and numbers, and removing stop words.

    Args:
        text (str): The input text.

    Returns:
        str: The preprocessed text.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove stop words
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text
