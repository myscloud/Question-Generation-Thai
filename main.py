import preprocess.sentence_segment as _ss
import question.question_generator as _qg
import choices.choice_generator as _chg
import choices.word_item as _wi
import choices.wordnet.wn_thai as _wnth
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
wnth = _wnth.wordnet_thai()
chg = _chg.choice_generator(wnth)

def read_custom_dict(dictdir):
	files = [join(dictdir, f) for f in listdir(dictdir) if isfile(join(dictdir, f))]
	
	custom_dict = dict()
	for filename in files:
		if filename[-4:] == ".csv":
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
					ans_eng, ans_index = wnth.get_general_info(answer)
					answer_item = _wi.word_item(answer, ans_eng, ans_index, None)
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

def get_article(question_set):
	last_idx = -1
	sentences = []
	for question in question_set:
		if question.sentence_no != last_idx:
			sentences.append(question.sentence)
			last_idx = question.sentence_no
	return sentences

def print_sentence_cut_results(question_set):
	sentences = get_article(generated_questions)
	for sentence in sentences:
		print(str(sentence))
	print("======================")

	for sentence in sentences:
		for word, pos in sentence.pos:
			print(word, pos)
		print("--------", end="\n\n")

if __name__ == "__main__":
    args = sys.argv

    custom_dict = dict()
    if len(args) >= 2:
    	if len(args) >= 3:
    		custom_dict = read_custom_dict(args[2])
    		ss.set_custom_dict(custom_dict)
    		wnth.set_custom_dict(custom_dict)
    	generated_questions = main_process(args[1])

    # all_questions = []
    # with open("ranking/test-globalwarming.out", "r") as f:
    # 	for line in f:
    # 		a_question_item = _qui.question_item(from_str=line.strip())
    # 		all_questions.append(a_question_item)
    
    # _ev.read_eval_file("ranking/evaluation/sheet1.csv", all_questions)
    # _ev.read_eval_file("ranking/evaluation/sheet2.csv", all_questions)
    # _ev.read_eval_file("ranking/evaluation/sheet3.csv", all_questions)
    # qr = qrank.question_ranker(question_set=all_questions)

    # ranked_question, ranked_scores = qr.rank_question(generated_questions)
    f = open("sun-atmosphere.dict", "w")
    for question in generated_questions:
    	f.write(str(question.question) + "\n")
    	f.write("( " + str(question.answer) + " )\n")
    	for choice in question.choices:
    		f.write(str(choice) + "\t" + str(choice.eng_word) + "\n")
    	f.write("\n\n")
    	# f.write(str(score) + "\n\n")
    f.close()

