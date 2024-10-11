"""Module with AnswerChooser, which finds a best candidate for an answer in a paragraph."""

from copy import copy
import random
import nltk  # type: ignore[import-untyped]
from nltk.corpus import wordnet  # type: ignore[import-untyped]
from tqdm import tqdm  # type: ignore[import-untyped]


class AnswerChooser:
    """
    Class choosing an answer from a paragraph for Question Generation module.
    """

    def __init__(self) -> None:
        self._cache: dict[str, str | None] = {}
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

    def sanitize(self, word: str) -> str:
        """
        Convert to lowercase and remove any punctuation mark.

        Args:
            word (str): Word to sanitize.

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
        word = self.sanitize(word=word)
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

    def choose_answer(
        self, paragraph: str, use_cached: bool = True
    ) -> str | None:
        """
        Choose a good candidate for an answer from a paragraph.

        Choose a good candidate from `paragraph` based on the following algorithm:
        1. Remove stop words.
        2. If any word with undetermined part of speech (PoS) is present,
            a random word with undetermined PoS is chosen.
        3. Otherwise, a random noun is chosen.
        This operation may be costly so its results are cached. Custom caching
        mechanism was implemented as `functools` `@cache` and `@lru_cache` should
        not be called on methods, only on functions.

        Args:
            paragraph (str): Source paragraph to choose candidate from.
            use_cached (bool): Use a cached results if available.

        Returns:
            str | None: Either chosen word or `None` if there are no good candidates.
        """
        if paragraph in self._cache and use_cached:
            return self._cache[paragraph]

        entered_paragraph = copy(paragraph)
        paragraph = self.remove_stopwords(paragraph)

        words = paragraph.split(' ')
        words = [self.sanitize(word) for word in words]
        tagged_words = [
            (sanitized_word, self.find_part_of_speech(sanitized_word))
            for sanitized_word in words
            if sanitized_word
        ]

        if not words:
            return None

        unknown_words_present = any(
            part_of_speech == 'n/a' for _, part_of_speech in tagged_words
        )
        if unknown_words_present:
            return random.choice(words)

        output = random.choice(
            [
                word
                for word, part_of_speech in tagged_words
                if part_of_speech == 'noun'
            ]
        )

        self._cache[entered_paragraph] = output
        return output
