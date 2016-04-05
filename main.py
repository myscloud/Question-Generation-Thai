import preprocess.sentence_segment as _ss
import question.question_generator as _qg
import choices.choice_generator as _chg
import choices.wordnet.wn_thai as _wnth
import question_item as _qui
import choices.word_item as _wi
import display_results as display
import initialize as init_proc

import sys

ss = _ss.sentence_segment()
qg = _qg.question_generator()
wnth = _wnth.wordnet_thai()
chg = None
qr = None
choice_rank = None



def main_process(input_file):
	sentence_count = 0
	gen_questions = []
	final_questions = []

	with open(input_file, "r") as f:
		for line in f:
			sentences = ss.sentence_segment(line, tri_gram=False)

			for i in range(len(sentences)):
				questions = qg.generate(sentences[i].pos)
				for tp in questions:
					(question, answer, answer_index) = tp
					ans_eng, ans_index = wnth.get_general_info(answer)
					answer_item = _wi.word_item(answer, ans_eng, ans_index, None)
					question_item = _qui.question_item(sentences[i], sentence_count, question, answer_item, answer_index)
					gen_questions.append(question_item)

				sentence_count += 1
			
	ranked_questions, qrank_scores = qr.rank_question(gen_questions)
	# ranked_questions = gen_questions   # don't rank
	for question in ranked_questions:
		choices = chg.generate_choices(question)
		if choices != []:
			question.add_choices(choices)
			final_questions.append(question)

	return final_questions


if __name__ == "__main__":
    
    qr, choice_rank = init_proc.train_ranking_model("ranking/test-globalwarming.out", eval_dir="ranking/evaluation/", wordnet=wnth)
    chg = _chg.choice_generator(wnth, choice_rank)

    args = sys.argv
    custom_dict = dict()
    if len(args) >= 2:
    	if len(args) >= 3:
    		custom_dict = init_proc.read_custom_dict(args[2])
    		ss.set_custom_dict(custom_dict)
    		wnth.set_custom_dict(custom_dict)
    	generated_questions = main_process(args[1])
    	# display.write_list_to_file(generated_questions, "test/market.wdict.list")
    	display.display(generated_questions)

    # all_questions = init_proc.read_from_file("test/all-questions.list")
    # all_questions = init_proc.read_from_tuple_file("test/all-questions.list")
    # display.display(all_questions, percent=100)
    # article = display.get_articles(all_questions)
    # for sentence in article:
    	# print("- ", sentence)
    	# for word, pos in sentence.pos:
    	# 	print(word, pos)
    	# print("------------")
