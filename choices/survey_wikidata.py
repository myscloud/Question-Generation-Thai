
import ast

def compare_word_list():
	wordnet = set()
	wiki = set()

	with open("wikidata/wikidata.item") as f:
		for line in f:
			word_info = ast.literal_eval(line.strip())
			(_, word, _, _, _) = word_info
			wiki.add(word.lower().replace(" ", "_"))

	with open("wordnet/dbfiles/index.noun") as f:
		for line in f:
			if line[0:1] != ' ':
				tokens = line.strip().split(" ")
				word = tokens[0]
				wordnet.add(word)

	occur_two = 0
	for word in wiki:
		if word in wordnet:
			occur_two += 1

	print("number of word in wiki: ", len(wiki))
	print("number of word in wordnet: ", len(wordnet))
	print("both occurence: ", occur_two)

def subclass_size():
	count_subclass = 0
	count_instance = 0
	with open("wikidata/wikidata.item") as f:
		for line in f:
			word_info = ast.literal_eval(line.strip())
			(_, _, _, sub, inst) = word_info
			if len(sub) > 3:
				count_subclass += 1
			if len(inst) > 1:
				count_instance += 1

	print(count_subclass, count_instance)


if __name__ == "__main__":
	# compare_word_list()
	subclass_size()