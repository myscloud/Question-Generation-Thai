
import wordnet.wordnetthai as wnth
import math
import random

class choice_generator:

	def __init__(self):
		self.wn = wnth.wordnetthai()

	# return True if word contains at least 1 thai character
	def is_thai_word(self, word):
		for char in word:
			if ord(char) in range(3585, 3676):
				return True
		return False

	# return an integer if word represents an integer, return None otherwise
	def get_integer(self, word):
		comma = False
		if "," in word:
			word = word.replace(",", "")
			comma = True

		try:
			number = int(word)
			return number, comma
		except ValueError:
			return None, False	

	def int_choice_generate(self, number):
		choices = set()
		choices.add(number)

		multiply = int(number / abs(number))
		lg = math.log10(abs(number))
		exp = math.floor(lg) - 1
		remain = int(number % (10**exp))

		while len(choices) < 4:
			if exp >= 0:
				r = random.randrange(10, 100)
				newchoice = multiply * int((r * 10**exp) + remain)
			else:
				newchoice = multiply * random.randrange(1, 10)
			choices.add(newchoice)

		return list(choices)

	def choice_generate(self, answer):
		if self.is_thai_word(answer):
			hyponyms = self.wn.get_siblings(answer)
			thai_hyponyms = []
			for word in hyponyms:
				if self.is_thai_word(word): thai_hyponyms.append(word)
			return thai_hyponyms
		else:
			number, comma = self.get_integer(answer)
			if number != None:
				choices = self.int_choice_generate(number)
				if comma: 
					return ["{:,}".format(num) for num in choices]
				else: 
					return choices
			else:
				return []


if __name__ == "__main__":
	cg = choice_generator()
	# print(cg.choice_generate("ความสัมพันธ์"))
	print(cg.choice_generate("-2"))
