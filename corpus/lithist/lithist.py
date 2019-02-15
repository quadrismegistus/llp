
from llp.corpus import Corpus
from llp.text import Text
import os

class LitHist(Corpus):
	TEXT_CLASS=Text
	PATH_TXT = 'lithist/_txt_lithist'
	PATH_XML = 'lithist/_xml_lithist'
	PATH_METADATA = 'lithist/corpus-metadata.LitHist.txt'

	def __init__(self):
		super(LitHist,self).__init__('LitHist',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
