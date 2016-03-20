
import json
import requests

class translator:

	def __init__(self):
		self.trans = dict()
		self.read_translation_file("choices/wordnet/translation/th-en.trans", "th", "en")
		self.read_translation_file("choices/wordnet/translation/en-th.trans", "en", "th")
		self.custom_dict = dict()

	def set_custom_dict(self, custom_dict):
		self.custom_dict = custom_dict

	def read_translation_file(self, filename, source, target):
		if source not in self.trans:
			self.trans[source] = dict()
		self.trans[source][target] = dict()
		self.trans[source][target]["#filename"] = filename

		with open(filename, "r") as f:
			for line in f:
				(source_word, target_word) = line.strip().split("^")
				self.trans[source][target][source_word] = target_word

	def translate(self, words, source, target, indexes=None):
		trans_results = []
		unknon_words = []
		unknown_list_index = []

		for i in range(len(words)):
			word = words[i]
			if indexes != None and indexes[i] in self.custom_dict:
				trans_results.append((word, self.custom_dict[indexes[i]]))
			elif word in self.trans[source][target]:
				trans_results.append((word, self.trans[source][target][word]))
			else:
				trans_results.append(None)
				unknon_words.append(word)
				unknown_list_index.append(len(trans_results)-1)

		# for unknown words
		if len(unknon_words) > 0:
			meanings = self.Google_translate(unknon_words, source, target)
			f = open(self.trans[source][target]["#filename"], "a")
			for i in range(len(meanings)):
				(src_word, tgt_word) = meanings[i]
				
				# delete an article in tgt_word
				if tgt_word[0:4] == "the ": tgt_word = tgt_word[4:]
				elif tgt_word[0:3] == "an ": tgt_word = tgt_word[3:]
				elif tgt_word[0:2] == "a ": tgt_word = tgt_word[2:]

				f.write(src_word + "^" + tgt_word + "\n")
				self.trans[source][target][src_word] = tgt_word
				trans_results[unknown_list_index[i]] = meanings[i]
			f.close()

		return trans_results

	def Google_translate(self, words, source, target):
		if len(words) == 0:
			return None
		
		trans_results = []
		words_copy = words[:]
		while len(words_copy) > 0:
			req_link = "https://www.googleapis.com/language/translate/v2?key=AIzaSyBVJW-BmJ7J53EyfN0IFS6Rrrd4H3Xyhg8&source=%s&target=%s" % (source, target)
			
			words_tmp = []
			while len(words_copy) > 0 and len(req_link) < 250:
				req_link += ("&q=" + words_copy[0])
				words_tmp.append(words_copy[0])
				del words_copy[0]

			r = requests.get(req_link)
			results = r.json()
			trans = results["data"]["translations"]

			for i in range(len(words_tmp)):
				tp = (words_tmp[i], trans[i]["translatedText"])
				trans_results.append(tp)
				
		return trans_results

if __name__ == "__main__":
	# words = ["wolf", "normal", "ordinary", "monday"]
	# trans_results = Google_translate(words)
	# print(trans_results
	trans = translator()
	print(trans.translate(["cat", "forest", "ocean"], "en", "th"))
	print(trans.translate(["โลก", "มะนาว", "สะพาน"], "th", "en"))
	print(trans.trans)

