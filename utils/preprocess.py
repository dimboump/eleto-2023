from __future__ import annotations

import re

import pandas as pd

import utils.morph as morph


class TextPreprocessor:
    """Preprocess text by removing cross references and punctuation,
    and replacing numbers with zeros."""

    def __init__(
        self,
        text: str,
        *,
        remove_crossrefs: bool = True,
        digits_to_zeros: bool = True,
        remove_punctuation: bool = True,
        morphology: bool = False,
    ):
        self.text = text
        self.remove_crossrefs = remove_crossrefs
        self.digits_to_zeros = digits_to_zeros
        self.remove_punct = remove_punctuation
        self.morphology = morphology

    def _remove_crossrefs(self) -> None:
        """Remove cross references from text.
        A cross reference is a string of the form (ΑΚ 123) or (BGB § 123)."""
        pattern = r'\((ΑΚ|AK|BGB)[\s§]*\d+\)'
        self.text = re.sub(pattern, '', self.text)

    def _digits_to_zeros(self) -> None:
        """Replace all numbers with zeros (including article numbers),
        maintaining the same length of the string."""
        self.text = re.sub(r'\d', '0', self.text)

    def _remove_punctuation(self) -> None:
        """Remove punctuation from text."""
        self.text = re.sub(r'[^\w\s]', '', self.text)

    def _get_morphology(self) -> dict:
        """Return a dictionary of each token and its morphology
        from a text in a nested dictionary."""
        doc = morph.SpaCyModel('el_core_news_sm').get_doc(self.text)
        morphs = [morph.Morphology(token).get_morphology() for token in doc]
        return {'morphology': morphs}

    def preprocess(self) -> str:
        """Preprocess text by removing cross references and punctuation,
        and replacing numbers with zeros."""
        if self.remove_crossrefs:
            self._remove_crossrefs()
        if self.digits_to_zeros:
            self._digits_to_zeros()
        if self.remove_punct:
            self._remove_punctuation()
        if self.morphology:
            self._get_morphology()
        return self.text


class DataFramePreprocessor:
    """Preprocess a dataframe by adding a column with the preprocessed text."""

    def __init__(
        self,
        df: pd.DataFrame,
        remove_crossrefs: bool = True,
        digits_to_zeros: bool = True,
        remove_punctuation: bool = True,
        morphology: bool = False,
    ):
        self.df = df
        self.remove_crossrefs = remove_crossrefs
        self.digits_to_zeros = digits_to_zeros
        self.remove_punct = remove_punctuation
        self.morphology = morphology

    def check_df(self) -> None:
        """Check if df is a non-empty pandas DataFrame."""
        if not isinstance(self.df, pd.DataFrame) or self.df.empty:
            raise ValueError('df must be a non-empty pandas DataFrame')

    def preprocess(self) -> pd.DataFrame:
        preprocessed = (self.df['text']
                        .apply(lambda x: TextPreprocessor(
                            x,
                            remove_crossrefs=self.remove_crossrefs,
                            digits_to_zeros=self.digits_to_zeros,
                            remove_punctuation=self.remove_punct,
                            morphology=self.morphology,
                        ).preprocess()))
        preprocessed_df = pd.DataFrame({'preprocessed': preprocessed})
        return pd.concat([self.df, preprocessed_df], axis=1)
