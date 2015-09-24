#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import sgmllib
import sys

class ExtractText(sgmllib.SGMLParser):
  def __init__(self, verbose=0):
    sgmllib.SGMLParser.__init__(self, verbose)
    self.data = None

  def handle_data(self, data):
	if self.data is not None:
		text = string.split(data, '\n')
		del text[0]
		paragraph = ' '.join(text)
		print paragraph
		#self.data.append(data)

  def start_p(self, attrs):
	self.data = []

  def end_p(self):
	self.data = None


def main():
	parser = ExtractText()
	f = open(sys.argv[1])
	sgmlFile = f.read()
	parser.feed(sgmlFile)
	parser.close()

if __name__ == "__main__":
    main()
