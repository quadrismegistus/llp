# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import os,codecs,re
from llp.corpus import Corpus
from llp.text import Text
from llp import tools



################
## 1. Text class
################

class TextTOO(Text):
	@property
	def meta_by_file(self):
		"""
		This function looks into the XML of the file, if there is any, and returns a dictionary of metadata.
		Please make sure to include the id of the text
		"""
		md={}
		md['id']=self.id

		#...
		#import bs4
		#dom=bs4.BeautifulSoup(self.text_xml,'lxml')
		#...
		#

		return md


	def text_plain(self, force_xml=None):
		"""
		This function returns the plain text file. You may want to modify this.
		"""

		# Return plain text version if it exists
		if self.exists_txt: return self.text_plain_from_txt()

		# Otherwise, load from XML?
		# ...

		return ''





##################
## 2. Corpus class
##################



class TOO(Corpus):
	TEXT_CLASS=TextTOO
	EXT_XML='.xml'
	EXT_TXT='.txt'

	def __init__(self):
		super(TOO,self).__init__('TOO')
		self.path = os.path.dirname(__file__)
