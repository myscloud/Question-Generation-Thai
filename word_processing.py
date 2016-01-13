
import subprocess
import os
import shutil

class word_processing:

	def __init__(self):
		self.cwd = os.path.dirname(os.path.realpath(__file__))
		self.lexto_dir = self.cwd + "/LongLexTo/"

	def word_segment(self, sentence, dict="lexitron_original.txt"):
		# dict file
	    os.remove(self.lexto_dir + 'lexitron.txt')
	    shutil.copyfile(self.lexto_dir + dict, self.lexto_dir + 'lexitron.txt')

	    f = open(self.lexto_dir + 'tmp_sentence', 'w')
	    f.write(sentence)
	    f.close()

	    proc = subprocess.Popen(['java', 'LongLexTo', 'tmp_sentence'], cwd=self.lexto_dir, stdout=subprocess.PIPE)


	    results = proc.stdout.read()
	    uni_results = results.decode('utf-8').strip()
	    words = uni_results.split('\n')

	    os.remove(self.lexto_dir + 'tmp_sentence')

	    return words
