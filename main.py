
import word_processing
import orchid_corpus
import POS_tag

import time

def main():
	orchid = orchid_corpus.orchid_corpus()
	post = POS_tag.POS_tag(orchid)
	post.test_print()


if __name__ == "__main__":
    main()