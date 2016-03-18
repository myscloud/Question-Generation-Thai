import preprocess.sentence_segment as _ss
import question.question_generator as _qg
import choices.choice_generator as _chg
import choices.word_item as _wi
import question_item as _qui
import ranking.evaluate as _ev
import ranking.analyse as _anl
import ranking.question_ranker as qrank

import ast
import sys
import pickle

from os import listdir
from os.path import isfile, join
import csv

import choices.wordnet.wn_tree as wn_tree

ss = _ss.sentence_segment()
qg = _qg.question_generator()
chg = _chg.choice_generator()

def read_custom_dict(dictdir):
	files = [join(dictdir, f) for f in listdir(dictdir) if isfile(join(dictdir, f))]
	
	custom_dict = dict()
	for filename in files:
		with open(filename) as csvfile:
			reader = csv.reader(csvfile)
			next(reader, None)
			for row in reader:
				edited_info = [data if data != "" else None for data in row]
				word = edited_info[0]
				if word not in custom_dict:
					d = dict()
					d["pos"], d["eng"], d["sense"] = edited_info[1:]
					custom_dict[word] = d

	return custom_dict

def main_process(input_file):
	sentence_count = 0
	all_questions = []

	with open(input_file, "r") as f:
		for line in f:
			sentences = ss.sentence_segment(line, tri_gram=False)
			sentence_count += 1

			for i in range(len(sentences)):
				questions = qg.generate(sentences[i].pos)
				for tp in questions:
					(question, answer, answer_index) = tp
					answer_item = _wi.word_item(answer)
					question_item = _qui.question_item(sentences[i], sentence_count, question, answer_item, answer_index)

					choices = chg.choice_generate(answer_item)
					if len(choices) > 0:
						question_item.add_choices(choices)
						all_questions.append(question_item)


	# print(len(all_questions))
	return all_questions

	# f = open("testnow", "wb")
	# pickle.dump(all_questions, f)
	# f.close()

def test_read(file_name):
	with open(file_name, "rb") as f:
		all_questions = pickle.load(f)
		return all_questions

if __name__ == "__main__":
    args = sys.argv

    if len(args) >= 2:
    	generated_questions = main_process(args[1])

    all_questions = []
    with open("ranking/test-globalwarming.out", "r") as f:
    	for line in f:
    		a_question_item = _qui.question_item(from_str=line.strip())
    		all_questions.append(a_question_item)
    
    _ev.read_eval_file("ranking/evaluation/sheet1.csv", all_questions)
    _ev.read_eval_file("ranking/evaluation/sheet2.csv", all_questions)
    _ev.read_eval_file("ranking/evaluation/sheet3.csv", all_questions)
    qr = qrank.question_ranker(question_set=all_questions)

    ranked_question, ranked_scores = qr.rank_question(generated_questions)
    f = open("bank.rank", "w")
    for question, score in ranked_scores:
    	f.write(str(question.question) + "\n")
    	f.write("( " + str(question.answer) + " )\n")
    	for choice in question.choices:
    		f.write(str(choice) + "\t" + str(choice.eng_word) + "\n")
    	f.write("\n")
    	f.write(str(score) + "\n\n")
    f.close()

    
    # for custom dictionary

    # custom_dict = dict()
    # if len(args) >= 3:
    # 	custom_dict = read_custom_dict(args[2])
    # ss = _ss.sentence_segment(custom_dict=custom_dict)
    # main_process(args[1])


    
