
from math import ceil

def display(question_item, percent=None, n_items=None, with_eng=False):
	if percent != None and percent in range(0, 101):
		n_display = ceil((len(question_item) * percent) / 100)
	elif n_items != None:
		n_display = min(n_items, len(question_item))
	else:
		n_display = len(question_item)

	if with_eng:
		display_with_eng(question_item, n_display)
	else:
		for i in range(0, n_display):
			question = question_item[i]
			print(str(i+1) + ". " + question.question)
			print("( " + str(question.answer) + " )")
			print("ก. " + str(question.choices[0]))
			print("ข. " + str(question.choices[1]))
			print("ค. " + str(question.choices[2]))
			print("ง. " + str(question.choices[3]))
			print("", end="\n\n")

def display_with_eng(question_item, n_display):
	for i in range(0, n_display):
		question = question_item[i]
		print(str(i+1) + ". " + question.question)
		print("( " + str(question.answer) + " - " + question.answer.eng_word + " )")
		print("ก. " + str(question.choices[0]) + " - " + question.choices[0].eng_word)
		print("ข. " + str(question.choices[1]) + " - " + question.choices[1].eng_word)
		print("ค. " + str(question.choices[2]) + " - " + question.choices[2].eng_word)
		print("ง. " + str(question.choices[3]) + " - " + question.choices[3].eng_word)
		print("", end="\n\n")

def write_list_to_file(question_item, filename):
	with open(filename, "w") as f:
		for question in question_item:
			f.write(repr(question) + "\n")

def get_articles(question_set):
	last_idx = -1
	sentences = []
	for question in question_set:
		if question.sentence_no != last_idx:
			sentences.append(question.sentence)
			last_idx = question.sentence_no
	return sentences