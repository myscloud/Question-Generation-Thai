
import initialize as init_proc
import random

def question_set_random(topics):
	all_questions = []
	for topic in topics:
		nodict_questions = init_proc.read_from_file("test/" + topic + ".nodict.list")
		dict_questions = init_proc.read_from_file("test/" + topic + ".wdict.list")

		for i in range(len(nodict_questions)):
			all_questions.append((repr(nodict_questions[i]), topic + "-nodict", i))

		for i in range(len(dict_questions)):
			all_questions.append((repr(dict_questions[i]), topic + "-dict", i))

	random.shuffle(all_questions)

	with open("test/all-questions.list", "w") as f:
		for question_tuple in all_questions:		
			f.write(repr(question_tuple) + "\n")

if __name__ == "__main__":
	question_set_random(["market", "taxonomy"])