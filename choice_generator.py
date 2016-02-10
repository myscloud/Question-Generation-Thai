
import wordnet.wordnetthai as wnth

class choice_generator:

	def __init__(self):
		self.wn = wnth.wordnetthai()

	def choice_generate(self, answer):
		hyponyms = self.wn.get_siblings(answer)
		return hyponyms

if __name__ == "__main__":
	cg = choice_generator()
	print(cg.choice_generate("ดาวเสาร์"))