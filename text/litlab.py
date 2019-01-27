# -*- coding: utf-8 -*-

import codecs

from lit.text import Text

class TextLitLab(Text):
	
	def text_plain_from_xml(self):
		doc=[]
		for sentence in self.dom('sentence'):
			sent=[]
			for token in sentence('word'):
				tok=token.text
				tok=tok.replace('-LSB-','[').replace('-RSB-',']').replace('-LRB-','(').replace('-RRB-',')').replace('``','"').replace("''",'"')
				sent+=[tok]
			doc+=[sent]
		return '\n'.join(' '.join([w for w in sent]) for sent in doc)

	def lines_txt(self):
		sentence=[]
		for line in self.lines_xml():
			if '<sentence ' in line and sentence:
				yield ' '.join(sentence)
				sentence=[]
			if '<word>' in line:
				word=line.split('<word>')[1].split('</word>')[0]
				sentence+=[word]

		if sentence:
			yield ' '.join(sentence)