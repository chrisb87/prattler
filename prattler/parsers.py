import re
import os

from pdb import set_trace as bp

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

EXTRA_WHITESPACE_PATTERN = re.compile(r"\s+", re.MULTILINE)


class StringParser(object):
    def __init__(self, source_text):
        self.source_text = source_text

    def sentences(self):
        for sentence in sent_tokenize(self.source_text):
            sentence = sentence.strip()
            sentence = EXTRA_WHITESPACE_PATTERN.sub(" ", sentence)
            yield sentence


class GutenbergParser(object):
    def __init__(self, source_path, content_start = 0, content_end = -1):
        self.source_path = source_path
        self.content_start = content_start
        self.content_end = content_end

    def lines(self):
        with open(self.source_path) as f:
            for line in f:
                yield line.strip()

    def content_lines(self):
        for i, line in enumerate(self.lines(), start=1):
            if i < self.content_start:
                continue

            if (self.content_end > 0) and (i > self.content_end):
                break

            if line.startswith("CHAPTER "):
                continue

            yield line

    def lines_to_sentences(self, lines):
        # takes a list of lines, returns a list of sentences

        paragraph = " ".join(lines)
        sentences = []

        for sentence in sent_tokenize(paragraph):
            sentence = sentence.strip()
            sentence = EXTRA_WHITESPACE_PATTERN.sub(" ", sentence)

            if sentence != "":
                sentences.append(sentence)

        return sentences

    def sentences(self):
        current_paragraph = []

        for line in self.content_lines():
            if line == "":
                # end the paragraph and return it as sentences
                for sentence in self.lines_to_sentences(current_paragraph):
                    yield sentence

                current_paragraph = []
            else:
                # continue the paragraph
                current_paragraph.append(line)

        for sentence in self.lines_to_sentences(current_paragraph):
            yield sentence

    def tokenized_sentences(self):
        for sentence in self.sentences():
            yield word_tokenize(sentence)


class AliceParser(GutenbergParser):
    def __init__(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/alices_adventures_in_wonderland.txt"))
        super(AliceParser, self).__init__(data_path, 43, 3368)

class MobyParser(GutenbergParser):
    def __init__(self):
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/moby_dick.txt"))
        super(MobyParser, self).__init__(data_path, 57, 21743)
