from __future__ import absolute_import
FIELDS=None

def get_worddb_fields():
	global FIELDS
	if FIELDS: return FIELDS
	from .tools import worddb
	wdb=worddb()

	fd={}
	fd['Abs']={d['word'] for d in wdb if d['Abstract/Concrete']=='Abstract'}
	fd['AbsN']={d['word'] for d in wdb if d['Abstract/Concrete']=='Abstract' and d['pos']=='n'}
	fd['Conc']={d['word'] for d in wdb if d['Abstract/Concrete']=='Concrete'}
	fd['ConcN']={d['word'] for d in wdb if d['Abstract/Concrete']=='Concrete' and d['pos']=='n'}
	fd['NotAbs_NotConc']={d['word'] for d in wdb if d['Abstract/Concrete']=='Neither'}
	fd['ContentWord']={d['word'] for d in wdb if d['is_content_word']=='True'}
	fd['NotContentWord']={d['word'] for d in wdb if d['is_content_word']=='False'}
	fd['Name']={d['word'] for d in wdb if d['is_name']=='True'}
	fd['Verb']={d['word'] for d in wdb if d['pos']=='v'}
	fd['Noun']={d['word'] for d in wdb if d['pos']=='n'}
	fd['Adj']={d['word'] for d in wdb if d['pos']=='j'}

	FIELDS=fd
	return fd

def measure_fields(word_counts,fields={},only_fields=None):
	if not fields: fields=get_fields()
	word_types=set(word_counts.keys())

	cd={}
	for fieldname,fieldwords in list(fields.items()):
		count=0
		if only_fields and not fieldname in only_fields: continue
		for matching_word in fieldwords & word_types:
			count+=word_counts[matching_word]
		cd[fieldname]=count

	return cd

def get_fields(fnfn='/Users/ryan/DH/Dissertation/abstraction/words/data.fields.txt',only_fields={},only_pos={},word2fields={}):
	#from llp import tools
	#fd=field2words={}
	#for d in tools.readgen(fnfn):
	#	field2words[d['field']]=set(d['words'].split())
	from collections import defaultdict
	field2words=defaultdict(set)
	if only_pos: w2pos=get_word2pos()

	word2fields = get_word2fields(only_fields=only_fields) if not word2fields else word2fields

	for word,fields in list(word2fields.items()):
		if only_pos:
			pos=w2pos.get(w,'')
			if True not in [pos.startswith(x) for x in only_pos]:
				continue

		for f in fields:
			field2words[f]|={word}

	return field2words

def get_word2pos(worddb=None, word_col='word', pos_col='pos_byu'):
	from llp.tools import worddf
	df=worddf()
	return dict(zip(df[word_col],df[pos_col]))

def get_word2fields(fnfn='/Users/ryan/DH/Dissertation/abstraction/words/data.field_words.txt',
only_fields={'W2V.HGI.Abstract', 'W2V.HGI.Concrete'},
only_pos={'n','v','r','j'}):
	from llp import tools
	from collections import defaultdict
	if only_pos: w2pos=get_word2pos()

	w2f=defaultdict(list)
	for dx in tools.readgen(fnfn):
		try:
			w=dx['word']
			f=dx['field']
			if only_fields and not f in only_fields: continue

			if only_pos:
				pos=w2pos.get(w,'')
				if True not in [pos.startswith(x) for x in only_pos]:
					continue

			w2f[w]+=[f]
		except KeyError:
			pass
	return w2f


# Nicknames
#get_fields = get_worddb_fields
