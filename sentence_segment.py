
import viterbi as vtb
import word_processing


class sentence_segment:

	def __init__(self, corpus=None):
		self.corpus = corpus
		self.wp = word_processing.word_processing()

		self.initp = dict()
		self.trans_bi = dict()
		self.trans_tri = dict()
		self.emiss = dict()

		if self.corpus != None:
			self.calc_statistics()

		self.special = {
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

		self.inv_special = dict()
		for spc_char in self.special:
			token = self.special[spc_char]
			self.inv_special[token] = spc_char

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
		# bigram
		for pos1 in pos_list:
			self.trans_bi[pos1] = dict()
			self.trans_bi[pos1]["count"] = 0
			for pos2 in pos_list:
				self.trans_bi[pos1][pos2] = 0

		for paragraph in cp:
			n = len(paragraph)
			for i in range(n - 1):
				curr_pos = paragraph[i][1]
				next_pos = paragraph[i+1][1]
				self.trans_bi[curr_pos][next_pos] += 1
				self.trans_bi[curr_pos]["count"] += 1

		for pos1 in self.trans_bi:
			for pos2 in self.trans_bi[pos1]:
				if pos2 != "count":
					self.trans_bi[pos1][pos2] /= self.trans_bi[pos1]["count"]

		# trigram
		for pos1 in pos_list:
			self.trans_tri[pos1] = dict()
			for pos2 in pos_list:
				self.trans_tri[pos1][pos2] = dict()
				self.trans_tri[pos1][pos2]["count"] = 0
				for pos3 in pos_list:
					self.trans_tri[pos1][pos2][pos3] = 0  # p(pos3|pos1,pos2)

		for paragraph in cp:
			n = len(paragraph)
			for i in range(n - 2):
				pos1 = paragraph[i][1]
				pos2 = paragraph[i+1][1]
				pos3 = paragraph[i+2][1]

				self.trans_tri[pos1][pos2][pos3] += 1
				self.trans_tri[pos1][pos2]["count"] += 1

		for pos1 in self.trans_tri:
			for pos2 in self.trans_tri[pos1]:
				for pos3 in self.trans_tri[pos1][pos2]:
					if pos3 != "count" and self.trans_tri[pos1][pos2]["count"] != 0:
						self.trans_tri[pos1][pos2][pos3] /= self.trans_tri[pos1][pos2]["count"]

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


	def clean_special_characters(self, st):
		sentence = [ word for word in st ]
		word_count = len(sentence)
		for i in range(word_count):
			if sentence[i] in self.special:
				sentence[i] = self.special[sentence[i]]

		return sentence

	def clean_unknown_word(self, sentence):
		new_word_list = list()
		to_be_tagged = list()
		replace_idx = list()
		last_idx = -1

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

			replace_idx.append( (last_idx + 1, len(to_be_tagged) - 1 ) )
			last_idx = len(to_be_tagged) - 1

		return to_be_tagged, new_word_list, replace_idx

	def invert_unknown_word(self, pos, reverse_idx):
		new_pos = []
		noun_tag = ["NPRP", "NCNM", "NONM", "NLBL", "NCMN", "NTTL"]
		count = 0

		for idx in reverse_idx:
			start, end = idx[0], idx[1]
			if start != end:
				noun_count = 0
				for j in range(start, end + 1):
					if pos[j] in noun_tag:
						noun_count += 1
				if noun_count > 0:
					new_pos.append("NPRP") # proper noun
				else:
					new_pos.append(pos[start]) # use same pos with the first word
			else:
				new_pos.append(pos[start])
			count += 1

		return new_pos

	def cut_sentence(self, paragraph, pos):
		sentences = []
		sen_with_pos = []

		tmp_sentence = ""
		tmp_list = []

		for i in range(len(paragraph)):
			if pos[i] == "SBS":
				sentences.append(tmp_sentence)
				sen_with_pos.append(tmp_list)
				tmp_sentence = ""
				tmp_list = []
			else:
				tmp_sentence += paragraph[i]
				tmp_list.append( (paragraph[i], pos[i]) )

		if len(tmp_list) > 0:
			sentences.append(tmp_sentence)
			sen_with_pos.append(tmp_list)

		return sentences, sen_with_pos

	def sentence_segment(self, paragraph, tri_gram=True):
		
		# preprocess
		tmp_paragraph = self.clean_special_characters(paragraph)
		to_be_tagged, new_paragraph, replace_idx = self.clean_unknown_word(tmp_paragraph)

		# call viterbi function to get most possible pos sequence
		if tri_gram:
			path = vtb.viterbi_trigram(to_be_tagged, self.corpus.pos_list, self.initp, self.trans_tri, self.emiss)
		else:
			path = vtb.viterbi(to_be_tagged, self.corpus.pos_list, self.initp, self.trans_bi, self.emiss)

		# postprocess
		pos = self.invert_unknown_word(path, replace_idx)
		sentences, sen_with_pos = self.cut_sentence(paragraph, pos)
		return sentences, sen_with_pos


