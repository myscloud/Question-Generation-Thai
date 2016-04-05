
import ranking.evaluate as _ev
import ranking.question_ranker as qrank
import choices.choice_ranker as chrank
import question_item as _qui

from os import listdir
from os.path import isfile, join
import csv
import ast

def get_files_list_from_dir(dictdir, suffix):
	files = [join(dictdir, f) for f in listdir(dictdir) if isfile(join(dictdir, f)) and f.endswith(suffix)]
	return files

def read_custom_dict(dictdir):
	files = get_files_list_from_dir(dictdir, ".csv")
	
	custom_dict = dict()
	for filename in files:
		with open(filename, encoding="utf-8") as csvfile:
			reader = csv.reader(csvfile)
			next(reader, None)
			for row in reader:
				edited_info = [data if data != "" else None for data in row]
				word = edited_info[0]
				if word not in custom_dict:
					d = dict()
					d["pos"], d["eng"], d["sense"] = edited_info[1:]
					if d["sense"] != None:
						d["sense"] = int(d["sense"])
					custom_dict[word] = d

	return custom_dict

def train_ranking_model(question_file, eval_files=None, eval_dir=None, wordnet=None):
	all_questions = []
	with open(question_file, "r") as f:
		for line in f:
			a_question_item = _qui.question_item(from_str=line.strip())
			all_questions.append(a_question_item)

	eval_files = []
	if eval_dir != None:
		eval_files = get_files_list_from_dir(eval_dir, ".csv")

	for eval_file in eval_files:
		_ev.read_eval_file(eval_file, all_questions)

	qr = qrank.question_ranker(question_set=all_questions)
	choice_rank = chrank.choice_ranker(training_set=all_questions, wordnet=wordnet)
	return qr, choice_rank

def read_from_file(filename):
	all_questions = []
	with open(filename, "r") as f:
		for line in f:
			new_question = _qui.question_item(from_str=line.strip())
			all_questions.append(new_question)
	return all_questions

def read_from_tuple_file(filename):
	all_questions = []
	with open(filename, "r") as f:
		for line in f:
			tp = ast.literal_eval(line.strip())
			question_txt, _, _ = tp
			new_question = _qui.question_item(from_str=question_txt)
			all_questions.append(new_question)
	return all_questions
