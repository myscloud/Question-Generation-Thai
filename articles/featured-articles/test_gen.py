from ast import literal_eval

def sentence_gen(bigram_file, trigram_file, to_write):
	bi = open(bigram_file)
	tri = open(trigram_file)
	inq = open(to_write, "w")

	paragraphs_bi = bi.readlines()
	paragraphs_tri = tri.readlines()
	
	for i in range(len(paragraphs_bi)):
		inq.write("การแบ่งแบบ A\n")
		sentences_bi = literal_eval(paragraphs_bi[i])
		for sentence in sentences_bi:
			inq.write("___ " + sentence + "\n")

		inq.write("\nการแบ่งแบบ B\n")
		sentences_tri = literal_eval(paragraphs_tri[i])
		for sentence in sentences_tri:
			inq.write("___ " + sentence + "\n")

		inq.write("\n__ เลือกแบบ A\t__ เลือกแบบ B\n\n")
		inq.write("----------------------------------\n\n")

	
	bi.close()
	tri.close()
	inq.close()

def question_gen(bigram_file, to_write):
	bi = open(bigram_file)
	inq = open(to_write, "w")

	paragraphs_bi = bi.readlines()
	question_count = 0
	order = ["ก", "ข", "ค", "ง"]
	for i in range(len(paragraphs_bi)):
		sentences = literal_eval(paragraphs_bi[i])
		for sentence in sentences:
			for tp in sentence:
				question_count += 1
				(question, answer, choices) = tp
				inq.write(str(question_count) + ") " + question + "\n")
				inq.write("(คำตอบ: " + str(answer) + ")\n")
				inq.write("ประเมินคำถาม: [    ] \n")
				for i in range(0, 4):
					if i != 0:
						inq.write("\t")
					if str(choices[i]) != str(answer):
						inq.write("[   ] ")
					inq.write(order[i] + ". " + str(choices[i]))
				# inq.write("[   ] ก. " + str(choices[0]))
				# inq.write("\t[   ] ข. " + str(choices[1]))
				# inq.write("\t[   ] ค. " + str(choices[2]))
				# inq.write("\t[   ] ง. " + str(choices[3]) + "\n")
				
				# choice_count = 0
				# for choice in choices:
				# 	inq.write("__ " + str(choice) + " \t ")
				# 	choice_count += 1
				# 	if choice_count % 3 == 0:
				# 		inq.write("\n")
				# 		if choice_count >= 9: break

				# inq.write("\n\n----------------------------------\n\n")
				inq.write("\n\n")

	bi.close()
	inq.close()

def sentence_first_pos(sentence_file, pos_file, to_write):
	sen_file = open(sentence_file)
	pos_file = open(pos_file)
	out_file = open(to_write, "w")

	paragraphs = sen_file.readlines()
	para_pos = pos_file.readlines()

	for i in range(len(paragraphs)):
		sentences = literal_eval(paragraphs[i])
		pos_list = literal_eval(para_pos[i])
		for j in range(len(sentences)):
			(first_word, first_pos) = pos_list[j][0]
			out_file.write(first_pos + " " + first_word + " " + str(len(pos_list[j])) + ": " + sentences[j] + "\n")
		out_file.write("--------------------------------------\n\n")

	sen_file.close()
	pos_file.close()
	out_file.close()

if __name__ == "__main__":
	# sentence_gen("sun/sun-cut.sen.bi", "sun/sun-cut.sen.tri", "sun/sentence")
	question_gen("globalwarming/globalwarming-cut.quest.bi", "globalwarming/question")
	# sentence_first_pos("genetics/genetics.sen.bi", "genetics/genetics.pos.bi", "genetics/first.pos")
