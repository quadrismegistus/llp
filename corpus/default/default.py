
from llp.corpus import Corpus
import os
from llp.text import Text

class TextPlainTextCorpus(Text):
	pass

class PlainTextCorpus(Corpus):
	TEXT_CLASS=TextPlainTextCorpus

	def __init__(self, PATH_TXT=None, PATH_METADATA=None, PATH_ROOT=None, name=None):
		self.PATH_TXT=os.path.abspath(PATH_TXT) if PATH_TXT else None
		self.PATH_METADATA=os.path.abspath(PATH_METADATA) if PATH_METADATA else None
		self.PATH_ROOT=os.path.split(PATH_TXT)[0] if PATH_TXT else None
		super(PlainTextCorpus,self).__init__(
						'PlainTextCorpus' if not name else name,
						path_txt=self.PATH_TXT,
						path_metadata=self.PATH_METADATA,
						ext_txt='.txt')
		self.path = self.PATH_ROOT
