
import choices.wordnet.wn_thai as wnth

wn = wnth.wordnet_thai()

class word_item:
	def __init__(self, word, eng_word=None, index=None, hypernym_index=None):
		self.word = word
		if eng_word == None:
			self.eng_word, self.index = wn.get_general_info(word)
			self.hypernym_index = hypernym_index = None
		else:
			self.eng_word = eng_word
			self.index = index
			self.hypernym_index = hypernym_index

	def __str__(self):
		return self.word