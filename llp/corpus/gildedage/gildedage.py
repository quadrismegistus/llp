from __future__ import absolute_import
# -*- coding: utf-8 -*-

import os

from llp.corpus import Corpus
import codecs
from llp.text import Text

class GildedAge(Corpus):
	PATH_TXT = 'gildedage/_txt_gildedage'
	PATH_METADATA='gildedage/corpus-metadata.GildedAge.xlsx'
	EXT_TXT = '.txt.gz'
	TEXT_CLASS=Text

	def __init__(self):
		super(GildedAge,self).__init__('GildedAge',path_txt=self.PATH_TXT,ext_txt=self.EXT_TXT,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
