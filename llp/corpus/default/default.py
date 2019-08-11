from __future__ import absolute_import

from llp.corpus import Corpus
import os
from llp.text import Text

class TextPlainTextCorpus(Text):
	pass

class PlainTextCorpus(Corpus):
	TEXT_CLASS=TextPlainTextCorpus

	def __init__(self, path_txt=None, path_metadata=None, col_fn='fn', col_id='id', ext='.txt', path_root=None, name=None):
		self.PATH_TXT=os.path.abspath(path_txt) if path_txt else None
		self.PATH_METADATA=os.path.abspath(path_metadata) if path_metadata else None
		self.PATH_ROOT=os.path.split(path_txt)[0] if path_txt else None
		super(PlainTextCorpus,self).__init__(
						'PlainTextCorpus' if not name else name,
						path_txt=self.PATH_TXT,
						path_metadata=self.PATH_METADATA,
						ext_txt=ext,
						col_fn=col_fn,
						col_id=col_id)
		self.path = self.PATH_ROOT
