
class sentence:
	def __init__(self, sentence_content, sentence_pos):
		self.content = sentence_content
		self.pos = sentence_pos

	def __str__(self):
		return self.content