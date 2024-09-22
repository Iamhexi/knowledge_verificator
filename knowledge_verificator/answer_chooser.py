"""Module with AnswerChooser, which finds a best candidate for an answer in a paragraph."""

import random
import nltk  # type: ignore[import-untyped]
from nltk.corpus import wordnet  # type: ignore[import-untyped]
from tqdm import tqdm  # type: ignore[import-untyped]


class AnswerChooser:
    """
    Class choosing an answer from a paragraph for Question Generation module.
    """

    def __init__(self) -> None:
        dependencies = ('wordnet', 'stopwords', 'punkt')
        for dependency in tqdm(
            dependencies,
            desc='Downloading required files',
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} files',
        ):
            nltk.download(dependency, quiet=True)

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stop words such as `the`, `and` and so on.

        Args:
            text (str): Text to be cleansed.

        Returns:
            str: Cleansed text.
        """
        stopwords = set(nltk.corpus.stopwords.words('english'))
        words = nltk.word_tokenize(text)

        filtered_words = [
            word for word in words if word.lower() not in stopwords
        ]

        cleaned_text = ' '.join(filtered_words)
        return cleaned_text

    def santize(self, word: str) -> str:
        """
        Convert to lowercase and remove any punctuation mark.

        Args:
            word (str): Word to santize.

        Returns:
            str: Sanitized word.
        """
        word = word.strip()
        word = word.lower()
        to_remove = ('.', ',', '?', '!', '-', '_', '/', '(', ')', "'")
        for punctuation_mark in to_remove:
            word = word.replace(punctuation_mark, '')
        return word

    def find_part_of_speech(self, word: str) -> str:
        """
        Determine the part of speech of a word using WordNet.

        Args:
            word (str): Word, for which part of speech should be determined.

        Returns:
            str: Part of speech of the supplied word.
        """
        word = self.santize(word=word)
        synsets = wordnet.synsets(word)

        # If the word is not found, return 'n/a'
        if not synsets:
            return 'n/a'

        synset = synsets[0]
        pos = synset.pos()

        match pos:
            case 'a':
                return 'adjective'
            case 'n':
                return 'noun'
            case 'r':
                return 'adverb'
            case 'v':
                return 'verb'
            case _:
                return 'n/a'

    def choose_answer(self, paragraph: str) -> str | None:
        """
        Choose a good candidate for an answer from a paragraph.

        Choose a good candidate from `paragraph` based on the following algorithm:
        1. Remove stop words.
        2. If any unknown word is present, a random unknown word is chosen.
        3. Otherwise, a random noun is chosen.

        Args:
            paragraph (str): Source paragraph to choose candidate from.

        Returns:
            str | None: Either chosen word or `None` if there are no good candidates.
        """

        paragraph = self.remove_stopwords(paragraph)

        words = paragraph.split(' ')
        words = [self.santize(word) for word in words]
        tagged_words = [
            (santized_word, self.find_part_of_speech(santized_word))
            for santized_word in words
            if santized_word
        ]

        if not words:
            return None

        unknown_words_present = any(
            part_of_speech == 'n/a' for _, part_of_speech in tagged_words
        )
        if unknown_words_present:
            return random.choice(words)

        return random.choice(
            [
                word
                for word, part_of_speech in tagged_words
                if part_of_speech == 'noun'
            ]
        )
