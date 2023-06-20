from __future__ import annotations
import re

import pandas as pd


class TextPreprocessor:
    """Preprocess text by removing cross references and punctuation,
    and replacing numbers with zeros."""
    def __init__(self, text: str):
        self.text = text

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

    def preprocess(self) -> str:
        """Preprocess text by removing cross references and punctuation, 
        and replacing numbers with zeros."""
        self._remove_crossrefs()
        self._digits_to_zeros()
        self._remove_punctuation()
        return self.text


class DataFramePreprocessor:
    """Preprocess a dataframe by adding a column with the preprocessed text."""
    def __init__(self, df):
        self.df = df
    
    def preprocess(self):
        preprocessed_texts = self.df['text'].apply(lambda x: TextPreprocessor(x).preprocess())
        preprocessed_df = pd.DataFrame({'preprocessed_text': preprocessed_texts})
        return pd.concat([self.df, preprocessed_df], axis=1)