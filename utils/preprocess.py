from __future__ import annotations
import re

import pandas as pd


class TextPreprocessor:
    """Preprocess text by removing cross references and punctuation,
    and replacing numbers with zeros."""
    def __init__(
        self, 
        text: str, 
        remove_crossrefs: bool = True, 
        digits_to_zeros: bool = True, 
        remove_punctuation: bool = True
    ):
        self.text = text
        self.remove_crossrefs = remove_crossrefs
        self.digits_to_zeros = digits_to_zeros
        self.remove_punctuation = remove_punctuation

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
        if self.remove_crossrefs: self._remove_crossrefs()
        if self.digits_to_zeros: self._digits_to_zeros()
        if self.remove_punctuation: self._remove_punctuation()
        return self.text


class DataFramePreprocessor:
    """Preprocess a dataframe by adding a column with the preprocessed text."""
    def __init__(
        self,
        df: pd.DataFrame,
        remove_crossrefs: bool = True,
        digits_to_zeros: bool = True,
        remove_punctuation: bool = True
    ):
        self.df = df
        self.remove_crossrefs = remove_crossrefs
        self.digits_to_zeros = digits_to_zeros
        self.remove_punctuation = remove_punctuation
    
    def preprocess(self):
        preprocessed = (self.df['text']
                        .apply(lambda x: TextPreprocessor(x,
                                                          self.remove_crossrefs,
                                                          self.digits_to_zeros,
                                                          self.remove_punctuation
                                                         ).preprocess()))
        preprocessed_df = pd.DataFrame({'preprocessed': preprocessed})
        return pd.concat([self.df, preprocessed_df], axis=1)