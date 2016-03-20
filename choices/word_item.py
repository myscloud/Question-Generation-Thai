
from statistics import mean
import choices.wordnet.wn_thai as wnth
import ast
from nltk.corpus import brown

wn = wnth.wordnet_thai()

class word_item:
	def __init__(self, *args, **kwargs):
		if len(args) > 0:
			self.word = args[0]
			if len(args) == 1:
				self.eng_word, self.index = wn.get_general_info(self.word)
				self.hypernym_index = hypernym_index = None
			elif len(args) == 4:
				(eng_word, index, hypernym_index) = args[1:]
				self.eng_word = eng_word
				self.index = index
				self.hypernym_index = hypernym_index
		elif "from_str" in kwargs:
			attributes = ast.literal_eval(kwargs["from_str"])
			for key in attributes:
				setattr(self, key, attributes[key])
		self.evals = []
		# self.concord = self.prepare_cooccur()

	def add_evaluation(self, score):
		self.evals.append(score)

	def get_average_eval(self):
		if len(self.evals) > 0:
			return mean(self.evals)
		else:
			return None

	def __str__(self):
		return self.word

	def __repr__(self):
		represent = dict()
		attributes = vars(self)
		for key in attributes:
			if key != "evals":
				represent[key] = attributes[key]
		return repr(represent)

	def prepare_cooccur(self):
		concord = dict()
		for sentence in brown.tagged_sents(tagset="universal"):
			noun_set = set()
			verb_set = set()
			for word, pos in sentence:
				if pos == "NOUN":
					noun_set.add(word)
				elif pos == "VERB":
					verb_set.add(word)

			for noun in noun_set.union(verb_set):
				if noun not in concord:
					concord[noun] = dict()
				for word in (noun_set.union(verb_set)).difference({noun}):
					if word not in concord[noun]:
						concord[noun][word] = 0
					concord[noun][word] += 1
		
		return concord

	def get_cooccur(self, first, second):
		if first in self.concord and second in self.concord[first]:
			return self.concord[first][second]
		else:
			return None

