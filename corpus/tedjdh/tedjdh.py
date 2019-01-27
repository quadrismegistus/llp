# -*- coding: utf-8 -*-

from lit.corpus import Corpus
from lit.text import Text
import os

class TedJDH(Corpus):
	TEXT_CLASS=Text
	PATH_TXT = 'tedjdh/_txt_tedjdh'
	PATH_XML = 'tedjdh/_xml_tedjdh'
	PATH_METADATA = 'tedjdh/corpus-metadata.TedJDH.xls'

	def __init__(self):
		super(TedJDH,self).__init__('TedJDH',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
