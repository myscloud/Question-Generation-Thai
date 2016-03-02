
import ast
import csv
import statistics as stats
import wordnet.wordnetthai as wnth

from math import floor
from numpy import histogram

class question_item:
	def __init__(self, question_property, pos):
		(self.question_sentence, self.answer, self.choices) = question_property
		self.question_pos = pos
		self.question_eval = []
		self.choices_eval = []

	def get_word_list(self):
		return [word_pos[0] for word_pos in self.question_pos]

	def add_evaluation(self, quest_eval, choices_eval):
		self.question_eval.append(quest_eval)
		if quest_eval > 1:
			self.choices_eval.append(choices_eval)

	def get_question_average_rank(self):
		try:
			return stats.mode(self.question_eval)
		except stats.StatisticsError:
			return 2

	def get_choices_average_rank(self):
		if len(self.choices_eval) == 0:
			return None

		ordered_eval = [ [] for i in range(0, 4)]
		count = 0
		for vote in self.choices_eval:
			for i in range(len(vote)):
				ordered_eval[i].append(vote[i])
			count += 1

		average_choices = []
		for choice in ordered_eval:
			try:
				avg = stats.mode(choice)
			except stats.StatisticsError:
				avg = min(choice)
			average_choices.append(avg)

		return average_choices


	def __str__(self):
		txt = ""
		txt += "question: " + self.question_sentence + "\n"
		txt += "answer: " + self.answer + "\n"
		txt += "choices: " + str(self.choices) + "\n"
		txt += "pos: " + str(self.question_pos) + "\n"
		return txt

#########################################################################################
####################################### analysis ########################################

def summarize_question_average(question_eval):
	ranks = [0, 0, 0, 0]
	for eval in question_eval:
		ranks[eval] += 1

	print("From " + str(len(question_eval)) + " questions...")
	for i in range(3, 0, -1):
		print("question with rank " + str(i) + " = ", str(ranks[i]) + " (" + str(round((ranks[i]/len(question_eval) * 100), 2)) + "%)")
	return ranks

def summarize_choices_average(question_eval, choices_eval):
	ranks = [0, 0, 0]
	choices_count = 0

	for i in range(len(question_eval)):
		if question_eval[i] >= 2:
			for choice in choices_eval[i]:
				if choice != "-":
					ranks[int(choice)+1] += 1
					choices_count += 1

	print("From ", choices_count, " choices...")
	print("relevant choices: ", ranks[2], " (", round((ranks[2] / choices_count * 100),2), "% )")
	print("irrelevant choices: ", ranks[1], " (", round((ranks[1] / choices_count * 100),2), "% )")
	print("confusing choices: ", ranks[0], " (", round((ranks[0] / choices_count * 100),2), "% )")

def analyse_question_dict(test_set, file_name):
	dict_set = set()
	with open(file_name) as dict_file:
		for line in dict_file:
			dict_set.add(line.strip())

	results = []
	for question in test_set:
		word_list = question.get_word_list()
		known_word = 0
		for word in word_list:
			if word in dict_set:
				known_word += 1

		known_ratio = round((known_word / len(word_list)) * 100, 2)
		results.append(known_ratio)

	return results

def analyse_answer_height(test_set, choices_eval, question_eval):
	wn = wnth.wordnetthai()
	all_choice_height = []
	for i in range(len(question_eval)):
		if question_eval[i] >= 2:
			choices = test_set[i].choices
			choice_height = []
			for j in range(len(choices)):
				if choices[j] != "-":
					height = wn.get_word_height(choices[j])
					choice_height.append(height)
				all_choice_height.append(choice_height)
		else:
			all_choice_height.append([])
	return all_choice_height		

def plot_choice_height(choices_eval, choices_height):
	eval_score = []
	eval_height = []
	print(choices_eval)
	print(choices_height)
	print(len(choices_eval))
	print(len(choices_height))
	# for i in range(len(choices_height)):
	# 	for j in range(len(choices_height[i])):
	# 		if choices_eval[i][j] != '-':
	# 			eval_score.append(choices_eval[i][j])
	# 			eval_height.append(choices_height[i][j])

	print(eval_score)
	print(eval_height)

def plot_histogram(eval_results, analyse_results, acceptable):
	if len(eval_results) != len(analyse_results):
		return None
	
	accept_bin = [0] * 10
	all_bin = [0] * 10
	for i in range(len(eval_results)):
		bin_no = floor(analyse_results[i] / 10)
		if bin_no > 9: bin_no = 9
		all_bin[bin_no] += 1
		if eval_results[i] >= acceptable:
			accept_bin[bin_no] += 1

	for i in range(len(all_bin)):
		ratio = accept_bin[i] / all_bin[i] if all_bin[i] > 0 else 0
		start, end = (i*10), (i+1)*10
		print("from known word ratio ", start, " to ", end, " %: ", ratio)

################################# just for read results ################################# 

def read_results(question_file, pos_file):
	test_set = []
	sentence_pos = []
	
	with open(pos_file) as pfile:
		for line in pfile:
			paragraph = ast.literal_eval(line)
			for sentence in paragraph:
				sentence_pos.append(sentence)

	sentence_count = 0
	with open(question_file) as qfile:
		for line in qfile:
			question_struct = ast.literal_eval(line)
			for sentence in question_struct:
				for question in sentence:
					new_question = question_item(question, sentence_pos[sentence_count])
					test_set.append(new_question)

				sentence_count += 1

	return test_set

def add_eval_score(eval_file, test_set):
	with open(eval_file) as csvfile:
		spamreader = csv.reader(csvfile)
		question_count = 0
		for row in spamreader:
			quest_rank = int(row[1])
			choices_rank = row[2:]
			test_set[question_count].add_evaluation(quest_rank, choices_rank)
			question_count += 1

	return test_set

#########################################################################################

def test_1():
	test_question_set = read_results("wikipedia-article/globalwarming/globalwarming-cut.quest.bi", "wikipedia-article/globalwarming/globalwarming-cut.pos.bi")
	test_question_set = test_question_set[:35]
	test_question_set = add_eval_score("wikipedia-article/globalwarming/results1.csv", test_question_set)
	test_question_set = add_eval_score("wikipedia-article/globalwarming/results2.csv", test_question_set)
	test_question_set = add_eval_score("wikipedia-article/globalwarming/results3.csv", test_question_set)

	# question analysis
	question_average = [question.get_question_average_rank() for question in test_question_set]
	# summarize_question_average(question_average)
	print("")
	
	# choices analysis
	choices_average = [question.get_choices_average_rank() for question in test_question_set]
	# summarize_choices_average(question_average, choices_average)
	print("")

	print("Lexto")
	lexto_results = analyse_question_dict(test_question_set, "LongLexTo/lexitron_original.txt")
	plot_histogram(question_average, lexto_results, 3)
	print("")

	print("Orchid")
	orchid_results = analyse_question_dict(test_question_set, "LongLexTo/orchid_words.txt")
	plot_histogram(question_average, orchid_results, 3)

	# choices_height = analyse_answer_height(test_question_set, choices_average, question_average)
	# plot_choice_height(choices_average, choices_height)
	


if __name__ == "__main__":
	test_1()
