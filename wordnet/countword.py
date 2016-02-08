import re
from os import listdir
from os.path import isfile, join

def read_word(word):
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

	return new_word.replace("_", " ")

def extract_word_info(line):
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

			if token == "[": square_bracket += 1
			elif token == "]": square_bracket -= 1
			elif token == "{" or token == "}":
				pass
			elif token[-1:] == ",":
				if bracket > 0:
					definition += (" " + token)
				else:
					words.append(token[:-1])
			elif "," in token and square_bracket == 0 and bracket == 0:
				# print(line, token)
				(word, relation) = token.split(",")
				tp = (word, relation)
				relations.append(tp)
			elif bracket > 0:
				definition += (" " + token)

			#########
			if token[-1:] == ")": bracket -= 1

	else:
		return None, None, None

	clean_words = [read_word(word) for word in words]

	return clean_words, relations, definition[2:-1]


###########################################################################
# main program

# wordfile = open("noun.wordlist", "w")
# wordrelafile = open("noun.wordrela", "w")
dbpath = "dbfiles"
allfiles = [f for f in listdir(dbpath) if isfile(join(dbpath, f))]
nounfiles = [f for f in allfiles if re.match(r"noun\..+", f)]

nouns = set()
f = open("noun.wordlist")
tmp = f.readlines()
nounlist = [word.strip() for word in tmp]
f.close()

for noun in nounlist:
	nouns.add(noun)

for f in nounfiles:
	with open(join(dbpath, f), "r") as noun_info:
		for line in noun_info:
			# print(f)
			words, relations, definition = extract_word_info(line)
			if words != None:
				for relation in relations:
					w = relation[0]
					if w not in nounlist:
						print(w)

			# if words != None:
			# 	for word in words:
			# 		wordfile.write(word + "\n")
			# 		wordrelafile.write(word + " ")

			# 	wordrelafile.write("\n")

			# 	for relation in relations:
			# 		wordrelafile.write(str(relation) + " ")

			# 	wordrelafile.write("\n")

# wordfile.close()
# wordrelafile.close()