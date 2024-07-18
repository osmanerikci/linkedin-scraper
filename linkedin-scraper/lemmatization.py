import spacy

nlp = spacy.load('en_core_web_sm')

def lemmatize_text(text):
    """
    Lemmatizes the input text using spaCy.

    Args:
        text (str): The input text.

    Returns:
        str: The lemmatized text.
    """
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])
