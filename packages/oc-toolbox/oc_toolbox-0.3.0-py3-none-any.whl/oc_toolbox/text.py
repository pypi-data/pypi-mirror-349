import re
from difflib import SequenceMatcher
from typing import List

import numpy as np
import pandas as pd


def clean_text(
    text: str,
    lang: str = "english",
) -> List[str]:
    """
    Cleans a text string by lowercasing, removing punctuation,
    and eliminating stopwords.

    Parameters
    ----------
    text : str
        The input text to clean.
    lang : str, optional
        Language for stopwords (default is 'english').

    Returns
    -------
    List[str]
        A list of cleaned tokens without stopwords or punctuation.

    Notes
    -----
    - Requires NLTK's stopwords and tokenizer (`nltk.download('punkt')`, `nltk.download('stopwords')`).
    """
    if pd.isnull(text):
        return []

    import nltk

    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words(lang))

    return [word for word in tokens if word not in stop_words]


def _jaccard_similarity(a, b):
    set_a = set(str(a).split())
    set_b = set(str(b).split())
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return len(intersection) / len(union) if union else 0


def _similarity_ratio(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()


def compare_text_columns(df, col1="corpus_text", col2="lemmas_nltk_text"):
    result_df = df[[col1, col2]].copy()

    result_df["equal"] = df[col1] == df[col2]

    result_df["jaccard_similarity"] = df.apply(
        lambda row: _jaccard_similarity(row[col1], row[col2]), axis=1
    )

    result_df["similarity_ratio"] = df.apply(
        lambda row: _similarity_ratio(row[col1], row[col2]), axis=1
    )

    result_df["len_corpus"] = df[col1].str.split().str.len()
    result_df["len_lemmas"] = df[col2].str.split().str.len()

    result_df["length_difference"] = result_df["len_corpus"] - result_df["len_lemmas"]

    return result_df[result_df[col1] != result_df[col2]].reset_index(drop=True)


def extract_fasttext_features(sentence, model=None):
    if model is None:
        from gensim.models import KeyedVectors

        model = KeyedVectors.load_word2vec_format(
            "cc.en.300.vec",
            binary=False,
        )

    tokens = sentence.lower().split()

    vectors = [model[word] for word in tokens if word in model]

    if not vectors:
        return np.zeros(model.vector_size)

    return np.mean(
        vectors,
        axis=0,
    )


def lemmatize_tokens_nltk(text):
    import nltk

    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)

    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    lemmatizer_nltk = WordNetLemmatizer()
    tokens_nltk = word_tokenize(text.lower())

    return [lemmatizer_nltk.lemmatize(token) for token in tokens_nltk]


def lemmatize_tokens_spacy(text, nlp_spacy=None):
    if nlp_spacy is None:
        import spacy

        nlp_spacy = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    doc_spacy = nlp_spacy(text)

    return [token.lemma_ for token in doc_spacy]


def lemmatize_tokens_stanza(text, batch_size=64, nlp_stanza=None):
    if nlp_stanza is None:
        import stanza

        nlp_stanza = stanza.Pipeline(
            lang="en",
            ner_batch_size=batch_size,
            processors="tokenize,mwt,pos,lemma",
            tokenize_batch_size=batch_size,
            verbose=False,
        )

    doc_stanza = nlp_stanza(text)

    return [word.lemma for sent in doc_stanza.sentences for word in sent.words]


def list_pred_text(
    df,
    incorrect_only=True,
    limit=5,
    limit_incorrect=1,
    text_col="text",
    y_pred_col="y_pred",
    y_true_col="category_encoded",
    y_true_only_list=None,
    y_mapping=None,
):
    def _list(_df, _limit=limit):
        for i, row in enumerate(_df.head(_limit).itertuples()):
            _text = getattr(row, text_col)
            print(f"- {_text}")
            print()

    for category in sorted(df[y_true_col].unique()):
        if y_true_only_list is not None and category not in y_true_only_list:
            continue

        subset = df[df[y_true_col] == category]

        correct = subset[subset[y_true_col] == subset[y_pred_col]]
        incorrect = subset[subset[y_true_col] != subset[y_pred_col]]

        if y_mapping is not None:
            category = f"{category} - {y_mapping[category]}"

        print(category)
        print()

        if not incorrect_only and not correct.empty:
            _list(correct)
            print()

        if not incorrect.empty:
            # Grouper par la mauvaise catégorie prédite et trier par fréquence décroissante
            pred_counts = (
                incorrect[y_pred_col].value_counts().sort_values(ascending=False).index
            )

            for pred_cat in pred_counts[: min(len(pred_counts), limit_incorrect)]:
                label = (
                    f"{pred_cat} - {y_mapping[pred_cat]}"
                    if y_mapping
                    else str(pred_cat)
                )
                print(f"→ Incorrectement classé comme : {label}")
                print()

                _list(incorrect[incorrect[y_pred_col] == pred_cat])
                print()
