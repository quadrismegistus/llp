from __future__ import absolute_import

import llp
from llp.corpus import Corpus
from llp.text import Text
import os

"""
class LitHist(Corpus):
	TEXT_CLASS=Text
	PATH_TXT = 'lithist/_txt_lithist'
	PATH_XML = 'lithist/_xml_lithist'
	PATH_METADATA = 'lithist/corpus-metadata.LitHist.txt'

	def __init__(self):
		super(LitHist,self).__init__('LitHist',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA)
		self.path = os.path.dirname(__file__)
"""


from llp.corpus import CorpusMeta,name2corpus
import os



class LitHist(CorpusMeta):
	CORPORA=[
		'Chadwyck','ChadwyckPoetry','ChadwyckDrama',
		'ECCO-TCP','EEBO-TCP', #,'ECCO-TCP_in_Sections','EEBO-TCP_in_Sections' (too many files)
		'Sellars',   # 'TedJDH' (replicated in Sellars + ECCO-TCP)
		'DialNarr', #LitLab (too noisy),
		'MarkMark','Chicago',
		'COHA','CLMET','OldBailey','EnglishDialogues',
		'Spectator']

	def __init__(self, name='LitHist',corpora=None):
		if not corpora: corpora=[]

		for name in self.CORPORA:

			if name=='Chadwyck':
				c=llp.load_corpus(name)
				c._texts = [t for t in c.texts() if t.year>1500 and t.year<1900]
			elif name=='ChadwyckPoetry':
				c=llp.load_corpus(name)
				#c._texts = [t for t in c.texts() if t.meta['posthumous']=='False' and t.year>1500 and t.year<2000]
			elif name=='ChadwyckDrama':
				c=llp.load_corpus(name)
				#c._texts = [t for t in c.texts() if t.meta['posthumous']=='False' and t.year>1500 and t.year<2000]
			elif name=='ECCO-TCP_in_Sections':
				c=llp.load_corpus('ECCO_TCP').sections
				c._texts = [t for t in c.texts() if t.year>=1700 and t.year<1800]
			elif name=='ECCO-TCP':
				c=llp.load_corpus('ECCO_TCP')
				c._texts = [t for t in c.texts() if t.year>=1700 and t.year<1800]
			elif name=='EEBO-TCP_in_Sections':
				c=llp.load_corpus('EEBO_TCP').sections
				c._texts = [t for t in c.texts() if t.year>=1500 and t.year<1700]
			elif name=='EEBO-TCP':
				c=llp.load_corpus('EEBO_TCP')
				c._texts = [t for t in c.texts() if t.year>=1500 and t.year<1700]
			else:
				c=llp.load_corpus(name)
			#"""

			if c is not None:
				corpora.append(c)

		super(LitHist,self).__init__(name=name,corpora=corpora)
		self.path=os.path.join(self.path,'lithist')





class LitHistAuthors(CorpusMeta):
	CORPORA={'Chadwyck','ChadwyckPoetry','ChadwyckDrama','COHA','ECCO_TCP','EEBO_TCP'} #,'Sellars','CLMET','Spectator','Chicago','MarkMark'}
	YEAR_AUTHOR_30_MIN=1500

	def __init__(self, name='LitHistAuthors',corpora=None):
		if not corpora: corpora=[]

		for name in self.CORPORA:
			c=llp.load_corpus(name)
			if c is None: continue
			c._texts = [t for t in c.texts() if t.year_author_is_30>self.YEAR_AUTHOR_30_MIN]
			corpora.append(c)

		super(LitHistAuthors,self).__init__(name=name,corpora=corpora)
		self.path=os.path.join(self.path,'lithist')
