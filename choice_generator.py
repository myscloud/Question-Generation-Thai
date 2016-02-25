
import wordnet.wordnetthai as wnth

class choice_generator:

	def __init__(self):
		self.wn = wnth.wordnetthai()

	# return True if word contains at least 1 thai character
	def is_thai_word(self, word):
		for char in word:
			if ord(char) in range(3585, 3676):
				return True
		return False

	def choice_generate(self, answer):
		if self.is_thai_word(answer):
			hyponyms = self.wn.get_siblings(answer)
			thai_hyponyms = []
			for word in hyponyms:
				if self.is_thai_word(word): thai_hyponyms.append(word)
			return thai_hyponyms
		else:
			return []

if __name__ == "__main__":
	cg = choice_generator()
	# print(cg.choice_generate("ความสัมพันธ์"))