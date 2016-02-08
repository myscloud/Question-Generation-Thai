
class wordnet_tree():

	def __init__(self):
		self.ndata = self.read_data()
		self.nindex = self.read_index()

	def read_data(self, data_file="dbfiles/data.noun"):
		ndata = dict() # noun data (use same index as in data.noun)

		with open(data_file, "r") as f:
			for line in f:
				if line[0:1] != ' ':  # if this line is not a comment line
					tokens = line.strip().split(" ")

					# all states: init, words, relations, gloss
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

	def read_index(self, index_file="dbfiles/index.noun"):
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

	def get_hypernym(self, word, level=1, instance=False, index=False):
		curr_index = self.get_index(word)
		if curr_index == None:
			return None

		attr = "hyper" if not instance else "in_hyper"
		for i in range(level):
			if len(self.ndata[curr_index][attr]) > 0:
				curr_index = self.ndata[curr_index][attr][0]
			else:
				break

		return self.ndata[curr_index]["formatted"] if not index else curr_index


if __name__ == "__main__":
	wnt = wordnet_tree()

	while True:
		word = input("Enter word: ")
		if word == "quit": break
		print(wnt.get_hypernym(word, index=True))

