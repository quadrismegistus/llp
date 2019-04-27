from __future__ import absolute_import
from __future__ import print_function

from llp.corpus import Corpus
from llp.text import Text
import os


class TextChicago(Text):
	pass

class Chicago(Corpus):
	TEXT_CLASS=TextChicago
	PATH_TXT = '/Users/ryan/Volumes/Oak/stacks/raw/chicago/Texts'
	PATH_XML = 'chicago/_xml_chicago'
	PATH_METADATA = 'chicago/corpus-metadata.Chicago.txt'
	FN_METADATA_CSV_AUTHORS = 'AUTHORS_METADATA.csv'
	FN_METADATA_CSV_TEXTS = 'NOVELS_METADATA.csv'
	EXT_TXT = '.txt'

	def __init__(self):
		super(Chicago,self).__init__('Chicago',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA,ext_txt=self.EXT_TXT)
		self.path = os.path.dirname(__file__)

	def gen_metadata(self):
		from llp.tools import read_ld,ld2dd,write2
		"""
		Generates a single metadata table from AUTHORS_METADATA.csv and NOVELS_METADATA.csv
		"""
		auth_ld = read_ld(os.path.join(self.path,self.FN_METADATA_CSV_AUTHORS))
		text_ld = read_ld(os.path.join(self.path,self.FN_METADATA_CSV_TEXTS))

		auth_dd = ld2dd(auth_ld,'AUTH_ID')
		for d in text_ld:
			auth_id = d['AUTH_ID']
			for k,v in list(auth_dd.get(auth_id,{}).items()): d[k]=v
			d['id']=d['FILENAME'].replace('.txt','')

			# lowercase keys
			keys=list(d.keys())
			for k in list(d.keys()):
				k2=k.lower()
				if k2!=k:
					d[k2]=d[k]
					del d[k]

			# add year and author
			d['year']=d['publ_date']
			d['author']=d['auth_last']+', '+d['auth_first']

			print(d)

		write2(self.path_metadata, text_ld)
