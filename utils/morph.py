import spacy

import utils.grammar as grammar


class Morphology:
    """A class to get the morphology of a spaCy token."""

    def __init__(self, token: spacy.tokens.token.Token, grammar: bool = False):
        self.token = token
        self.grammar = grammar

    def get_grammar(self) -> dict:
        """Return a dictionary of each token and its grammar
        from a text in a nested dictionary."""
        return grammar.Grammar(self.token).get_grammar()

    def get_morphology(self) -> dict:
        """Return a dictionary of each token and its morphology
        from a text in a nested dictionary."""
        if self.grammar:
            return {
                self.token.text: {
                    'POS': self.get_grammar().get(self.token.text),
                    **self.token.morph.to_dict()
                }
            }
        return {self.token.text: self.token.morph.to_dict()}

    @property
    def token(self) -> spacy.tokens.token.Token:
        return self._token

    @token.setter
    def token(self, token: spacy.tokens.token.Token) -> None:
        self._token = token
