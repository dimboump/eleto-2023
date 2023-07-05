# Get the absolute and relative frequencies of the number of:
# - words per sentence
# - parts of speech
# - function words
# - civil code / legal terms
# - subordinate clauses
# - prepositional phrases
import spacy

import utils.stopwords as stopwords


class Frequencies:
    """A class to get the frequencies of a text."""

    def __init__(
        self,
        text: str,
        language: str = 'el',
        model: spacy.language.Language = None,
        stopwords: list = None
    ):
        self.text = text
        self.language = language
        self.model = model
        self.stopwords = stopwords

    def get_frequencies(self) -> dict:
        """Return a dictionary of the frequencies of a text."""
        return {
            'words_per_sentence': self.words_per_sentence_freq(),
            'parts_of_speech': self.parts_of_speech_freq(),
            'function_words': self.function_words_freq(),
            'civil_code_terms': self.civil_code_terms_freq(),
            'subordinate_clauses': self.subordinate_clauses_freq(),
            'prepositional_phrases': self.prepositional_phrases_freq()
        }

    def words_per_sentence_freq(self) -> dict:
        """Return a dictionary of the frequencies of the number of words
        per sentence."""
        words_per_sentence = self.get_words_per_sentence()
        return {
            'absolute': words_per_sentence,
            'relative': self.get_relative_frequencies(words_per_sentence)
        }

    def parts_of_speech_freq(self) -> dict:
        """Return a dictionary of the frequencies of parts of speech."""
        parts_of_speech = self.get_parts_of_speech()
        return {
            'absolute': parts_of_speech,
            'relative': self.get_relative_frequencies(parts_of_speech)
        }

    def function_words_freq(self) -> dict:
        """Return a dictionary of the frequencies of function words."""
        function_words = self.get_function_words()
        return {
            'absolute': function_words,
            'relative': self.get_relative_frequencies(function_words)
        }

    def civil_code_terms_freq(self) -> dict:
        """Return a dictionary of the frequencies of civil code terms."""
        civil_code_terms = self.get_civil_code_terms()
        return {
            'absolute': civil_code_terms,
            'relative': self.get_relative_frequencies(civil_code_terms)
        }

    def subordinate_clauses_freq(self) -> dict:
        """Return a dictionary of the frequencies of subordinate clauses."""
        subordinate_clauses = self.get_subordinate_clauses()
        return {
            'absolute': subordinate_clauses,
            'relative': self.get_relative_frequencies(subordinate_clauses)
        }

    def prepositional_phrases_freq(self) -> dict:
        """Return a dictionary of the frequencies of prepositional phrases."""
        prepositional_phrases = self.get_prepositional_phrases()
        return {
            'absolute': prepositional_phrases,
            'relative': self.get_relative_frequencies(prepositional_phrases)
        }

    def get_words_per_sentence(self) -> list:
        """Return a list of the number of words per sentence."""
        return [len(sentence) for sentence in self.get_sentences()]

    def get_sentences(self) -> list:
        """Return a list of sentences from a text."""
        return [sentence for sentence in self.get_doc().sents]

    def get_parts_of_speech(self) -> list:
        """Return a list of parts of speech from a text."""
        return [token.pos_ for token in self.get_doc()]

    def get_function_words(self) -> list:
        """Return a list of function words from a text."""
        fn_words = stopwords.FunctionWords(
            self.text, self.language, self.model)
        return fn_words.get_function_words()

    def get_legal_terms(self) -> list:
        """Return a list of legal terms from a text. Legal terms are annotated
        in-text with the custom spaCy pipeline component LegalTerms."""
        return [token.text for token in self.get_doc().ents if token.label_ == 'LEGAL_TERM']


class LegalTerms:
    """A spaCy pipeline component to annotate legal terms in a text.
    The terms have been manually annotated in-text with HTML tags."""
    name = 'legal_terms'

    def __init__(self, nlp):
        """Initialise the pipeline component."""
        self.nlp = nlp
        self.labels = ['LEGAL_TERM']

        # Register the custom attribute on the Token class
        Token.set_extension('is_legal_term', default=False, force=True)

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object."""
        # Iterate over the matches
        for match_id, start, end in self.matcher(doc):
            # Get the matched span
            span = doc[start:end]
            # Set the Token attribute is_legal_term to True
            for token in span:
                token._.set('is_legal_term', True)
        return doc

    def add_label(self, label):
        """Add a new label to the pipe."""
        self.labels.append(label)
        self.matcher.add(label, None, [{'TAG': 'LEGAL_TERM'}])
