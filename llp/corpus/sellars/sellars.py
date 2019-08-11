from __future__ import absolute_import
import os
from llp.corpus import Corpus
from llp.text import Text

class TextSellars(Text):
	@property
	def medium(self):
		if self.genre in {'Drama'}:
			return 'Unknown'
		elif self.genre in {'Poetry'}:
			return 'Verse'
		else:
			return 'Prose'


class Sellars(Corpus):
	TEXT_CLASS=TextSellars
	PATH_TXT = 'sellars/_txt_sellars'
	PATH_XML = None
	PATH_METADATA = 'sellars/corpus-metadata.Sellars.xls'

	def __init__(self):
		super(Sellars,self).__init__('Sellars',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
		self.ext_txt='.txt.gz'
