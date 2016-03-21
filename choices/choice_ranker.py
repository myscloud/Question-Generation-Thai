
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import ranking.linear_regression as regr

from nltk.metrics.distance import edit_distance
from nltk.corpus import brown

class choice_ranker():

	def __init__(self, model=None, training_set=None, wordnet=None):
		self.wn = wordnet.wn
		self.trans = wordnet.trans
		self.vectorizer = None
		self.concord = self.prepare_cooccur()
		if model !=  None:
			pass
		elif training_set != None:
			self.model = self.train_choices(training_set)

	def get_data_feature(self, question_item, choice_item):
		answer = question_item.answer.eng_word.lower()
		choice = choice_item.eng_word.lower()

		features = dict()
		# features["edit-dist"] = edit_distance(question_item.answer.word, choice_item.word)
		# features["length"] = len(choice_item.word)
		# features["edit-dist-eng"] = edit_distance(answer, choice)
		features["familiar"] = self.wn.get_word_frequency(index=choice_item.index)
		# features["height"] = self.wn.get_word_height(choice, index=choice_item.index)
		# features["siblings-count"] = self.wn.get_siblings_count(choice_item.index, choice_item.hypernym_index)
		features["noun-cooccur"] = self.get_cooccur(answer, choice)
		features["verb-cooccur"] = self.get_verb_cooccur(question_item, choice)

		return features

	def preprocess_data(self, question_set, has_score=False):
		choice_features = []
		choice_scores = []

		for question in question_set:
			if question.get_average_eval() >= 2.0:
				for choice in question.choices:
					if choice.word != question.answer.word:
						features = self.get_data_feature(question, choice)
						choice_features.append(features)
						if has_score:
							choice_scores.append(choice.get_average_eval())

		return self.vectorize(choice_features), np.array(choice_scores)

		# vectorize
	def vectorize(self, choice_features):
		if self.vectorizer == None:
			self.vectorizer = DictVectorizer(sparse=False)
			choice_vector = self.vectorizer.fit_transform(choice_features)
		else:
			choice_vector = self.vectorizer.transform(choice_features)

		return choice_vector

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

	def get_last_word(self, word):
		words = word.split(" ")
		return words[-1]

	def get_verb_cooccur(self, question, word):
		near_verb, _ = question.get_nearest_verb()
		if near_verb != None:
			(_, verb_eng) = (self.trans.translate([near_verb], "th", "en"))[0]
			return self.get_cooccur(verb_eng, word)
		return None

	def get_cooccur(self, first, second):
		# word1 = self.get_last_word(first)
		# word2 = self.get_last_word(second)
		word1, word2 = first, second
		if word1 in self.concord and word2 in self.concord[word1]:
			return self.concord[word1][word2]
		else:
			return 0

	def train_choices(self, question_set):
		choice_vector, choice_scores = self.preprocess_data(question_set, has_score=True)
		model = regr.train_model(choice_vector, choice_scores)
		return model

	def rank_choices(self, question, choices_list):
		choice_with_score = []
		for choice in choices_list:
			if choice.word != question.answer.word:
				choice_features = self.get_data_feature(question, choice)
				choice_vector = self.vectorize(choice_features)
				predicted_scores = regr.predict(self.model, choice_vector)
				choice_with_score.append((choice, predicted_scores[0]))

		ranked_choices = sorted(choice_with_score, key=lambda x: x[1], reverse=True)
		return [choice for choice, score in ranked_choices], ranked_choices

if __name__ == "__main__":
	chrank = choice_ranker()
	while True:
		word1 = input("Enter first word: ")
		if word1 == "quit":
			break
		word2 = input("Enter second word: ")
		print(chrank.get_cooccur(word1, word2))
