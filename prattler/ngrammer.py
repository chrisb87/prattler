import random
import copy
from pdb import set_trace as bp

from nltk.tokenize import word_tokenize

class NGrammer(object):
	def __init__(self, n=2):
		self.n = n
		self.models = {}

		for ngram_size in xrange(2, n + 1):
			self.models[ngram_size] = {
				'forward' : {},
				'backward' : {}
			}

	def train(self, sentences):
		sliding_window = [None]

		for sentence in sentences:
			for token in (sentence + [None]):
				sliding_window.append(token)

				if len(sliding_window) > self.n:
					sliding_window.pop(0)

				for ngram_size in xrange(2, len(sliding_window) + 1):
					ngram = sliding_window[0 - ngram_size:]

					ngram_keys = {
						'forward' : tuple(ngram[:-1]),
						'backward' : tuple(ngram[1:])
					}

					ngram_values = {
						'forward' : ngram[-1],
						'backward' : ngram[0]
					}

					for direction in ['forward', 'backward']:
						model = self.models[ngram_size][direction]
						ngram_key = ngram_keys[direction]
						ngram_value = ngram_values[direction]

						if ngram_key not in model:
							model[ngram_key] = {}

						if ngram_value not in model[ngram_key]:
							model[ngram_key][ngram_value] = 1
						else:
							model[ngram_key][ngram_value] += 1

	def weighted_choice(self, choices):
		total_weight = sum(weight for choice, weight in choices)
		target = random.uniform(0, total_weight)
		upto = 0

		for choice, weight in choices:
			upto += weight

			if upto >= target:
				return choice

	def next_word(self, tokens, max_ngram_size=None, direction="forward"):
		current_ngram_size = max_ngram_size

		if current_ngram_size is None:
			current_ngram_size = self.n

		while current_ngram_size >= 2:
			model = self.models[current_ngram_size][direction]

			if direction == 'forward':
				ngram_key = tuple(tokens[1 - current_ngram_size:])
			elif direction == 'backward':
				ngram_key = tuple(tokens[:current_ngram_size - 1])
			else:
				raise "bad direction"

			try:
				next_word = self.weighted_choice(model[ngram_key].items())
				return next_word
			except KeyError:
				current_ngram_size -= 1

		raise "could not find word"

	def prev_word(self, tokens, max_ngram_size=None):
		return self.next_word(tokens, max_ngram_size, direction="backward")

	def sentence_from_tokens(self, tokens):
		while (len(tokens) <= 1) or (tokens[-1] is not None):
			tokens.append(self.next_word(tokens))

		while tokens[0] is not None:
			tokens.insert(0, self.prev_word(tokens))

		return self.format_sentence(tokens)

	def sentence(self):
		return self.sentence_from_tokens([None])

	def sentence_starting_with(self, words):
		return self.sentence_from_tokens([None] + word_tokenize(words))

	def sentence_ending_with(self, words):
		return self.sentence_from_tokens(word_tokenize(words) + [None])

	def sentence_containing(self, words):
		return self.sentence_from_tokens(word_tokenize(words))
	
	def format_sentence(self, tokenized_words):
		sentence = []

		for i in xrange(len(tokenized_words)):
			word = tokenized_words[i]

			if i == 0:
				prev_word = None
			else:
				prev_word = tokenized_words[i - 1]

			if word in [None]:
				continue

			if prev_word is None:
				pass
			elif word in ['.', '!', '?', ',', ':', ';', "n't"]:
				pass
			elif word.startswith("'"):
				pass
			else:
				word = ' ' + word

			sentence.append(word)

		return "".join(sentence)



if __name__ == '__main__':

	import parsers
	parser = parsers.MobyParser()

	ngrammer = NGrammer(4)
	ngrammer.train(parser.tokenized_sentences())

	for i in xrange(10):
		print "-----"
		print ngrammer.sentence()







