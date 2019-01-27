# -*- coding: utf-8 -*-

from lit.corpus import CorpusMeta,name2corpus
from lit.corpus.tedjdh import TedJDH
import os

class Poetry(CorpusMeta):
	def __init__(self, name='Poetry'):
		tedjdh=TedJDH()
		corpora = [tedjdh]
		tedjdh._texts = [t for t in tedjdh.texts() if t.medium in ['Poetry']]

		super(Poetry,self).__init__(name=name,corpora=corpora)
		self.path=os.path.join(self.path,'poetry')
