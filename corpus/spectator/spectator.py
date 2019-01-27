
from lit.corpus import Corpus
from lit.text import Text
import os

class Spectator(Corpus):
	TEXT_CLASS=Text
	PATH_TXT = 'spectator/_txt_spectator'
	PATH_XML = 'spectator/_xml_spectator'
	PATH_METADATA = 'spectator/corpus-metadata.Spectator.txt'

	def __init__(self):
		super(Spectator,self).__init__('Spectator',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
