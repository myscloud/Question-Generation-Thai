import word_processing
import orchid_corpus
import sentence_segment
import question_generate
import choice_generator

import sys

if __name__ == "__main__":
	orchid = orchid_corpus.orchid_corpus()
	ss = sentence_segment.sentence_segment(orchid)
	wp = word_processing.word_processing()
	qg = question_generate.question_generate()
	cg = choice_generator.choice_generator()

	args = sys.argv
	if len(args) == 2:
		file_name = args[1]

	article_dir = "wikipedia-article/"
	out_bi = open(article_dir + "cut-sentence/" + file_name + ".bi", "w")
	out_tri = open(article_dir + "cut-sentence/" + file_name + ".tri", "w")

	with open(article_dir + "raw-content/" + file_name + ".in", "r") as f:
		for line in f:
			sentences_bi, _ = ss.sentence_segment(line, tri_gram=False)
			for sentence in sentences_bi:
				out_bi.write(sentence + "\n")

			sentences_tri, _ = ss.sentence_segment(line, tri_gram=True)
			for sentence in sentences_tri:
				out_tri.write(sentence + "\n")

	out_bi.close()
	out_tri.close()

