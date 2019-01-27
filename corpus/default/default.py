
from lit.corpus import Corpus
from lit.text.default import TextPlainTextCorpus
import os

class PlainTextCorpus(Corpus):
	TEXT_CLASS=TextPlainTextCorpus

	def __init__(self, PATH_TXT, PATH_METADATA=None, PATH_ROOT=None, name=None):
		self.PATH_TXT=os.path.abspath(PATH_TXT)
		self.PATH_METADATA=os.path.abspath(PATH_METADATA) if PATH_METADATA else None
		self.PATH_ROOT=os.path.split(PATH_TXT)[0]
		super(PlainTextCorpus,self).__init__(
						'PlainTextCorpus' if not name else name,
						path_txt=self.PATH_TXT,
						path_metadata=self.PATH_METADATA,
						ext_txt='.txt')
		self.path = self.PATH_ROOT
