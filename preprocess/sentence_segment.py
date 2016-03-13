
import preprocess.orchid_corpus as orch
import preprocess.viterbi as vtb
import preprocess.word_processing as wp
import preprocess.sentence as sentence

class sentence_segment:

	def __init__(self, corpus=orch.orchid_corpus(), custom_dict=dict()):
		self.corpus = corpus
		self.wp = wp.word_processing()

		self.custom_dict = custom_dict
		if custom_dict != None:
			word_list = set()
			with open("preprocess/tools/lexitron_original.txt") as f:
				for line in f:
					word_list.add(line.strip())
			for word in custom_dict:
				word_list.add(word)
			self.dict_name = "custom_dict_word.txt"
			with open("preprocess/tools/custom_dict_word.txt", "w") as f:
				for word in word_list:
					f.write(word + "\n")
		else:
			self.dict_name = "lexitron_original.txt"


	def clean_unknown_word(self, sentence):
		new_word_list = list()
		to_be_tagged = list()
		replace_idx = list()
		last_idx = -1

		for word in sentence:
			if word in self.custom_dict and self.custom_dict[word]["pos"] != None:
				new_word_list.append(word)
				to_be_tagged.append("_" + self.custom_dict[word]["pos"])
			elif not self.corpus.exists(word):
				subwords = self.wp.word_segment(word, dict="orchid_words.txt")
				valid_first = True
				valid_all = True

				for i in range(len(subwords)):
					if not self.corpus.exists(subwords[i]): 
						if i == 0:
							valid_first = False
						valid_all = False
						break

				if valid_all: # don't split this word if it exists in custom dict
					new_word_list.extend(subwords)
					to_be_tagged.extend(subwords)
				elif valid_first:
					new_word_list.append(word)
					to_be_tagged.append(subwords[0])
				else:
					new_word_list.append(word)
					to_be_tagged.append("_NCMN")

			else:
				new_word_list.append(word)
				to_be_tagged.append(word)

			replace_idx.append( (last_idx + 1, len(to_be_tagged) - 1 ) )
			last_idx = len(to_be_tagged) - 1

		return to_be_tagged, new_word_list, replace_idx

	def invert_unknown_word(self, broken_words, pos, reverse_idx):
		new_pos = []
		noun_tag = ["NPRP", "NCNM", "NONM", "NLBL", "NCMN", "NTTL"]
		count = 0

		for idx in reverse_idx:
			
			start, end = idx[0], idx[1]
			original_word = "".join(broken_words[start:(end+1)])
			if original_word in self.custom_dict and self.custom_dict[original_word]["pos"] != None:
				new_pos.append(self.custom_dict[original_word]["pos"])
			elif start != end:
				# print(original_word)
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

	def merge_sentence(self, sentences, sen_with_pos):
		new_sentences = [sentences[0]]
		new_sen_with_pos = [sen_with_pos[0]]

		for i in range(1, len(sentences)):
			first_pos = sen_with_pos[i][0][1]
			last_word_len = len(new_sen_with_pos[-1])

			merge = False
			start_sentence, cut_idx = sentences[i], 0
			if first_pos == "JCRG" or first_pos == "JCMP":
				merge = True
			elif first_pos == "JSBR":
				if len(sen_with_pos[i]) + last_word_len < 50 or len(sen_with_pos[i]) < 10:
					merge = True
				elif len(sen_with_pos[i]) > 2:
					# remove conjunction (with space, if any)
					cut_idx = 1 if sen_with_pos[i][1][1] != "NSBS" else 2
			if merge:
				new_sentences[-1] += " " + sentences[i]
				new_sen_with_pos[-1].extend([(" ", "NSBS")])
				new_sen_with_pos[-1].extend(sen_with_pos[i])
			else:
				if cut_idx > 0:
					start_sentence = "".join([word for (word,pos) in sen_with_pos[i][cut_idx:]])
				new_sentences.append(start_sentence)
				new_sen_with_pos.append(sen_with_pos[i][cut_idx:])
				
		return new_sentences, new_sen_with_pos

	def sentence_segment(self, paragraph, tri_gram=False):
		
		# preprocess
		words = self.wp.word_segment(paragraph, dict=self.dict_name)
		tmp_paragraph = self.wp.clean_special_characters(words)
		to_be_tagged, new_paragraph, replace_idx = self.clean_unknown_word(tmp_paragraph)

		# call viterbi function to get most possible pos sequence
		initp, trans, emiss = self.corpus.get_statistics_model(tri_gram)

		if tri_gram:
			path = vtb.viterbi_trigram(to_be_tagged, self.corpus.pos_list_sentence, initp, trans, emiss)
		else:
			path = vtb.viterbi(to_be_tagged, self.corpus.pos_list_sentence, initp, trans, emiss)
			# for i in range(len(path)):
			# 	print(to_be_tagged[i] + "\t\t" + path[i])

		# postprocess
		pos = self.invert_unknown_word(new_paragraph, path, replace_idx)
		sentences, sen_with_pos = self.cut_sentence(words, pos)
		merge_sen, merge_sen_with_pos = self.merge_sentence(sentences, sen_with_pos)

		# return sentences, sen_with_pos
		# return merge_sen, merge_sen_with_pos
		# return [sentence.sentence(sentences[i], sen_with_pos[i]) for i in range(len(sentences))]
		return [sentence.sentence(merge_sen[i], merge_sen_with_pos[i]) for i in range(len(merge_sen))]

	def get_stats(self):
		return self.initp, self.trans_bi, self.trans_tri, self.emiss



