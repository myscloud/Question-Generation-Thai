
import wordnet.translator as translator
import wordnet.wordnet_tree as wordnet_tree

class wordnetthai:

	def __init__(self):
		self.wn = wordnet_tree.wordnet_tree()
		self.trans = translator.translator()

	def process_eng_word(self, word):
		words = word.split(", ")
		return words[0].lower().replace("_", " ")

	def get_hypernym(self, thai_word, level=1):
		trans_results = self.trans.translate([thai_word], "th", "en")
		(_, eng_word) = trans_results[0]
		eng_hypernym, _ = self.wn.get_hypernym(eng_word, level)
		if eng_hypernym != None:
			eng_hypernym = self.process_eng_word(eng_hypernym)
			trans_results = self.trans.translate([eng_hypernym], "en", "th")
			return trans_results[0][1]
		else:
			return None

	def get_all_hypernym(self, thai_word, reverse=False):
		trans_results = self.trans.translate([thai_word], "th", "en")
		(_, eng_word) = trans_results[0]
		eng_hypernyms = self.wn.get_all_hypernym(eng_word, reverse)
		
		if eng_hypernyms != None:
			processed_eng_hypernyms = [self.process_eng_word(word) for word in eng_hypernyms]
			trans_results = self.trans.translate(processed_eng_hypernyms, "en", "th")
			return [tp[1] for tp in trans_results]
		else:
			return None

	def get_siblings(self, thai_word, level=1):
		trans_results = self.trans.translate([thai_word], "th", "en")
		(_, eng_word) = trans_results[0]
		eng_siblings = self.wn.get_siblings(eng_word, level)

		processed_eng_siblings = [self.process_eng_word(word) for word in eng_siblings]
		trans_results = self.trans.translate(processed_eng_siblings, "en", "th")
		return [tp[1] for tp in trans_results]


if __name__ == "__main__":
	wnth = wordnetthai()
	print(wnth.get_siblings("ดาว"))
