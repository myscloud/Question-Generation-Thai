
import choices.wordnet.wn_thai as wnth
import choices.word_item as word_item
import math
import random

class choice_generator:

	def __init__(self, wordnet, chrank):
		self.wn = wordnet
		self.choice_ranker = chrank

	# return True if word contains at least 1 thai character
	def is_thai_word(self, word):
		for char in word:
			if ord(char) in range(3585, 3664): # exclude thai number
				return True
		return False

	def generate_choices(self, question_item):
		answer = question_item.answer
		if self.is_thai_word(answer.word):
			siblings, eng_siblings, index, hypernyms = self.wn.get_siblings(answer.eng_word, answer.index)
			
			choices_set = set()
			all_choices = []
			for i in range(len(siblings)):
				for j in range(len(siblings[i])):
					new_item = word_item.word_item(siblings[i][j], eng_siblings[i][j], index[i][j], hypernyms[i])

					sibling_thai = siblings[i][j]
					if sibling_thai not in choices_set and self.is_thai_word(sibling_thai):
						choices_set.add(sibling_thai)
						all_choices.append(new_item)
			
			if len(all_choices) >= 3:
				ranked_choices, choices_with_score = self.choice_ranker.rank_choices(question_item, all_choices)
				choices = [question_item.answer] + ranked_choices[0:3]
			else:
				return []
			# choices = self.rank_choices(all_choices, answer)
		else:
			return []

		random.shuffle(choices)
		return choices

if __name__ == "__main__":
	cg = choice_generator()
	# print(cg.choice_generate("ความสัมพันธ์"))
	print(cg.choice_generate("3,434"))
