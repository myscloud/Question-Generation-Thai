
import ast
import csv
import question_item as qi
import matplotlib.pyplot as plt
from math import floor, ceil

def opencsv(filename):
	firstline = True
	quest_eval = []
	with open(filename) as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			if firstline:
				questno = int((len(row) - 4)/5)
				for i in range(questno):
					d = {"question": [], "choices": [[], [], [], []]}
					quest_eval.append(d)
				firstline = False
			else:
				rating = row[1: -3]
				for i in range(len(rating)):
					if i % 5 == 0:
						quest_eval[int(i/5)]["question"].append(int(rating[i]))
					else:
						quest_no = int(i/5)
						choice_no = (i%5) - 1
						if rating[i] != "":
							quest_eval[quest_no]["choices"][choice_no].append(1)
						else:
							quest_eval[quest_no]["choices"][choice_no].append(0)

	return quest_eval

def evaluate(path, start, end, questfile):
	evalresults = []
	for counter in range(start, end+1):
		evalfile = path + str(counter) + ".csv"
		partresults = opencsv(evalfile)
		evalresults.extend(partresults)

	data = {"market-dict": [], "market-nodict": [], "taxonomy-dict": [], "taxonomy-nodict": []}
	question_count = 0
	with open(questfile) as f:
		for line in f:
			(quest_str, index, quest_no) = ast.literal_eval(line.strip())
			quest_no = int(quest_no)
			while len(data[index]) <= quest_no:
				data[index].append(None)

			new_quest_item = qi.question_item(from_str=quest_str)
			new_quest_item.add_evaluations(evalresults[question_count]["question"])
			for j in range(len(new_quest_item.choices)):
				choice = new_quest_item.choices[j]
				if choice.is_distractor:
					choice.add_evaluations(evalresults[question_count]["choices"][j])

			data[index][quest_no] = new_quest_item
			question_count += 1

	return data

def question_eval(data, percent):
	n_quest = ceil((len(data) * percent) / 100)
	passed_questions = 0
	for i in range(n_quest):
		question = data[i]
		if question.get_average_eval() >= 0.5:
			passed_questions += 1

	return ((passed_questions / n_quest) * 100), passed_questions, n_quest

def choice_eval(data):
	all_choices = 0
	passed_choices = 0
	hist_choices = [0, 0, 0, 0]
	for question in data:
		if question.get_average_eval() >= 0.5:
			per_quest = 0
			for choice in question.choices:
				if choice.is_distractor():
					all_choices += 1
					if choice.get_average_eval() >= 0.5:
						passed_choices += 1
						per_quest += 1

			hist_choices[per_quest] += 1

	n_passed_quest = sum(hist_choices)
	ratio_choices = [ x / n_passed_quest for x in hist_choices ]
	return ratio_choices, hist_choices, passed_choices, all_choices

def plot_question(data_nodict, data_wdict):
	x_axis = []
	y_nodict = []
	y_wdict = []

	for percent in range(5, 105, 5):
		x_axis.append(percent)
		percent_nodict, _, _ = question_eval(data_nodict, percent)
		percent_wdict, _, _ = question_eval(data_wdict, percent)
		y_nodict.append(percent_nodict)
		y_wdict.append(percent_wdict)

	ax = plt.subplot()

	ax.set_ylim(60, 100)
	wdict_line, = plt.plot(x_axis, y_wdict, 'go-', label="questions with dictionary")
	nodict_line, = plt.plot(x_axis, y_nodict, 'bs--', label="questions without dictionary")

	plt.legend(handles=[wdict_line, nodict_line])

	# plt.title("Acceptability of generated questions")
	plt.xlabel("%")
	plt.ylabel("Percentage of acceptable questions from lists of top-n ranked questions")
	plt.show()



if __name__ == "__main__":
	data = evaluate("test/feedback/eval", 1, 16, "test/all-questions.list")
	data_nodict = data["market-nodict"]
	data_nodict.extend(data["taxonomy-nodict"])
	
	data_wdict = data["market-dict"]
	data_wdict.extend(data["taxonomy-dict"])

	plot_question(data_nodict, data_wdict)

