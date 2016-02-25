import word_processing
import orchid_corpus
import sentence_segment
import question_generate
import choice_generator

import test_model as tm

import sys

orchid = orchid_corpus.orchid_corpus()
ss = sentence_segment.sentence_segment(orchid)
wp = word_processing.word_processing()
qg = question_generate.question_generate()
cg = choice_generator.choice_generator()

def main():
	args = sys.argv
	if len(args) == 3:
		article = open(args[1])
		outfile = open(args[2], "w")
	else:
		article = open("articles/gravity.in")
		outfile = open("articles/gravity.out", "w")

	lines = article.readlines()
	article.close()

	count = 0
	for line in lines:
		sentences, sen_with_pos = ss.sentence_segment(line, tri_gram=False)
		for i in range(len(sentences)):
			questions = qg.generate(sen_with_pos[i])
			outfile.write(sentences[i] + "\n\n")
			outfile.write("===============================\n\n")
			for question in questions:
				choices = cg.choice_generate(question[1])
				if len(choices) > 0:
					outfile.write(question[0] + "\n")
					outfile.write("(" + question[1] + ")\n\n")
					outfile.write("other choices: ")
					for choice in choices:
						outfile.write(choice + " / ")
					outfile.write("\n\n\n")
					count += 1

			outfile.write("===============================\n\n")
	outfile.close()
	print("questions = ", count)

def test_paper(input_file, output_dir, tri_gram):
	file_name = (input_file.split("/"))[-1]
	file_name = (file_name.split("."))[0]
	suffix = ".tri" if tri_gram else ".bi"

	sen_file = open(output_dir + file_name + ".sen" + suffix, "w")
	pos_file = open(output_dir + file_name + ".pos" + suffix, "w")
	quest_file = open(output_dir + file_name + ".quest" + suffix, "w")

	with open(input_file, "r") as f:
		for line in f:
			# bi gram
			sentences, sen_with_pos = ss.sentence_segment(line, tri_gram=tri_gram)

			prg_questions = [] # all questions in a paragraph
			for i in range(len(sen_with_pos)):
				questions = qg.generate(sen_with_pos[i])
				sen_questions = []
				for tp in questions:
					(question, answer) = tp
					choices = cg.choice_generate(answer)
					if len(choices) > 0:
						sen_questions.append((question, answer, choices))
				prg_questions.append(sen_questions)

			sen_file.write(repr(sentences) + "\n")
			pos_file.write(repr(sen_with_pos) + "\n")
			quest_file.write(repr(prg_questions) + "\n")

	sen_file.close()
	pos_file.close()
	quest_file.close()



if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
    	if args[1] == "all":
    		pass
    	else:
    		# test_paper(args[1], args[2], False)
    		test_paper(args[1], args[2], True)
