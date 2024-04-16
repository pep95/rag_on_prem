import pandas as pd
import logging
import numpy as np
import re
from config import Settings
settings = Settings()

stopword_path = settings.STOP_WORD_PATH
def get_stop_words():
    """
    This function loads stopwords from a given path.

    Parameters
    ----------
    stopword_path : str
        stopword support file path

    Returns
    ---------
    stop_set: frozenset
        immutable stopwords set
    """

    with open(stopword_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = frozenset(m.strip() for m in stopwords)

        return stop_set

stopwords = get_stop_words()


logger = logging.getLogger(__name__)

# threshold for the minimum number of unique items in a column to be considered as valid
NUMERIC_ELEMENTS_THRESHOLD = 10





def clean_stopwords(text, stopword_set):
    """
    This function cleans a given text from the loaded stopwords.

    Parameters
    ----------
    text : str
        text to be cleaned

    stopword_set : frozenset
        immutable stopword set

    Returns
    ---------
    text: str
        cleaned text
    """

    text = ' '.join(word for word in text.split() if word not in stopword_set)

    return text

def clean_str(string):
    """
    This function cleans a given string:
    - it removes punctuation
    - it convert double or more consecutive spaces into one
    - it removes spaces both at the beginning and at the end of the string
    - it transform the string in lowercase

    Parameters
    ----------
    string : str
        string to clean

    Returns
    ---------
    cleaned_string: str
        cleaned string
    """
    cleaned_string = re.sub(r"[^A-Za-z0-9àèìòùÀÈÌÒÙáéíóÁÉÍÓ]", " ", string)
    cleaned_string = re.sub(r"\s{2,}", " ", cleaned_string)
    cleaned_string = cleaned_string.strip().lower()
    # cleaned_string = lemmatize_words(cleaned_string)

    return cleaned_string

def text_cleaning(field):
    """
    This function cleans string elements inside the field passed.

    Parameters
    ----------
    field : string
        text field to pre-process and clean

    """


    if not isinstance(field, str):
        field = str(field)

    field = clean_str(field)
    field = clean_stopwords(field, stopwords)

    return field


