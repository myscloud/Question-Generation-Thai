import re
from os import listdir
from os.path import isfile, join

import sys

class wordnet_tree():

	def __init__(self):
		self.sense_tree = []
		self.word_list = dict()

		self.nounfiles = list()
		self.read_corpus()

	def read_corpus(self, dbpath="dbfiles"):
		allfiles = [f for f in listdir(dbpath) if isfile(join(dbpath, f))]
		self.nounfiles = [f for f in allfiles if re.match(r"noun\..+", f)]
		current_idx = 0

		# read into sense_tree and word_list
		for f in self.nounfiles:
			with open(join(dbpath, f), "r") as noun_info:
				for line in noun_info:
					words, relations, definition = self.extract_word_info(line)
					if words != None:
						d = dict()
						d["words"] = words
						d["hype"] = None
						d["class"] = None
						d["hypo"] = []
						d["inst"] = []
						d["fname"] = f
						# d["readable_words"] = ", ".join(self.read_word(word) for word in words)
						
						for tp in relations:
							if tp[1] == "@": #hypernym
								d["hype"] = tp[0]
							elif tp[1] == "@i":
								d["class"] = tp[0]

						self.sense_tree.append(d)

						for word in words:
							real_word = self.read_word(word)

							if real_word not in self.word_list:
								self.word_list[real_word] = []

							tp = (f, word, current_idx)
							self.word_list[real_word].append(tp)

						current_idx += 1

		# add hypernym and hyponym (+instance)
		for i in range(len(self.sense_tree)):
			sense = self.sense_tree[i]
			relations = [("hype", "hypo"), ("class", "inst")]
			for tp in relations:
				rel = tp[0]
				results = tp[1]
				
				if sense[rel] != None:
					rel_idx = self.find_relword_idx(sense[rel], sense["fname"])
					if rel_idx != None:
						sense[rel] = rel_idx
						self.sense_tree[rel_idx][results].append(i)

		f = open("test/sense_tree", "w")
		for i in range(len(self.sense_tree)):
			f.write(str(i) + " " + str(self.sense_tree[i]) + "\n")
		f.close()

	def get_hypernym(self, word, level=1):
		if word in self.word_list:
			(_, _, idx) = self.word_list[word][0]
			hype_idx = self.sense_tree[idx]["hype"]
			if hype_idx != None:
				return self.get_full_word(self.sense_tree[hype_idx]["words"])

	def get_siblings(self, word):
		if word in self.word_list:
			(_, _, idx) = self.word_list[word][0]
			hype_idx = self.sense_tree[idx]["hype"]
			siblings = []

			if hype_idx != None:
				for sib in self.sense_tree[hype_idx]["hypo"]:
					siblings.append(self.get_full_word(self.sense_tree[sib]["words"]))

			return siblings


	def get_hyponyms(self, word):
		pass

	def get_full_word(self, words):
		return ", ".join(self.read_word(word) for word in words)


	def extract_word_info(self, line):
		words = []
		relations = []
		definition = ""
		square_bracket = 0
		bracket = 0

		line = line.strip()
		if line[0:1] == "{" and line[-1:] == "}":
			pieces = line.split(" ")

			for token in pieces:
				if token[0:1] == "(": bracket += 1
				#########

				if token == "[" or token[0:1] == "[": square_bracket += 1
				elif token == "]" or token[-1:] == "]": square_bracket -= 1
				elif token == "{" or token == "}":
					pass
				elif token[-1:] == ",":
					if bracket > 0:
						definition += (" " + token)
					else:
						words.append(token[:-1].lower())
				elif "," in token and square_bracket == 0 and bracket == 0:
					(word, relation) = token.split(",")
					tp = (word, relation)
					relations.append(tp)
				elif bracket > 0:
					definition += (" " + token)

				#########
				if token[-1:] == ")": bracket -= 1

		else:
			return None, None, None

		return words, relations, definition[2:-1]

	def read_word(self, word):
		hasDigit = any(char.isdigit() for char in word)
		if hasDigit:
			if '"' in word:
				new_word = word.replace('"', '')
			else:
				new_word = ""
				for c in word:
					new_word += "" if c.isdigit() else c
		else:
			new_word = word

		new_word = new_word.lower()
		return new_word.replace("_", " ")

	def find_relword_idx(self, word, fname):
		rel_fname = fname
		rel_word = word
		
		if ":" in word:
			rel_fname, rel_word = word.split(":")

		rel_word = rel_word.lower()
		real_word = self.read_word(rel_word)

		if real_word in self.word_list:
			for tp in self.word_list[real_word]:
				if rel_fname == tp[0] and rel_word == tp[1]: # return index
					return tp[2]

			# print(rel_fname, rel_word, self.word_list[real_word])
		
		return None



if __name__ == "__main__":
	wnt = wordnet_tree()
	while True:
		word = input("Enter word: ")
		if word == "quit":
			break
		print(wnt.word_list[word])


