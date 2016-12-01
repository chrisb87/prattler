import unittest
import os
from pdb import set_trace as bp

from .context import prattler
from prattler import parsers

class TestParser(unittest.TestCase):

    def test_string_parser_returns_sentences(self):
        source_text = """
            This is the source text.

            It contains three sentences.

            One sentence is on
            multiple lines.

        """

        p = prattler.parsers.StringParser(source_text)
        sentences = [s for s in p.sentences()]

        self.assertEqual(len(sentences), 3)
        self.assertEqual(sentences[0], "This is the source text.")
        self.assertEqual(sentences[1], "It contains three sentences.")
        self.assertEqual(sentences[-1], "One sentence is on multiple lines.")

    def test_guttenberg_parser_returns_sentences(self):
        p = prattler.parsers.GutenbergParser('data/guttenberg_simple.txt', 10, 16)
        sentences = [s for s in p.sentences()]

        self.assertEqual(len(sentences), 7)
        self.assertEqual(sentences[0], "This is a simple text.")
        self.assertEqual(sentences[6], "A simple text is nice for debugging.")
        self.assertEqual(sentences[-1], 'A simple text is nice for debugging.')

    def test_tokenized_sentences(self):
        p = prattler.parsers.GutenbergParser('data/guttenberg_simple.txt', 10, 16)
        tokenized_sentences = [s for s in p.tokenized_sentences()]

        self.assertEqual(len(tokenized_sentences), 7)
        self.assertEqual(tokenized_sentences[0], ['This', 'is', 'a', 'simple', 'text', '.'])

    def test_guttenberg_parser_content_lines(self):
        p = prattler.parsers.GutenbergParser('data/guttenberg_simple.txt', 10, 16)
        content_lines = [l for l in p.content_lines()]

        self.assertEqual(len(content_lines), 7)
        self.assertEqual(content_lines[0], "This is a simple text. It contains simple sentences. This is not")
        self.assertEqual(content_lines[1], "a complicated text. It does not")
        self.assertEqual(content_lines[-1], "words. A simple text is nice for debugging.")

    def test_alice_parser(self):
        alice_parser = prattler.parsers.AliceParser()
        sentences = list(alice_parser.sentences())

        self.assertEqual(sentences[0], "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'")
        self.assertEqual(sentences[-1], 'Lastly, she pictured to herself how this same little sister of hers would, in the after-time, be herself a grown woman; and how she would keep, through all her riper years, the simple and loving heart of her childhood: and how she would gather about her other little children, and make THEIR eyes bright and eager with many a strange tale, perhaps even with the dream of Wonderland of long ago: and how she would feel with all their simple sorrows, and find a pleasure in all their simple joys, remembering her own child-life, and the happy summer days.')

    def test_moby_parser(self):
        moby_parser = prattler.parsers.MobyParser()
        sentences = list(moby_parser.sentences())

        self.assertEqual(sentences[0], 'The pale Usher--threadbare in coat, heart, body, and brain; I see him now.')
        self.assertEqual(sentences[-1], 'It was the devious-cruising Rachel, that in her retracing search after her missing children, only found another orphan.')
