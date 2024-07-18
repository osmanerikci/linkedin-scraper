from sklearn.feature_extraction.text import TfidfVectorizer

def extract_top_keywords(texts, top_n=50):
    """
    Extracts the top keywords from the input texts using TF-IDF.

    Args:
        texts (iterable): The input texts.
        top_n (int): The number of top keywords to return.

    Returns:
        list of tuples: The top keywords and their TF-IDF scores.
    """
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(texts)

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Sum the TF-IDF values for each term across all documents
    sum_tfidf = X.sum(axis=0)
    tfidf_scores = [(word, sum_tfidf[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    tfidf_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    return tfidf_scores[:top_n]
