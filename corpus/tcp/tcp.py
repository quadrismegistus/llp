import os
from llp.corpus import Corpus,Corpus_in_Sections
from llp import tools
STYPE_FN=os.path.join(__file__,'data.section_types.xlsx')

class TCP(Corpus):
	STYPE_DD=None

	def sectiontype2genre(self,stype):
		if not self.STYPE_DD:
			print '>> loading stype2genre'
			self.STYPE_DD=tools.ld2dd(tools.read_ld(STYPE_FN),'section_type')
		return self.STYPE_DD.get(stype,{}).get('genre','')


def gen_section_types():
	import tools
	from llp.corpus.eebo import EEBO_TCP
	from llp.corpus.ecco import ECCO_TCP
	corpora = [EEBO_TCP(), ECCO_TCP()]

	from collections import defaultdict,Counter
	section_types=defaultdict(Counter)
	for c in corpora:
		cs=c.sections
		for d in cs.meta:
			section_types[c.name][d['section_type']]+=1

	def writegen():
		all_stypes = set([key for cname in section_types for key in section_types[cname]])
		for stype in all_stypes:
			dx={'section_type':stype}
			dx['count']=0
			for cname in section_types:
				dx['count_'+cname]=section_types[cname].get(stype,0)
				dx['count']+=dx['count_'+cname]
			yield dx

	tools.writegen('data.section_types.txt', writegen)
