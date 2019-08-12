from __future__ import absolute_import
# -*- coding: utf-8 -*-
import codecs
from llp.text import Text
from llp.corpus.tcp import TextTCP

class TextEEBO_TCP(TextTCP):
	@property
	def meta_by_file(self):
		if not hasattr(self,'_meta'):
			mtxt=''
			for line in self.lines_xml():
				mtxt+=line
				if '</HEADER>' in line:
					break
			md=self.extract_metadata(mtxt)
			md['fnfn_xml']=self.fnfn
			md['id']=self.id
			md['genre'],md['medium']=self.return_genre()
			del md['notes']
			self._meta=md
		return self._meta

import os
from llp.corpus.tcp import TCP,TextSectionTCP

class EEBO_TCP(TCP):
	"""
	Steps for corpus generation
	1) Hook up path to TCP XML
	2) This is built on TextTCP class which can read metadata and text from TCP xml files
	3) gen_freqs()
	4) save_metadata()
	5) gen_mfw(year_min=1500,year_max=1699,yearbin=50)
	6) gen_freq_table()
	"""


	TEXT_CLASS=TextEEBO_TCP
	EXT_XML = '.headed.xml.gz'
	EXT_TXT='.txt.gz'
	TEXT_SECTION_CLASS=TextSectionTCP

	
