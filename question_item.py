
class question_item:
	def __init__(self, sentence, sentence_no, question, answer):
		self.sentence = sentence
		self.sentence_no = sentence_no
		self.question = question
		self.answer = answer
		self.choices = None

	def add_choices(self, new_choices):
		self.choices = new_choices

	def __str__(self):
		txt = self.question + "\n"
		for choice in self.choices:
			txt += choice.word + "\t"
		txt += "\n" + str(self.sentence.pos)
		return txt