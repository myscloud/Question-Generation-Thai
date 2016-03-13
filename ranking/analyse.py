
from math import ceil, floor
import matplotlib.pyplot as plt
import preprocess.orchid_corpus as orchid_corpus

def question_analyse(test_set):
	good_question_count = 0
	choice_count = 0
	for question in test_set:
		score = question.get_average_eval()
		if score >= 2.0:
			good_question_count += 1

	question_count = len(test_set)

	# plot graph
	sizes = [(good_question_count / question_count), (question_count - good_question_count) / question_count]
	labels = ["Good questions", "Bad questions"]
	colors = ['palegreen', 'indianred']
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', startangle=90)
	plt.axis("equal")

	plt.show()

def analyse_question(function_name, test_set):
	labeled_value = {"good": [], "bad": []}

	for question in test_set:
		called_func = getattr(question, function_name)
		value = called_func()
		# print(question.answer.eng_word, value)
		if question.get_average_eval() >= 2.0:
			labeled_value["good"].append(value)
		else:
			labeled_value["bad"].append(value)
	return labeled_value

def question_prev_pos(test_set):
	labeled_value = analyse_question("get_prev_pos", test_set)
	plot_histogram(labeled_value["good"], labeled_value["bad"],\
		x_label="part of speech")

def question_next_pos(test_set):
	labeled_value = analyse_question("get_next_pos", test_set)
	plot_histogram(labeled_value["good"], labeled_value["bad"],\
		x_label="part of speech",\
		graph_name="Compared to POS of word next to the answer")

def question_first_pos(test_set):
	labeled_value = analyse_question("get_first_pos", test_set)
	plot_histogram(labeled_value["good"], labeled_value["bad"],\
		x_label="part of speech",\
		graph_name="Compared to POS of the first word in a sentence")

def question_wordnet_height(test_set):
	labeled_value = analyse_question("get_wordnet_height", test_set)
	max_value = max(labeled_value["good"] + labeled_value["bad"])
	plot_histogram(labeled_value["good"], labeled_value["bad"],
		x_range=list(range(0, max_value+1)),
		x_label="wordnet height",
		graph_name="Question acceptability compared with wordnet height of the answer")

def question_answer_freq_in_sentence(test_set):
	labeled_value = analyse_question("get_answer_freq_in_sentence", test_set)
	max_value = max(labeled_value["good"] + labeled_value["bad"])
	plot_histogram(labeled_value["good"], labeled_value["bad"],\
		x_range=list(range(1, max_value+1)), x_label="frequence of answer",
		graph_name="Compared to frequency of answer in the sentence")

def question_answer_freq_in_article(test_set):
	article = []
	last_idx = -1
	for question in test_set:
		if question.sentence_no != last_idx:
			article.extend([word for word, pos in question.sentence.pos])
			last_idx = question.sentence_no

	labeled_value = {"good": [], "bad": []}
	max_value = 0
	for question in test_set:
		frequency_count = article.count(str(question.answer))
		max_value = max(max_value, frequency_count)
		if question.get_average_eval() >= 2.0:
			labeled_value["good"].append(frequency_count)
		else:
			labeled_value["bad"].append(frequency_count)

	plot_histogram(labeled_value["good"], labeled_value["bad"],
		x_range=list(range(1, max_value+1)),
		x_label="frequency of answer",
		graph_name="Compared to frequency of answer in the article")

def question_orchid(test_set):
	labeled_value = {"good": [], "bad": []}
	orchid = orchid_corpus.orchid_corpus()

	for question_item in test_set:
		known_word_count = sum([orchid.exists(word[0]) for word in question_item.sentence.pos])
		known_ratio = (known_word_count/len(question_item.sentence.pos)) * 100
		if question_item.get_average_eval() >= 2.0:
			labeled_value["good"].append(known_ratio)
		else:
			labeled_value["bad"].append(known_ratio)

	plot_histogram(labeled_value["good"], labeled_value["bad"],
		x_range=(0, 100), bins_count=10,
		x_label="ratio of known words (in orchid)",
		graph_name="Question acceptability compared with ratio of known words in orchid")

def question_sentence_length(test_set):
	labeled_value = analyse_question("get_word_count", test_set)
	max_length = max(max(labeled_value["good"]), max(labeled_value["bad"]))
	plot_histogram(labeled_value["good"], labeled_value["bad"],\
	 x_range=(0, max_length+1), bins_count=10,\
	 x_label="number of words in a sentence",\
	 graph_name="question -> number of words in the question sentence")

def question_answer_frequency(test_set):
	labeled_value = analyse_question("get_answer_frequency", test_set)
	max_value = max(labeled_value["good"] + labeled_value["bad"])
	plot_histogram(labeled_value["good"], labeled_value["bad"],
		x_range=(0, max_value), bins_count=10,
		x_label="frequency of the answer",
		graph_name="Question acceptability compared with frequency of the answer")

# ==============================================================================

def plot_histogram(good_data, bad_data, x_range=None, bins_count=None, x_label="", y_label="percentage of good/bad questions", graph_name="", eval_type="question"):

	if x_range != None and bins_count != None:
		processed_good_data, bins = process_continuous_data(good_data, x_range, bins_count)
		processed_bad_data, _ = process_continuous_data(bad_data, x_range, bins_count)
	else:
		is_bin_sorted = True
		if x_range == None:
			x_range = list(set(good_data + bad_data))
			is_bin_sorted = False

		processed_good_data, bins = process_discrete_data(good_data, bins=x_range, is_bin_sorted=is_bin_sorted)
		processed_bad_data, bins = process_discrete_data(bad_data, bins=bins)


	left_margin, width = 0.2, 0.3
	good_index = [(i + left_margin) for i in range(len(processed_good_data))]
	tick_index = bad_index = [(index + width) for index in good_index]
	fig, ax = plt.subplots()
	good_rects = ax.bar(good_index, processed_good_data, width, color='palegreen')
	bad_rects = ax.bar(bad_index, processed_bad_data, width, color="indianred")

	ax.set_xticks(tick_index)
	ax.set_xticklabels(bins, fontsize=10)
	ax.set_ylim(0,100)
	ax.set_yticks(list(range(0, 110, 10)))

	ax.legend((good_rects[0], bad_rects[0]), ("good " + eval_type, "bad " + eval_type))

	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)	
	ax.set_title(graph_name)

	autolabel(ax, good_rects)
	autolabel(ax, bad_rects)

	plt.show()

def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.1f' % height,
                ha='center', va='bottom')

def process_continuous_data(data, x_range, bins_count):
	(start, end) = x_range
	bins_width = ceil((end - start) / bins_count)
	bins = [(bins_width * i) for i in range(0, bins_count+1)]
	data_frequency = [0 for i in range(0, bins_count)]
	for value in data:
		index = floor((value - start) / bins_width)
		if index < len(data_frequency):
			data_frequency[index] += 1

	data_normalized = [(value / len(data)) * 100 for value in data_frequency]
	
	bins_range = []
	for i in range(bins_count-1):
		bins_range.append("[" + str(bins[i]) + "," + str(bins[i+1]) + ")")
	bins_range.append("[" + str(bins[-2]) + "," + str(bins[-1]) + "]")

	return data_normalized, bins_range

def process_discrete_data(data, bins=None, is_bin_sorted=True, allow_new_key=True):
	if bins != None:
		data_frequency = dict((item, 0) for item in bins)
	else:
		data_frequency = dict()

	new_key = []
	for value in data:
		if value in data_frequency:
			data_frequency[value] += 1
		elif allow_new_key:
			new_key.append(value)
			data_frequency[value] = 1

	# sort list if bins are not sorted yet
	if is_bin_sorted == False:
		sorted_tuples = sorted(data_frequency.items(), key=lambda x: x[1])
		data_freq_list, bins = [], []
		for key, value in sorted_tuples:
			bins.append(key)
			data_freq_list.append(value)
	else:
		data_freq_list = [data_frequency[key] for key in bins]
		for key in new_key:
			data_freq_list.insert(0, data_frequency[key])
			bins.insert(0, key)

	data_count = sum(data_freq_list)
	data_normalized = [(value/data_count)*100 for value in data_freq_list]
	return data_normalized, bins

