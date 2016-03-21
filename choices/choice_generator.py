
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
			if ord(char) in range(3585, 3676):
				return True
		return False

	# return an integer if word represents an integer, return None otherwise
	# def get_integer(self, word):
	# 	comma = False
	# 	if "," in word:
	# 		word = word.replace(",", "")
	# 		comma = True

	# 	try:
	# 		number = int(word)
	# 		return number, comma
	# 	except ValueError:
	# 		return None, False	

	# def int_choice_generate(self, number):
	# 	choices = set()
	# 	choices.add(number)

	# 	multiply = int(number / abs(number))
	# 	lg = math.log10(abs(number))
	# 	exp = math.floor(lg) - 1
	# 	remain = int(number % (10**exp))

	# 	while len(choices) < 4:
	# 		if exp >= 0:
	# 			r = random.randrange(10, 100)
	# 			newchoice = multiply * int((r * 10**exp) + remain)
	# 		else:
	# 			newchoice = multiply * random.randrange(1, 10)
	# 		choices.add(newchoice)

	# 	return list(choices)


	# def rank_choices(self, siblings, answer):
	# 	choices_item = []
	# 	choices_word = set()
	# 	choices_item.append(answer)
	# 	choices_word.add(answer.word)

	# 	len_list = [(item, abs(len(answer.word) - len(item.word))) for item in siblings]
	# 	sorted_list = sorted(len_list, key=lambda x: x[1])

	# 	for tp in sorted_list:
	# 		word = tp[0].word
	# 		if self.is_thai_word(word) and word not in choices_word:
	# 			choices_word.add(word)
	# 			choices_item.append(tp[0])

	# 		if len(choices_item) >= 4:
	# 			return choices_item

	# 	return [] # in case no. of choices is less than 4


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

		# random.shuffle(choices)
		return choices


if __name__ == "__main__":
	cg = choice_generator()
	# print(cg.choice_generate("ความสัมพันธ์"))
	print(cg.choice_generate("3,434"))
