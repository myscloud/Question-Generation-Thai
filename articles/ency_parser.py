from html.parser import HTMLParser
import urllib.request

import sys

class ency_parser(HTMLParser):

	def __init__(self):
		super().__init__()
		self.in_big = False

	def handle_starttag(self, tag, attrs):
		if tag == "big":
			self.in_big = True

	def handle_data(self, data):
		if self.in_big:
			print(data)

	def handle_endtag(self, tag):
		if tag == "big":
			self.in_big	= False

def parse_ency(filename):
	parser = ency_parser()
	with open(filename) as f:
		for line in f:
			print(line)

if __name__ == "__main__":
	args = sys.argv
	if len(args) > 1:
		parse_ency(args[1])
