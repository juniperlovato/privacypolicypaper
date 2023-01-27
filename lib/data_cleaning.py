import functools

import nltk
import pandas as pd
import numpy as np
from pandarallel import pandarallel

from .timed_execution import Timer

@functools.cache
def tokenizer():
    return nltk.tokenize.RegexpTokenizer(r'\w+')

def tokenize_series(series: pd.Series) -> pd.Series:
    return series.apply(tokenizer().tokenize) # type: ignore

def remove_non_letter_words(series: pd.Series) -> pd.Series:
    # remove words that don't start with a letter
    letter_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return series.apply(lambda x: [word for word in x if set(word).issubset(letter_set)])

def remove_stopwords(series: pd.Series) -> pd.Series:
    nltk.download('stopwords', quiet=True)
    stopwords = set(nltk.corpus.stopwords.words('english'))
    return series.apply(lambda words: [word for word in words if not word in stopwords]) # type: ignore

def stem_series(series: pd.Series, parallel: bool) -> pd.Series:
    stemmer = nltk.stem.snowball.EnglishStemmer()
    stem = lambda texts: [stemmer.stem(text) for text in texts]
    if parallel:
        pandarallel.initialize()
        return series.parallel_apply(stem) # type: ignore
    else:
        return series.apply(stem)

def combine_lists_of_bags(bag1: pd.DataFrame, bag2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([bag1, bag2], ignore_index=True, sort=False).fillna(0).astype(pd.SparseDtype(np.uint16, 0))

ALL_STEPS = set([
    'tokenize',
    'downcase',
    'remove_stopwords',
    'stem',
    'remove_short_words',
    'remove_non_letter_words',
])

def clean_series(srs: pd.Series, log: bool = True, parallel: bool = True, steps: set = ALL_STEPS) -> pd.Series:
    assert steps.issubset(ALL_STEPS)

    if 'tokenize' in steps:
        with Timer("Tokenizing text", log):
            srs = tokenize_series(srs)

    if 'downcase' in steps:
        with Timer("downcasing text", log):
            srs = srs.apply(lambda x: [word.lower() for word in x])

    if 'remove_stopwords' in steps:
        with Timer("Removing stopwords", log):
            srs = remove_stopwords(srs)

    if 'stem' in steps:
        with Timer("Stemming text", log):
            srs = stem_series(srs, parallel)

    if 'remove_short_words' in steps:
        with Timer("Removing very short words", log):
            srs = srs.apply(lambda x: [item for item in x if len(item) > 2])

    if 'remove_non_letter_words' in steps:
        with Timer("Removing non-letter words", log):
            srs = remove_non_letter_words(srs)

    return srs
