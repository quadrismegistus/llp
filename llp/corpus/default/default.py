from __future__ import absolute_import

from llp.corpus import Corpus
import os
from llp.text import Text

class TextPlainTextCorpus(Text):
	"""
	A default text class, useful for customization
	of the most important methods from the root Text class
	"""

	def get_metadata(self):
		meta=super().get_metadata()
		meta['wee!']='weeeeeee'
		return meta



class PlainTextCorpus(Corpus):
	TEXT_CLASS=TextPlainTextCorpus
	pass
