
import viterbi as vtb
import word_processing


class sentence_segment:

	def __init__(self, corpus=None):
		self.corpus = corpus
		self.wp = word_processing.word_processing()

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
		words = self.wp.word_segment(paragraph)
		tmp_paragraph = self.wp.clean_special_characters(words)
		to_be_tagged, new_paragraph, replace_idx = self.clean_unknown_word(tmp_paragraph)

		# call viterbi function to get most possible pos sequence
		initp, trans, emiss = self.corpus.get_statistics_model(tri_gram)

		if tri_gram:
			path = vtb.viterbi_trigram(to_be_tagged, self.corpus.pos_list_sentence, initp, trans, emiss)
		else:
			path = vtb.viterbi(to_be_tagged, self.corpus.pos_list_sentence, initp, trans, emiss)

		# postprocess
		pos = self.invert_unknown_word(path, replace_idx)
		sentences, sen_with_pos = self.cut_sentence(words, pos)

		return sentences, sen_with_pos

	def get_stats(self):
		return self.initp, self.trans_bi, self.trans_tri, self.emiss



