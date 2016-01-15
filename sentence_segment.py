
import viterbi as vtb
import word_processing


class sentence_segment:

	def __init__(self, corpus=None):
		self.corpus = corpus
		self.wp = word_processing.word_processing()

		self.initp = dict()
		self.trans = dict()
		self.emiss = dict()

		if self.corpus != None:
			self.calc_statistics()

	def calc_statistics(self):
		cp = self.corpus.get_corpus_sentence()
		word_list = self.corpus.word_list
		pos_list = self.corpus.pos_list
		pos_list.add("SBS")
		pos_list.add("NSBS")

		# initial probability
		for pos in pos_list:
			self.initp[pos] = 0

		for paragraph in cp:
			self.initp[paragraph[0][1]] += 1

		n = len(cp)
		for pos in self.initp:
			self.initp[pos] /= n

		# transition probability
		for pos1 in pos_list:
			self.trans[pos1] = dict()
			self.trans[pos1]["count"] = 0
			for pos2 in pos_list:
				self.trans[pos1][pos2] = 0

		for paragraph in cp:
			n = len(paragraph)
			for i in range(n - 1):
				curr_pos = paragraph[i][1]
				next_pos = paragraph[i+1][1]
				self.trans[curr_pos][next_pos] += 1
				self.trans[curr_pos]["count"] += 1

		for pos1 in self.trans:
			for pos2 in self.trans[pos1]:
				if pos2 != "count":
					self.trans[pos1][pos2] /= self.trans[pos1]["count"]

        # emission probability
		pos_count = dict()
		for pos in pos_list:
			pos_count[pos] = 0

		for word in word_list:
			self.emiss[word] = dict()
			for pos in pos_list:
				self.emiss[word][pos] = 0

		for paragraph in cp:
			for word in paragraph:
				pos_count[word[1]] += 1
				self.emiss[word[0]][word[1]] += 1

		for word in word_list:
			for pos in pos_list:
				self.emiss[word][pos] /= pos_count[pos]


	def clean_special_characters(self, sentence):
		special = {
			' ': '<space>',
			'-': '<minus>',
			'(': '<left_parenthesis>',
			')': '<right_parenthesis>',
			'*': '<asterisk>',
			'.': '<full_stop>',
			'"': '<quotation>',
			'/': '<slash>',
			':': '<colon>',
			'=': '<equal>',
			',': '<comma>',
			';': '<semi_colon>',
			'<': '<less_than>',
			'>': '<greater_than>',
			'&': '<ampersand>',
			'{': '<left_curly_bracket>',
			'}': '<right_curly_bracket>',
			"'": '<apostrophe>',
			'+': '<plus>',
			'?': '<question_mark>',
			'!': '<exclamation>',
			'$': '<dollar>',
			'%': '<percent>'
		}

		word_count = len(sentence)
		for i in range(word_count):
			if sentence[i] in special:
				sentence[i] = special[sentence[i]]

		return sentence

	def clean_unknown_word(self, sentence):
		new_word_list = list()
		to_be_tagged = list()

		for word in sentence:
			if not self.corpus.exists(word):
				subwords = self.wp.word_segment(word, dict="orchid_words.txt")
				valid_first = True
				valid_all = True

				for i in range(len(subwords)):
					if not self.corpus.exists(subwords[i]): 
						if i == 0:
							valid_first = False
						valid_all = False
						break

				if valid_all:
					new_word_list.extend(subwords)
					to_be_tagged.extend(subwords)
				elif valid_first:
					new_word_list.append(word)
					to_be_tagged.append(subwords[0])
				else:
					new_word_list.append(word)
					to_be_tagged.append("tmp_noun")

			else:
				new_word_list.append(word)
				to_be_tagged.append(word)

		return to_be_tagged, new_word_list

	def sentence_segment(self, paragraph):
		tmp_paragraph = self.clean_special_characters(paragraph)
		to_be_tagged, new_paragraph= self.clean_unknown_word(tmp_paragraph)

		path = vtb.viterbi(to_be_tagged, self.corpus.pos_list, self.initp, self.trans, self.emiss)

		return new_paragraph, path


