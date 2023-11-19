import spacy
from IPython.core.display import HTML
from IPython.display import display
from spacy import displacy
from spacy.language import Language
from spacy.tokens import Doc

COLORS = {
    'de': '#a52040',
    'el': '#404080',
    'stern_yellow': '#c3c31d',
    'stern_blue': '#0b3f7e',
    'stern_purple': '#7c7cf8',
    'stern_darkbrown': '#370306',
    'darkgreen': '#006400',
    'orange': '#f4a460',
    'green': '#90ee90',
    'blue': '#add8e6',
    'purple': '#800080',
    'err': '#b4b446',
}

POS_COLORS = [
    "#FFD700",  # Gold
    "#90EE90",  # Light Green
    "#FFA07A",  # Light Salmon
    "#AFEEEE",  # Pale Turquoise
    "#F08080",  # Light Coral
    "#ADD8E6",  # Light Blue
    "#FFB6C1",  # Light Pink
    "#FFE4B5",  # Moccasin
    "#B0E0E6",  # Powder Blue
    "#D3D3D3",  # Light Grey
    "#E6E6FA",  # Lavender
    "#FFDEAD",  # Navajo White
    "#F5DEB3",  # Wheat
    "#FFFACD",  # Lemon Chiffon
    "#BDB76B",  # Dark Khaki
    "#8787df",  # Light Slate Blue
    "#E0FFFF",  # Light Cyan
]


class Grammar:
    """A class to get the grammar of a spaCy token."""

    def __init__(self, token: spacy.tokens.token.Token):
        self.token = token

    def get_grammar(self) -> dict:
        """Return a dictionary of each token and its part of speech
        from a text in a nested dictionary."""
        return {self.token.text: self.token.pos_}

    @property
    def token(self) -> spacy.tokens.token.Token:
        return self._token

    @token.setter
    def token(self, token: spacy.tokens.token.Token) -> None:
        self._token = token


class CustomTagger:
    def __init__(self, nlp):
        self.nlp = nlp

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            token.tag_ = token.pos_
        return doc

    if not Language.has_factory("custom_tagger"):
        @Language.factory("custom_tagger")
        def create_custom_tagger(nlp, name):
            return CustomTagger(nlp)

    def add_pipe(self, *, before: str = None) -> None:
        """Add a custom tagger to the spaCy pipeline."""
        self.nlp.add_pipe('custom_tagger', before=before)


class VisualPOS:
    def __init__(
        self,
        text: str,
        model: spacy.language.Language,
        colors: list = POS_COLORS
    ):
        self.text = text
        self.nlp = model
        self.colors = colors

    def render(self, text: str = None) -> None:
        """Render a spaCy doc with POS tags."""

        if text is None:
            text = self.text

        doc = self.nlp(text)

        # get the labels, iterate over them and extract the POS tags
        pos_tags = list(self.nlp.get_pipe('custom_tagger').labels)
        pos_tags = [tag.split('POS=')[1].split('|')[0] for tag in pos_tags]
        pos_tags = sorted(list(set(pos_tags)))

        colormap = dict(zip(pos_tags, self.colors))

        ents = []
        for token in doc:
            if token.pos_ in pos_tags:
                ents.append({'start': token.idx,
                             'end': token.idx + len(token),
                             'label': token.pos_})

        doc = {'text': doc.text, 'ents': ents}

        options = {'ents': pos_tags, 'colors': colormap}

        html = displacy.render(doc,
                               style='ent',
                               options=options,
                               manual=True,
                               jupyter=True,
                               )
        display(HTML(html))

    @property
    def colors(self) -> list:
        return self._colors

    @colors.setter
    def colors(self, colors: list) -> None:
        self._colors = colors
