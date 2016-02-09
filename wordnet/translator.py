
import json
import requests

class translator:

	def __init__(self):
		self.trans = dict()
		self.read_translation_file("translation/th-en.trans", "th", "en")
		self.read_translation_file("translation/en-th.trans", "en", "th")


	def read_translation_file(self, filename, source, target):
		if source not in self.trans:
			self.trans[source] = dict()
		self.trans[source][target] = dict()
		self.trans[source][target]["#filename"] = filename

		with open(filename, "r") as f:
			for line in f:
				(source_word, target_word) = line.strip().split("^")
				self.trans[source][target][source_word] = target_word

	def translate(self, words, source, target):
		trans_results = []
		unknon_words = []
		unknown_list_index = []

		for word in words:
			if word in self.trans[source][target]:
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
				tp = meanings[i]
				f.write(tp[0] + "^" + tp[1] + "\n")
				self.trans[source][target][tp[0]] = tp[1]
				trans_results[unknown_list_index[i]] = tp
			f.close()

		return trans_results

	def Google_translate(self, words, source, target):
		if len(words) == 0:
			return None
		
		req_link = "https://www.googleapis.com/language/translate/v2?key=AIzaSyBVJW-BmJ7J53EyfN0IFS6Rrrd4H3Xyhg8&source=%s&target=%s" % (source, target)
		
		for word in words:
			req_link += ("&q=" + word)

		r = requests.get(req_link)
		results = r.json()
		trans = results["data"]["translations"]

		trans_results = []
		for i in range(len(words)):
			tp = (words[i], trans[i]["translatedText"])
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

