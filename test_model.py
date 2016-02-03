
import viterbi as vtb

def test_model(corpus):
	cp = corpus.corpus_sentence

	word_list = list()
	pos_list = list()
	
	for paragraph in cp:
		text = []
		pos = []

		for tp in paragraph:
			text.append(tp[0])
			pos.append(tp[1])

		word_list.append(text)
		pos_list.append(pos)

	initp, trans_bi, emiss = corpus.get_statistics_model(tri_gram=False)
	_, trans_tri, emiss = corpus.get_statistics_model(tri_gram=True)

	bigram_result = []
	trigram_result = []

	count = 0
	for paragraph in word_list:
		pos_bi = vtb.viterbi(paragraph, corpus.pos_list_sentence, initp, trans_bi, emiss)
		# pos_tri = vtb.viterbi_trigram(paragraph, corpus.pos_list_sentence, initp, trans_tri, emiss)

		bigram_result.append(pos_bi)
		# trigram_result.append(pos_tri)

		print(count)
		count += 1
		if count == 1000:
			break

	tp, tn, fp, fn, other = evaluate_sentence(pos_list[0:1000], bigram_result)
	write_results_to_file("test/test_model_orchid_bigram", word_list[0:1000], pos_list, bigram_result, tp, tn, fp, fn, other, test_text="bigram model test")

	# tp, tn, fp, fn, other = evaluate_sentence(pos_list[0:1000], trigram_result)
	# write_results_to_file("test/test_model_orchid_trigram", word_list[0:1000], pos_list, trigram_result, tp, tn, fp, fn, other, test_text="trigram model test")


def evaluate_sentence(origin, test):
	tp, tn, fp, fn = 0, 0, 0, 0  # true positive, true negative, false pos, false neg
	other = 0

	for i in range(len(origin)):
		for j in range(len(origin[i])):
			origin_pos = origin[i][j]
			test_pos = test[i][j]

			if origin_pos == "SBS":
				if test_pos == "SBS": tp += 1
				elif test_pos == "NSBS": fn += 1
				else: other += 1
			
			elif origin_pos == "NSBS":
				if test_pos == "SBS": fp += 1
				elif test_pos == "NSBS": tn += 1
				else: other += 1

	return tp, tn, fp, fn, other


def print_results(tp, tn, fp, fn, other=0, test_text="test"):
	print("==============================")
	print(test_text + " results: ")
	print("true positive: " + str(tp))
	print("true negative: " + str(tn))
	print("false positive: " + str(fp))
	print("false negative: " + str(fn))
	print("other: " + str(other))
	print("==============================", end="\n\n")

def write_results_to_file(filename, words, origin_pos, test_pos, tp, tn, fp, fn, other, test_text="test"):
	f = open(filename, "w")
	f.write(test_text + " results \n")
	f.write("true positive: " + str(tp) + "\n")
	f.write("true negative: " + str(tn) + "\n")
	f.write("false positive: " + str(fp) + "\n")
	f.write("false negative: " + str(fn) + "\n")
	f.write("other: " + str(other) + "\n")
	f.write("\n#############################################################################\n\n\n")

	for i in range(len(words)):
		f.write("paragraph #" + str(i+1) + "\n")
		f.write("=============================================\n")
		for j in range(len(words[i])):
			f.write(words[i][j] + " " + origin_pos[i][j] + " " + test_pos[i][j] + "\n")
		f.write("=============================================\n\n")

	f.close()




