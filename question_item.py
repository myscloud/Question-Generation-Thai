
from statistics import mean
from preprocess.orchid_corpus import pos_map

import preprocess.sentence as _sentence
import choices.wordnet.wn_tree as wn_tree
import choices.word_item as _word_item

import ast

wn = wn_tree.wordnet_tree()

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

	def get_prev_pos(self):
		if self.answer_index == 0:
			return "<first>"
		else:
			pos = self.sentence.pos[self.answer_index-1][1]
			# return type of pos (e.g. NPRP -> noun)
			# for key in pos_map:
			# 	if pos in pos_map[key]:
			# 		return key
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
		return word_list.count(str(self.answer))

	def get_word_count(self):
		word_count = 0
		for (word, pos) in self.sentence.pos:
			if pos != "NSBS":
				word_count += 1
		return word_count

	def get_answer_frequency(self):
		processed_eng_word = wn.process_eng_word(str(self.answer.eng_word))
		freq = wn.get_word_frequency(word=processed_eng_word)
		return freq if freq != None else -1

	def __str__(self):
		txt = self.question + "\n"
		for choice in self.choices:
			txt += choice.word + "\t"
		txt += "\n" + str(self.sentence.pos)
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

		