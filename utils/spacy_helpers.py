import spacy


class SpaCyModel:
    """A class to load a spaCy model."""

    def __init__(self, model: str):
        self.model = model
        self.nlp = self.load_model(self.model)

    def download_model(self, model: str) -> None:
        """Download a spaCy model."""
        spacy.cli.download(model)

    def load_model(self, model: str) -> spacy.language.Language:
        if not spacy.util.is_package(model):
            self.download_model(model)
        return spacy.load(model)

    def get_doc(self, text: str) -> spacy.tokens.doc.Doc:
        return self.nlp(text)

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        self._model = model
