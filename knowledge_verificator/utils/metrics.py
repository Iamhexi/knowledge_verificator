"""The module with implementation of NLP metrics such as BLEU and other."""

from nltk.translate.bleu_score import sentence_bleu  # type: ignore[import-untyped]
from nltk.translate.meteor_score import single_meteor_score  # type: ignore[import-untyped]
from nltk.translate.nist_score import sentence_nist  # type: ignore[import-untyped]
from nltk.tokenize import word_tokenize  # type: ignore[import-untyped]
from rouge_score import rouge_scorer  # type: ignore[import-untyped]


def calculate_bleu_4(reference: str, hypothesis: str) -> float:
    """
    Calculate the BLEU-4 (Bilingual Evaluation Understudy) score.

    Args:
        reference (str): A reference sentence.
        hypothesis (str): An evaluated sentence.

    Returns:
        float: Value of the BLEU score.
    """
    reference = word_tokenize(reference)
    hypothesis = word_tokenize(hypothesis)
    return sentence_bleu(references=[reference], hypothesis=hypothesis)


def calculate_rouge_n(reference: str, hypothesis: str, n: int) -> float:
    """
    Calculate the ROUGE-N (Recall-Oriented Understudy for Gisting Evaluation) score.

    Args:
        reference (str): A reference sentence.
        hypothesis (str): An evaluated sentence.
        n (int): The size of the n-gram to evaluate.

    Returns:
        float: Value of the ROUGE-N score.
    """
    # ROUGE-N (N-gram) scoring
    scorer = rouge_scorer.RougeScorer([f'rouge{n}'], use_stemmer=True)
    return scorer.score(target=reference, prediction=hypothesis)[f'rouge{n}']


def calculate_rouge_lcs(reference: str, hypothesis: str) -> float:
    """
    Calculate the ROUGE-LCS (Longest Common Subsequence) score.

    Args:
        reference (str): A reference sentence.
        hypothesis (str): An evaluated sentence.

    Returns:
        float: Value of the ROUGE-LCS score.
    """
    # ROUGE-LCS (Longest Common Subsequence) scoring
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    return scorer.score(target=reference, prediction=hypothesis)['rougeL']


def calculate_nist(reference: str, hypothesis: str) -> float:
    """
    Calculate the NIST (National Institute of Standards and Technology) score.

    Args:
        reference (str): A reference sentence.
        hypothesis (str): An evaluated sentence.

    Returns:
        float: Value of the NIST score.
    """
    reference = word_tokenize(reference)
    hypothesis = word_tokenize(hypothesis)
    return sentence_nist(references=[reference], hypothesis=hypothesis)


def calculate_meteor(reference: str, hypothesis: str) -> float:
    """
    Calculate the METEOR (Metric for Evaluation of Translation with Explicit ORdering) score.

    Args:
        reference (str): A reference sentence.
        hypothesis (str): An evaluated sentence.

    Returns:
        float: Value of the METEOR score.
    """
    reference = word_tokenize(reference)
    hypothesis = word_tokenize(hypothesis)
    return single_meteor_score(reference=reference, hypothesis=hypothesis)
