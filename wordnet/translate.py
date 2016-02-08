
import json
import requests

def Google_translate(words, source_lang="en", target_lang="th"):
	if len(words) == 0:
		return None
	
	req_link = "https://www.googleapis.com/language/translate/v2?key=AIzaSyBVJW-BmJ7J53EyfN0IFS6Rrrd4H3Xyhg8&source=%s&target=%s" % (source_lang, target_lang)
	
	for word in words:
		req_link += ("&q=" + word)

	print(req_link)

	r = requests.get(req_link)
	results = r.json()
	trans = results["data"]["translations"]

	trans_results = []
	for i in range(len(words)):
		tp = (words[i], trans[i]["translatedText"])
		trans_results.append(tp)

	return trans_results

if __name__ == "__main__":
	words = ["wolf", "normal", "ordinary", "monday"]
	trans_results = Google_translate(words)
	print(trans_results)

