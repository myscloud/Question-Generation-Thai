
class wordnet_tree():

	def __init__(self):
		self.ndata = self.read_data()
		self.nindex = self.read_index()
		self.read_cnt_list()

	def read_data(self, data_file="choices/wordnet/dbfiles/data.noun"):
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
					d["freq"] = 0
					
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

	def read_index(self, index_file="choices/wordnet/dbfiles/index.noun"):
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

	def read_cnt_list(self, cnt_file="choices/wordnet/dbfiles/cntlist.noun"):	
		noun_freq_list = []
		with open(cnt_file, "r") as f:
			for line in f:
				(freq, word, sense) = line.strip().split(" ")
				freq = int(freq)
				sense = int(sense)
				index = self.nindex[word][sense-1]
				self.ndata[index]["freq"] = freq

	def get_index(self, word, get_all=False):
		pword = word.replace(" ", "_").lower()
		if pword in self.nindex:
			if not get_all: return self.nindex[pword][0] # return first sense of the word
			else: return self.nindex[pword]
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

	# get hypernyms (in every senses) but just for 1-level hypernym
	def get_hypernyms(self, senses_index):
		if senses_index == None:
			return None

		hypernym_index = []
		for index in senses_index:
			if len(self.ndata[index]["hyper"]) > 0:
				for ele in self.ndata[index]["hyper"]:
					hypernym_index.append((ele, "", index))
			elif len(self.ndata[index]["in_hyper"]) > 0:
				for ele in self.ndata[index]["in_hyper"]:
					hypernym_index.append((ele, "in_", index))
			else:
				pass

		return hypernym_index


	def get_all_hypernym(self, word, reverse=False, curr_index=None):
		if curr_index == None:
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

	def get_word_from_index(self, index):
		return self.ndata[index]["formatted"]

	def get_word_height(self, word, index=None):
		all_hypernym = self.get_all_hypernym(word, curr_index=index)
		if all_hypernym == None:
			return 0
		else:
			return len(all_hypernym)

	def get_siblings_one_sense(self, hypernym_index, attr, query_word_index, level=1):
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
		return siblings, siblings_index

	def get_siblings(self, word, get_all=True, index=True, word_index=None):
		if word_index == None:
			word_index = self.get_index(word, get_all=get_all)
		hypernyms_list = self.get_hypernyms(word_index)
		if hypernyms_list == None or len(hypernyms_list) == 0:
			return None, None, None

		if not get_all:
			return self.get_siblings_one_sense(word, hypernyms_list[0][0], hypernyms_list[0][1])
		else:
			hypernyms_index = []
			siblings, siblings_index = [], []
			for hyper in hypernyms_list:
				sib, sib_index = self.get_siblings_one_sense(hyper[0], hyper[1], hyper[2])
				if len(sib) > 0:
					siblings.append(sib)
					siblings_index.append(sib_index)
					hypernyms_index.append(hyper[0])
			
			if index:
				return siblings, siblings_index, hypernyms_index
			else:
				return siblings

	def get_siblings_count(self, word_index, hypernym_index):
		attr = ""
		if hypernym_index in self.ndata[word_index]["in_hyper"]:
			attr = "in_"
		attr += "hypo"
		return len(self.ndata[hypernym_index][attr])

	def get_no_of_sense(self, word):
		if word in self.nindex:
			return len(self.nindex[word])
		else:
			return None

	def process_eng_word(self, word):
		return word.replace(" ", "_").lower()

	def get_word_frequency(self, word=None, index=None, sense=0):
		if word != None and word in self.nindex and len(self.nindex[word]) > sense:
			index = self.nindex[word][sense]
			return self.ndata[index]["freq"]
		elif index != None:
			return self.ndata[index]["freq"]
		else:
			return None

	def get_word_index(self, word, sense):
		new_word = self.process_eng_word(word)
		if new_word in self.nindex and sense == None:
			return self.nindex[new_word]
		elif new_word in self.nindex and sense <= len(self.nindex[new_word]):
			return [self.nindex[new_word][sense-1]]
		else:
			return None

	def exists(self, word):
		return word in self.nindex

if __name__ == "__main__":
	wnt = wordnet_tree()

	while True:
		word = input("Enter word: ")
		if word == "quit": break
		print(wnt.get_word_from_index(word))

