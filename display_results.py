
from math import ceil

def display(question_item, percent=None, n_items=None):
	if percent != None and percent in range(0, 101):
		n_display = ceil((len(question_item) * percent) / 100)
	elif n_items != None:
		n_display = min(n_items, len(question_item))
	else:
		n_display = len(question_item)

	for i in range(0, n_display):
		question = question_item[i]
		print(str(i+1) + ". " + question.question)
		print("( " + str(question.answer) + " )")
		print("ก. " + str(question.choices[0]))
		print("ข. " + str(question.choices[1]))
		print("ค. " + str(question.choices[2]))
		print("ง. " + str(question.choices[3]))
		print("", end="\n\n")
