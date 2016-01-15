
import word_processing
import orchid_corpus
import POS_tag
import sentence_segment

import time

def main():
	orchid = orchid_corpus.orchid_corpus()
	ss = sentence_segment.sentence_segment(orchid)
	wp = word_processing.word_processing()
	# post = POS_tag.POS_tag(orchid)
	
	article = open("test/comet.in")
	lines = article.readlines()
	article.close()

	for line in lines:
		words = wp.word_segment(line)
		new_paragraph, path = ss.sentence_segment(words)

		for i in range(len(path)):
			if path[i] == "SBS":
				print("")
				print("=======================")
				print("")
			else:
				print(new_paragraph[i], path[i])

		print("")

if __name__ == "__main__":
    main()