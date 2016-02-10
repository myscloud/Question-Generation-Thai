
class wordnet_tree():

	def __init__(self):
		self.ndata = self.read_data()
		self.nindex = self.read_index()

	def read_data(self, data_file="wordnet/dbfiles/data.noun"):
		ndata = dict() # noun data (use same index as in data.noun)

		with open(data_file, "r") as f:
			for line in f:
				if line[0:1] != ' ':  # if this line is not a comment line
					tokens = line.strip().split(" ")

					# all states: index, words, relations, gloss
					state = "index"
					count = 0
					no_of_list = 0

					# initialize value
					index = 0
					words = []
					d = dict()
					d["formatted"] = ""
					d["hyper"] = []
					d["hypo"] = []
					d["in_hyper"] = []
					d["in_hypo"] = []
					
					for i in range(len(tokens)):
						if state == "index":
							if count == 0: index = tokens[i]
							elif count == 2:
								state = "words"
								count = -1
						elif state == "words":
							if count == 0:
								# print(index, tokens[i])
								no_of_list = int(tokens[i], 16)
							elif count%2 == 1:
								words.append(tokens[i])
							elif count == (no_of_list*2):
								d["formatted"] = ", ".join(words)
								state = "relations"
								count = -1
						elif state == "relations":
							if count == 0:
								no_of_list = int(tokens[i])
							elif count % 4 == 1:
								relation = tokens[i]
								rel_idx = tokens[i+1]

								if relation == "@": d["hyper"].append(rel_idx)
								elif relation == "~": d["hypo"].append(rel_idx)
								elif relation == "@i": d["in_hyper"].append(rel_idx)
								elif relation == "~i": d["in_hypo"].append(rel_idx)
							elif count == (no_of_list*4):
								state = "gloss"
								count = -1
						elif state == "gloss":
							break

						count += 1

					ndata[index] = d

		return ndata

	def read_index(self, index_file="wordnet/dbfiles/index.noun"):
		nindex = dict()

		with open(index_file, "r") as f:
			for line in f:
				if line[0:1] != ' ':  # if this line is not a comment line
					tokens = line.strip().split(" ")
					word = tokens[0]
					no_of_sense = int(tokens[2])
					no_of_rel = int(tokens[3])
					sense_start_idx = 6 + no_of_rel
					nindex[word] = tokens[sense_start_idx:]

		return nindex

	def get_index(self, word):
		pword = word.replace(" ", "_").lower()
		if pword in self.nindex:
			return self.nindex[pword][0] # return first sense of the word
		else:
			return None

	def get_hypernym(self, word, level=1, index=False):
		curr_index = self.get_index(word)
		if curr_index == None:
			return None, None

		attr = ""
		for i in range(level):
			if len(self.ndata[curr_index]["hyper"]) > 0:
				curr_index = self.ndata[curr_index]["hyper"][0]
			elif i == 0 and len(self.ndata[curr_index]["in_hyper"]) > 0:
				curr_index = self.ndata[curr_index]["in_hyper"][0]
				attr = "in_"
			else:
				return None

		hypernym = self.ndata[curr_index]["formatted"] if not index else curr_index
		return hypernym, attr

	def get_all_hypernym(self, word, reverse=False):
		curr_index = self.get_index(word)
		if curr_index == None:
			return None

		hypernyms_index = [curr_index]
		first = True
		while True:
			if len(self.ndata[curr_index]["hyper"]) > 0:
				curr_index = self.ndata[curr_index]["hyper"][0]
			elif first and len(self.ndata[curr_index]["in_hyper"]) > 0:
				curr_index = self.ndata[curr_index]["in_hyper"][0]
			else:
				break

			hypernyms_index.append(curr_index)
			first = False

		hypernyms = [self.ndata[index]["formatted"] for index in hypernyms_index]
		if reverse: 
			hypernyms.reverse()
		return hypernyms

	def get_siblings(self, word, level=1):
		query_word_index = self.get_index(word)
		hypernym_index, attr = self.get_hypernym(word, level=level, index=True)
		if hypernym_index == None:
			return []

		siblings_index = []
		queue = [(hypernym_index, 0)]
		attr = attr + "hypo"

		while len(queue) > 0:
			(word_index, word_level) = queue[0]
			if word_level == level:
				if word_index != query_word_index:
					siblings_index.append(word_index)
			else:
				for child_index in self.ndata[word_index][attr]:
					queue.append((child_index, word_level+1))

			del queue[0]

		siblings = [self.ndata[word_index]["formatted"] for word_index in siblings_index]
		return siblings


if __name__ == "__main__":
	wnt = wordnet_tree()

	while True:
		word = input("Enter word: ")
		if word == "quit": break
		print(wnt.get_siblings(word))

