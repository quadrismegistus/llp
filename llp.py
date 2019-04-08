import os,codecs
import tools

ROOT = os.path.dirname(os.path.realpath(__file__))
SPELLING_VARIANT_PATH=os.path.join(ROOT,'data/spelling_variants_from_morphadorner.txt')






### FUNCTIONS

from corpus import load_corpus, corpora


## Spelling
V2S = None
def variant2standard():
	global V2S
	if not V2S:
		V2S = dict((d['variant'],d['standard']) for d in tools.tsv2ld(SPELLING_VARIANT_PATH,header=['variant','standard','']))
	return V2S

def standard2variant():
	v2s=variant2standard()
	d={}
	for v,s in v2s.items():
		if not s in d: d[s]=[]
		d[s]+=[v]
	return d



def phrase2variants(phrase):
	s2v=standard2variant()
	words = phrase.split()
	word_opts = [[s]+s2v[s] for s in words]
	word_combos = list(pystats.product(*word_opts))
	phrase_combos = [' '.join(x) for x in word_combos]
	return phrase_combos
###




ENGLISH = None
def load_english():
	global ENGLISH
	print '>> loading english dictionary...'
	ENGLISH = set(codecs.open('/Dropbox/LITLAB/TOOLS/english.txt','r','utf-8').read().split('\n'))
	#ENGLISH = (eng - load_stopwords())
	return ENGLISH
