import unittest
import random
from pdb import set_trace as bp

from .context import prattler
from prattler.ngrammer import NGrammer

class TestNGrammer(unittest.TestCase):

    def test_training(self):
    	ngrammer = NGrammer(5)
    	ngrammer.train([
    		["one", "two", "three", "four", "five", "."], 
    		["one", "thousand", "."],
    		["one", "two", "one", "two", "."]
    	])

        self.assertEqual(
            ngrammer.models[2]['forward'][('one',)],  
            {'thousand': 1, 'two': 3}
        )

        self.assertEqual(
            ngrammer.models[2]['forward'][('.',)],
            {None: 3}
        )

    	self.assertEqual(
    		ngrammer.models[3]['forward'][('one', 'two')],  
    		{'.': 1, 'one': 1, 'three': 1}
    	)

        self.assertEqual(
            ngrammer.models[2]['backward'][('one',)],  
            {'two': 1, None: 3}
        )

        self.assertEqual(
            ngrammer.models[2]['backward'][(None,)],  
            {'.': 3}
        )

        self.assertEqual(
            ngrammer.models[3]['backward'][('.', None)],
            {'five': 1, 'thousand': 1, 'two': 1}
        )

    def test_sentence_boundaries(self):
    	ngrammer = NGrammer(2)
    	ngrammer.train([
    		["First", "sentence", "."],
    		["Second", "sentence", "."]
    	])

    	self.assertEqual(
    		ngrammer.models[2]['forward'][(None,)],
    		{'First': 1, 'Second': 1}
    	)

    	self.assertEqual(
    		ngrammer.models[2]['forward'][('.',)],
    		{None: 2}
    	)

    def test_weighted_choice(self):
    	ngrammer = NGrammer(2)
    	choices = [("first", 50), ("second", 100)]
    	results = {"first": 0, "second": 0}

    	random.seed("c40c5fce4d352ca6daf1aec9ee3afa67")

    	for i in xrange(100):
    		choice = ngrammer.weighted_choice(choices)
    		results[choice] += 1

    	self.assertEqual(results["first"], 34)
    	self.assertEqual(results["second"], 66)

    def test_format_sentence(self):
        ngrammer = NGrammer()
        self.assertEqual(
            ngrammer.format_sentence([None, 'This', ':', 'is', ',', 'a', 'formated', 'sentence', '.', None]),
            'This: is, a formated sentence.'
        )

        self.assertEqual(
            ngrammer.format_sentence(['Do', "n't", 'worry', ',', 'I', "'m", 'fine', '!']),
            "Don't worry, I'm fine!"
        )

    def test_sentence(self):
        ngrammer = NGrammer(2)
        ngrammer.train([
            ["one", "two", "three", "four", "five", "."], 
            ["one", "thousand", "."],
            ["one", "two", "one", "two", "."]
        ])

        sentence = ngrammer.sentence()
        self.assertTrue(len(sentence) > 0)

    def test_sentence_starting_with(self):
        ngrammer = NGrammer(2)
        ngrammer.train([
            ["one", "two", "three", "four", "five", "."], 
            ["one", "thousand", "."],
            ["one", "two", "one", "two", "."],
            ["hello", ",", "world", "!"],
            ["another", "sentence", "?"]
        ])

        sentence = ngrammer.sentence_starting_with("hello")
        self.assertTrue(sentence.startswith("hello"))
        self.assertEqual(sentence, "hello, world!")

    def test_sentence_ending_with(self):
        ngrammer = NGrammer(2)
        ngrammer.train([
            ["one", "two", "three", "four", "five", "."], 
            ["one", "thousand", "."],
            ["one", "two", "one", "two", "."],
            ["hello", ",", "world", "!"],
            ["another", "sentence", "?"]
        ])

        sentence = ngrammer.sentence_ending_with("?")
        self.assertEqual(sentence, "another sentence?")

    def test_sentence_containing(self):
        ngrammer = NGrammer(2)
        ngrammer.train([
            ["one", "two", "three", "four", "five", "."], 
            ["one", "thousand", "."],
            ["one", "two", "one", "two", "."],
            ["hello", ",", "world", "!"],
            ["another", "sentence", "?"],
            ["and", "yet", "1", "more"]
        ])

        sentence = ngrammer.sentence_containing("1")
        self.assertEqual(sentence, "and yet 1 more")


