# Extract the function words from the set of stopwords
# for Greek and German, by using the POS tagger.
import spacy


class FunctionWords:
    """A class to get the function words from a text."""

    def __init__(self, text: str, language: str = 'el', model: spacy.language.Language = None):
        self.text = text
        self.language = language
        self.model = model

    def get_function_words(self) -> list:
        """Return a list of function words from a text."""
        if self.language in {'el', 'de'}:
            return self.get_function_words()
        else:
            raise ValueError(f"Language {self.language} is not supported.")

    def get_function_words(self) -> list | None:
        """Return a list of function words from a text in English.
        Function words include only determiners, pronouns, prepositions,
        and conjunctions."""
        doc = self.get_doc()
        function_words = [token.pos_ for token in doc
                          if token.pos_ in {'DET', 'PRON', 'ADP', 'CCONJ'}]
        return function_words

    def get_doc(self) -> spacy.tokens.doc.Doc:
        """Return a spaCy doc from a text."""
        return self.nlp(self.text)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        self._language = language

    @property
    def nlp(self) -> spacy.language.Language:
        return self._nlp

    @nlp.setter
    def nlp(self, model: spacy.language.Language) -> None:
        self._nlp = model
