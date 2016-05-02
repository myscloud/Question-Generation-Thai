
import csv

def read_eval_file(eval_file, test_set):
	with open(eval_file) as csvfile:
		spamreader = csv.reader(csvfile)
		question_count = 0
		for row in spamreader:
			quest_rank = int(row[1])
			test_set[question_count].add_evaluation(quest_rank)
			if quest_rank > 1 and len(test_set[question_count].choices) == 4:
				choices_rank = row[2:]
				for i in range(len(choices_rank)):
					if choices_rank[i] != "-":
						test_set[question_count].choices[i].add_evaluation(int(choices_rank[i]))
			question_count += 1

	# return test_set
