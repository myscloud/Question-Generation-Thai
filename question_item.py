
from statistics import mean
import preprocess.orchid_corpus as orchid_corpus

import preprocess.sentence as _sentence
import choices.wordnet.wn_tree as wn_tree
import choices.word_item as _word_item

import ast

wn = wn_tree.wordnet_tree()
orchid = orchid_corpus.orchid_corpus()

class question_item:
	def __init__(self, *args, **kwargs):
		if len(args) == 5:
			(sentence, sentence_no, question, answer, answer_index) = args
			self.sentence = sentence
			self.sentence_no = sentence_no
			self.question = question
			self.answer = answer
			self.answer_index = answer_index
			self.choices = None
			self.asked_choices = None
		elif "from_str" in kwargs:
			attributes = ast.literal_eval(kwargs["from_str"])
			for key in attributes:
				if key == "sentence":
					self.sentence = _sentence.sentence(from_str=attributes["sentence"])
				elif key == "choices":
					self.choices = [_word_item.word_item(from_str=choice_str) for choice_str in attributes["choices"]]
				elif key == "answer":
					self.answer = _word_item.word_item(from_str=attributes["answer"])
				else:
					setattr(self, key, attributes[key])

		self.evals = []

	def add_choices(self, new_choices):
		self.choices = new_choices

	def add_evaluation(self, eval):
		self.evals.append(int(eval))

	def get_average_eval(self):
		if len(self.evals) > 0:
			return mean(self.evals)
		else:
			return 0.0

	def get_orchid_ratio(self):
		known_word = sum([orchid.exists(word[0]) for word in self.sentence.pos])
		known_ratio = (known_word / len(self.sentence.pos)) * 100
		return known_ratio

	def get_prev_pos(self):
		if self.answer_index == 0:
			return "<first>"
		else:
			pos = self.sentence.pos[self.answer_index-1][1]
			return pos

	def get_next_pos(self):
		if self.answer_index == len(self.sentence.pos) - 1:
			return "<last>"
		else:
			pos = self.sentence.pos[self.answer_index+1][1]
			return pos

	def get_prev_next_pos(self):
		pos = self.get_prev_pos() + " " + self.get_next_pos()
		return pos

	def get_first_pos(self):
		return self.sentence.pos[0][1]

	def get_wordnet_height(self):
		return wn.get_word_height(self.answer.eng_word)

	def get_answer_freq_in_sentence(self):
		word_list = [word for word, pos in self.sentence.pos]
		return word_list.count(str(self.answer)) / self.get_word_count()

	def get_answer_freq_in_article(self, article):
		article_len = 0
		for word in article:
			if word != " ":
				article_len += 1

		return (article.count(str(self.answer)) / article_len) * 100

	def get_word_count(self):
		word_count = 0
		for (word, pos) in self.sentence.pos:
			if pos != "NSBS":
				word_count += 1
		return word_count

	def get_answer_familiarity(self):
		processed_eng_word = wn.process_eng_word(str(self.answer.eng_word))
		freq = wn.get_word_frequency(word=processed_eng_word)
		return freq if freq != None else -1

	def get_known_answer(self):
		# todo: if answer is in custom dict, return 2.0
		if orchid.exists(str(self.answer)):
			return 1
		else:
			return 0

	def get_all_features(self, article):
		features = dict()
		features["orchid"] = self.get_orchid_ratio()
		# features["first-pos"] = self.get_first_pos()
		features["sentence-len"] = self.get_word_count()
		# features["prev-pos"] = self.get_prev_pos()
		# features["next-pos"] = self.get_next_pos()
		features["wn-height"] = self.get_wordnet_height()
		features["known-ans"] = self.get_known_answer()
		# features["freq-article"] = self.get_answer_freq_in_article(article)
		features["ans-familiar"] = self.get_answer_familiarity()

		return features

	def is_verb(self, index):
		(word, pos) = self.sentence.pos[index]
		if pos == "VSTA" or pos == "VACT":
			return True
		return False

	def get_nearest_verb(self):
		center = self.answer_index
		boundary = max((center + 1), (len(self.sentence.pos) - center))

		for count in range(1, boundary):
			if center - count >= 0:
				if self.is_verb(center - count):
					return self.sentence.pos[center - count][0], (center - count)
			if center + count < len(self.sentence.pos):
				if self.is_verb(center + count):
					return self.sentence.pos[center + count][0], (center + count)

		return None, None


	def __str__(self):
		print(self.question)
		txt = self.question + "\n"
		txt = "( " + self.answer.word + ")\n"
		for choice in self.choices:
			txt += choice.word + "\t"
		txt += "\n"
		return txt

	def __repr__(self):
		represent = dict()
		represent["sentence"] = repr(self.sentence)
		represent["sentence_no"] = self.sentence_no
		represent["question"] = self.question
		represent["answer"] = repr(self.answer)
		represent["answer_index"] = self.answer_index
		represent["choices"] = [repr(a_choice) for a_choice in self.choices]
		return repr(represent)

		