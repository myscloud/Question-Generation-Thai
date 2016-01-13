
import os

class orchid_corpus:

	def __init__(self, file_name="/corpus/orchid97.txt"):
		cwd = os.path.dirname(os.path.realpath(__file__))
		self.orchid = cwd + file_name
		self.corpus = list()
		self.corpus_pos = list()
		self.corpus_sentence = list()
		self.read_from_corpus()

		self.word_list = set()
		self.pos_list = set()
		self.get_word_pos_list()

	def read_from_corpus(self):
		corpus_file = open(self.orchid, "r")
		corpus = corpus_file.readlines()
		corpus_file.close()

		state = "init"
		sentences = []
		words = []

		# read to corpus

		for line in corpus:
			line = line.strip()

			if state == "init":
				if line[0:7] == "%TTitle":
					state = "book"
				elif line[0] == '#' and line[1] == 'P':
					state = "paragraph"
				elif line[0] == '#':
					state = "sentence"

			elif state == "book":
				if line[0] == '#' and line[1] == 'P':
					state = "paragraph"

			elif state == "paragraph":
				if len(sentences) > 0:
					self.corpus.append(sentences)
				sentences = []
				state = "sentence"

			elif state == "sentence":
				if "//" in line:
					if line[0:2] == "%E":
						state = "init"
					else:
						words = []
						state = "word"
				elif line[0:2] == "%E":
					state = "eng"

			elif state == "eng":
				if "//" in line:
					state = "init"

			elif state == "word":
				if "//" in line:
					state = "init"
					sentences.append(words)
				else:
					(word, pos) = line.split('/')
					words.append( (word, pos) )

		# corpus_pos

		for paragraph in self.corpus:
			for sentence in paragraph:
				self.corpus_pos.append(sentence)

		# corpus_sentence
		# add tag <SBS> = Sentence Break Space and <NSBS> = Non Sentence Break Space

		for paragraph in self.corpus:
			p = []
			for i in range(len(paragraph)):
				for word in paragraph[i]: # for each word in sentence
					if word[0] == "<space>":
						p.append( ("<space>", "NSBS") )
					else:
						p.append(word)

				if i != len(paragraph) - 1:
					p.append( ("<space>", "SBS") )

			self.corpus_sentence.append(p)		


	def get_word_pos_list(self):

		for paragraph in self.corpus:
			for sentence in paragraph:
				for word in sentence:
					self.word_list.add(word[0])
					self.pos_list.add(word[1])


	def get_corpus_pos(self):
		return self.corpus_pos


