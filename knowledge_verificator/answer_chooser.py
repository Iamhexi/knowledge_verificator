"""Module with AnswerChooser, which finds a best candidate for an answer in a paragraph."""

import random
import nltk
from nltk.corpus import wordnet

# FIXME: Write docstrings.


class AnswerChooser:
    def __init__(self) -> None:
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('punkt_tab')

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from a string using NLTK.
        """
        # Get the stopwords from the NLTK stopwords corpus
        stopwords = set(nltk.corpus.stopwords.words('english'))

        # Tokenize the text into words
        words = nltk.word_tokenize(text)

        # Remove the stopwords from the words
        filtered_words = [
            word for word in words if word.lower() not in stopwords
        ]

        # Join the filtered words back into a string
        cleaned_text = ' '.join(filtered_words)

        # Return the cleaned text
        return cleaned_text

    def santize(self, word: str) -> str:
        """Convert to lowercase and remove any punctuation mark."""
        word = word.strip()
        word = word.lower()
        to_remove = ('.', ',', '?', '!', '-', '_', '/', '(', ')', "'")
        for punctuation_mark in to_remove:
            word = word.replace(punctuation_mark, '')
        return word

    def find_part_of_speech(self, word: str) -> str:
        """
        Determine the part of speech of a word using WordNet.
        """
        # Look up the word in WordNet
        word = self.santize(word=word)
        synsets = wordnet.synsets(word)

        # If the word is not found, return 'n/a'
        if not synsets:
            return 'n/a'

        # Get the first synset and determine the part of speech
        synset = synsets[0]
        pos = synset.pos()

        # Map WordNet POS tags to more common POS tags
        if pos == 'a':
            return 'adjective'
        elif pos == 'n':
            return 'noun'
        elif pos == 'r':
            return 'adverb'
        elif pos == 'v':
            return 'verb'
        else:
            return 'n/a'

    def choose_answer(self, paragraph: str) -> str:
        paragraph = self.remove_stopwords(paragraph)
        words = paragraph.split(' ')
        # FIXME: Refactor not to use three times the same function...
        words = [
            self.santize(word)
            for word in words
            if self.santize(word)
            and self.find_part_of_speech(self.santize(word)) == 'n/a'
        ]

        return random.choice(words)
