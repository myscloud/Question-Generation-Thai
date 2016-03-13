
import subprocess
import os
import os.path
import shutil

class word_processing:

	def __init__(self):
		self.cwd = os.path.dirname(os.path.realpath(__file__))
		self.dict_dir = self.cwd + "/tools/"

		self.special = {
			' ': '<space>',
			'-': '<minus>',
			'(': '<left_parenthesis>',
			')': '<right_parenthesis>',
			'*': '<asterisk>',
			'.': '<full_stop>',
			'"': '<quotation>',
			'/': '<slash>',
			':': '<colon>',
			'=': '<equal>',
			',': '<comma>',
			';': '<semi_colon>',
			'<': '<less_than>',
			'>': '<greater_than>',
			'&': '<ampersand>',
			'{': '<left_curly_bracket>',
			'}': '<right_curly_bracket>',
			"'": '<apostrophe>',
			'+': '<plus>',
			'?': '<question_mark>',
			'!': '<exclamation>',
			'$': '<dollar>',
			'%': '<percent>'
		}


	def word_segment(self, sentence, dict="lexitron_original.txt"):
		# dict file
	    if os.path.exists(self.dict_dir + 'lexitron.txt'):
	    	os.remove(self.dict_dir + 'lexitron.txt')
	    shutil.copyfile(self.dict_dir + dict, self.dict_dir + 'lexitron.txt')

	    f = open(self.dict_dir + 'tmp_sentence', 'w')
	    f.write(sentence)
	    f.close()

	    proc = subprocess.Popen(['java', 'LongLexTo', 'tmp_sentence'], cwd=self.dict_dir, stdout=subprocess.PIPE)


	    results = proc.stdout.read()
	    uni_results = results.decode('utf-8').strip()
	    words = uni_results.split('\n')

	    os.remove(self.dict_dir + 'tmp_sentence')
	    # for word in words:
	    # 	print(word, end=" / ")
	    # print("\n=====================")
	    return words

	def clean_special_characters(self, st):
		sentence = [ word for word in st ]
		word_count = len(sentence)
		for i in range(word_count):
			if sentence[i] in self.special:
				sentence[i] = self.special[sentence[i]]

		return sentence



