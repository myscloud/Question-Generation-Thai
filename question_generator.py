import preprocess.sentence_segment as _ss
import question.question_generator as _qg
import choices.choice_generator as _chg
import choices.wordnet.wn_thai as _wnth
import question_item as _qui
import choices.word_item as _wi
import initialize as init_proc

import json


ss = _ss.sentence_segment()
qg = _qg.question_generator()
wnth = _wnth.wordnet_thai()
chg = None
qr = None
choice_rank = None
qr, choice_rank = init_proc.train_ranking_model("ranking/test-globalwarming.out", eval_dir="ranking/evaluation/", wordnet=wnth)
chg = _chg.choice_generator(wnth, choice_rank)

def generate_questions(article):
	sentence_count = 0
	gen_questions = []
	final_questions = []

	sentences = ss.sentence_segment(article, tri_gram=False)
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
	for question in ranked_questions:
		choices = chg.generate_choices(question)
		if choices != []:
			question.add_choices(choices)
			final_questions.append(question)

	formatted_questions = []
	for q in final_questions:
		choices_list = [str(c) for c in q.choices]
		formatted_questions.append([q.question, choices_list])

	return formatted_questions
	# return json.dumps(formatted_questions, ensure_ascii=False)
