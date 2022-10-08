from heapq import nlargest
from string import punctuation

import spacy
from spacy.lang.en.stop_words import STOP_WORDS


def get_summarization(text: str, percentage: float) -> str:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        word_lower = word.text.lower()
        if word_lower not in list(STOP_WORDS) and word_lower not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}

    for sent in sentence_tokens:
        for word in sent:
            word_lower = word.text.lower()
            if word_lower not in word_frequencies.keys():
                continue
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_frequencies[word_lower]
            else:
                sentence_scores[sent] += word_frequencies[word_lower]

    select_length = int(len(sentence_tokens) * percentage)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = [word.text for word in summary]
    summary = "".join(summary)

    return summary
