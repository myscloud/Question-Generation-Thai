#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import ast
import preprocess.sentence as sentence
import question_item as question_item
import choices.word_item as word_item
import choices.wordnet.wn_thai as wordnet_thai
import choices.choice_generator as choice_gen

_cg = choice_gen.choice_generator()

def find_blank_index(word_list, text):
	for i in range(len(word_list)):
		word = word_list[i]
		if word == text[0:len(word)]:
			text = text[len(word):]
		else:
			return i
	else:
		return None

def get_question_item(question_file, pos_file):
	sentences = []
	sentence_with_pos = []
	with open(pos_file) as f:
		for line in f:
			read_list = ast.literal_eval(line.strip())
			for a_sentence in read_list:
				sentences.append("".join([word for (word, _) in a_sentence]))
				sentence_with_pos.append(a_sentence)

	sentence_count = 0
	all_question_items = []
	with open(question_file) as f:
		for line in f:
			read_list = ast.literal_eval(line.strip())
			for a_sentence in read_list:
				sentence_item = sentence.sentence(sentences[sentence_count], sentence_with_pos[sentence_count])
				for a_question in a_sentence:
					(question_sentence, answer, choices) = a_question
					answer_item = word_item.word_item(answer)
					answer_index = find_blank_index([tp[0] for tp in sentence_with_pos[sentence_count]], question_sentence)
					all_generated_choices = _cg.choice_generate(answer_item)
					choice_items = []
					for a_choice in choices:
						if str(a_choice) == answer:
							choice_items.append(answer_item)
						else:
							for gen_choice in all_generated_choices:
								if str(gen_choice) == a_choice:
									choice_items.append(gen_choice)
									break

					# print([str(choice) for choice in choice_items])
					question = question_item.question_item(sentence_item, sentence_count, question_sentence, answer_item, answer_index)
					question.add_choices(choice_items)
					all_question_items.append(question)

				sentence_count += 1

	return all_question_items

if __name__ == "__main__":
	pos = [('ปรากฏการณ์', 'NCMN'), ('โลก', 'NCMN'), ('ร้อน', 'VATT'), (' ', 'NSBS'), ('หมายถึง', 'VSTA'), ('การ', 'FIXN'), ('เพิ่มขึ้น', 'VSTA'), ('ของ', 'RPRE'), ('อุณหภูมิ', 'NCMN'), ('เฉลี่ย', 'VACT'), ('ของ', 'RPRE'), ('อากาศ', 'NCMN'), ('ใกล้', 'RPRE'), ('พื้นผิว', 'NCMN'), ('โลก', 'NCMN'), ('และ', 'JCRG'), ('น้ำ', 'NCMN'), ('ใน', 'RPRE'), ('มหาสมุทร', 'NCMN'), ('ตั้งแต่', 'RPRE'), ('ช่วง', 'NCMN'), ('ครึ่งหลัง', 'NCNM'), ('ของ', 'RPRE'), ('คริสต์', 'NCMN'), ('ศตวรรษ', 'NCMN'), ('ที่', 'PREL'), (' ', 'NSBS'), ('20', 'DCNM'), (' ', 'NSBS'), ('และ', 'JCRG'), ('มี', 'VSTA'), ('การคาดการณ์', 'FIXN'), ('ว่า', 'RPRE'), ('อุณหภูมิ', 'NCMN'), ('เฉลี่ย', 'VACT'), ('จะ', 'XVBM'), ('เพิ่มขึ้น', 'VSTA'), ('อย่างต่อเนื่อง', 'ADVP')]
	text = 'ปรากฏการณ์โลกร้อน หมายถึงการเพิ่มขึ้นของ ________ เฉลี่ยของอากาศใกล้พื้นผิวโลกและน้ำในมหาสมุทรตั้งแต่ช่วงครึ่งหลังของคริสต์ศตวรรษที่ 20 และมีการคาดการณ์ว่าอุณหภูมิเฉลี่ยจะเพิ่มขึ้นอย่างต่อเนื่อง'
	answer_index = find_blank_index([tp[0] for tp in pos], text)
	print(answer_index)
