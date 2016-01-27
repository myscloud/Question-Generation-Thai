import word_processing
import orchid_corpus
import sentence_segment
import question_generate

import sys

def main():
	orchid = orchid_corpus.orchid_corpus()
	ss = sentence_segment.sentence_segment(orchid)
	wp = word_processing.word_processing()
	qg = question_generate.question_generate()


	args = sys.argv
	if len(args) == 3:
		article = open(args[1])
		outfile = open(args[2], "w")
	else:
		article = open("articles/comet.in")
		outfile = open("articles/results.out", "w")

	lines = article.readlines()
	article.close()

	for line in lines:
		sentences, sen_with_pos = ss.sentence_segment(line, tri_gram=False)
		for i in range(len(sentences)):
			questions = qg.generate(sen_with_pos[i])
			outfile.write(sentences[i] + "\n\n")
			outfile.write("===============================\n\n")
			for question in questions:
				outfile.write(question[0] + "\n")
				outfile.write("(" + question[1] + ")\n\n")

			outfile.write("===============================\n\n")
	outfile.close()

if __name__ == "__main__":
    main()
