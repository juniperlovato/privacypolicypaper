from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def build_matrix(documents: list[str], vocabulary: list[str]) -> pd.DataFrame:
    # build cooccurrent matrix
    # only count one co-occurence per pair of terms per document
    # e.g. if a document contains "biometric geolocation" twice, we only count one co-occurrence
    # between "biometric" and "geolocation"
    vectorizer = CountVectorizer(vocabulary=vocabulary, binary=True, ngram_range=(1, 4))
    term_doc_matrix = vectorizer.fit_transform(documents)
    cooccurrence_matrix = term_doc_matrix.T * term_doc_matrix
    cooccurrence_matrix.setdiag(0)

    # convert to pandas dataframe
    return pd.DataFrame(cooccurrence_matrix.toarray(), index=vocabulary, columns=vocabulary)

