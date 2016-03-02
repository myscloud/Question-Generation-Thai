from html.parser import HTMLParser
import urllib.request

import sys

class WikipediaParser(HTMLParser):
	def __init__(self):
		super().__init__()
		self.paragraphs = []
		self.current_string = ""
		self.readable = False
		self.current_div = []
		self.in_p_li = False

	def reset_paragraphs(self):
		self.paragraphs = []

	def get_paragraphs(self):
		return self.paragraphs

	def handle_starttag(self, tag, attrs):
		if tag == "div":
			content = False
			for attr in attrs:
				if attr[0] == "id" and attr[1] == "mw-content-text":
					content = True
			self.current_div.append(content)
		elif (tag == "p" or tag == "li") and self.current_div[-1] == True:
			self.readable = True
			self.current_string = ""
			self.in_p_li = True
		elif tag == "sup" and self.in_p_li:
			self.readable = False

	def handle_endtag(self, tag):
		if tag == "div":
			self.current_div.pop()
		elif (tag == "p" or tag == "li") and self.current_div[-1] == True:
			self.readable = False
			if self.current_string != "":
				self.paragraphs.append(self.current_string)
			self.current_string = ""
			self.in_p_li = False
		elif tag == "sup" and self.in_p_li:
			self.readable = True
	
	def handle_data(self, data):
		if self.readable:
			self.current_string += data
		elif data == "แหล่งข้อมูลอื่น":
			self.current_div[-1] = False

	def handle_startendtag(self, tag, attrs):
		pass


if __name__ == "__main__":
	args = sys.argv
	parser = WikipediaParser()
	f = open(args[1])
	html = f.readlines()
	for line in html:
		parser.feed(line.strip())
	f.close()
	
	paragraphs = parser.get_paragraphs()
	f = open(args[2], "w")
	for paragraph in paragraphs:
		f.write(paragraph + "\n")
	f.close()

	# parser.feed('<html><head><title>Test</title></head>'
 #            '<body><h1>Parse me!</h1><br /><p>abc</p></body></html>')
