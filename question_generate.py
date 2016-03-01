
class question_generate:

	def __init__(self):
		pass

	def generate(self, sen_with_pos):
		noun_idx = []
		
		for i in range(len(sen_with_pos)):
			word = sen_with_pos[i]
			# print(word, type(word))
			if word[1] == "NCMN" or word[1] == "NPRP":
				noun_idx.append(i)

		questions = []
		sen = [ word[0] for word in sen_with_pos ]
		for idx in noun_idx:
			answer = sen[idx]
			sen[idx] = " ________ "
			new_quest = "".join(sen)
			sen[idx] = answer

			questions.append( (new_quest, answer) )

		return questions

