import preprocess.sentence_segment as _ss
import question.question_generator as _qg
import choices.choice_generator as _chg
import choices.word_item as _wi
import question_item as _qui

import sys
import pickle

ss = _ss.sentence_segment()
qg = _qg.question_generator()
chg = _chg.choice_generator()

# def main():
# 	args = sys.argv
# 	if len(args) == 3:
# 		article = open(args[1])
# 		outfile = open(args[2], "w")
# 	else:
# 		article = open("articles/gravity.in")
# 		outfile = open("articles/gravity.out", "w")

# 	lines = article.readlines()
# 	article.close()

# 	count = 0
# 	for line in lines:
# 		sentences, sen_with_pos = ss.sentence_segment(line, tri_gram=False)
# 		for i in range(len(sentences)):
# 			questions = qg.generate(sen_with_pos[i])
# 			outfile.write(sentences[i] + "\n\n")
# 			outfile.write("===============================\n\n")
# 			for question in questions:
# 				choices = cg.choice_generate(question[1])
# 				if len(choices) > 0:
# 					outfile.write(question[0] + "\n")
# 					outfile.write("(" + question[1] + ")\n\n")
# 					outfile.write("other choices: ")
# 					for choice in choices:
# 						outfile.write(choice + " / ")
# 					outfile.write("\n\n\n")
# 					count += 1

# 			outfile.write("===============================\n\n")
# 	outfile.close()
# 	print("questions = ", count)

# def test_paper(input_file, output_dir, tri_gram):
# 	file_name = (input_file.split("/"))[-1]
# 	file_name = (file_name.split("."))[0]
# 	suffix = ".tri" if tri_gram else ".bi"

# 	sen_file = open(output_dir + file_name + ".sen" + suffix, "w")
# 	pos_file = open(output_dir + file_name + ".pos" + suffix, "w")
# 	quest_file = open(output_dir + file_name + ".quest" + suffix, "w")

# 	with open(input_file, "r") as f:
# 		for line in f:
# 			# bi gram
# 			sentences, sen_with_pos = ss.sentence_segment(line, tri_gram=tri_gram)

# 			prg_questions = [] # all questions in a paragraph
# 			for i in range(len(sen_with_pos)):
# 				questions = qg.generate(sen_with_pos[i])
# 				sen_questions = []
# 				for tp in questions:
# 					(question, answer) = tp
# 					choices = cg.choice_generate(answer)
# 					if len(choices) > 0:
# 						sen_questions.append((question, answer, choices))
# 				prg_questions.append(sen_questions)

# 			sen_file.write(repr(sentences) + "\n")
# 			pos_file.write(repr(sen_with_pos) + "\n")
# 			quest_file.write(repr(prg_questions) + "\n")

# 	sen_file.close()
# 	pos_file.close()
# 	quest_file.close()

def main_process(input_file):
	sentence_count = 0
	all_questions = []

	with open(input_file) as f:
		for line in f:
			sentences = ss.sentence_segment(line)
			for i in range(len(sentences)):
				sentence_count += 1
				questions = qg.generate(sentences[i].pos)
				for tp in questions:
					(question, answer) = tp
					answer_item = _wi.word_item(answer)
					question_item = _qui.question_item(sentences[i], sentence_count, question, answer_item)

					choices = chg.choice_generate(answer_item)
					if len(choices) > 0:
						question_item.add_choices(choices)
						all_questions.append(question_item)

	f = open("testnow", "wb")
	pickle.dump(all_questions, f)
	f.close()

def test_read(file_name):
	with open(file_name, "rb") as f:
		all_sentences = pickle.load(f)
		print(all_sentences[0])

if __name__ == "__main__":
    args = sys.argv
    test_read("testnow")
    # if len(args) >= 2:
    # 	main_process(args[1])

    
