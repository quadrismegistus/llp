FIELDS=None

def get_worddb_fields():
	global FIELDS
	if FIELDS: return FIELDS
	from tools import worddb
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

def measure_fields(words,fields=None):
	if not fields: fields=get_fields()

	cd={}
	for fieldname,fieldwords in fields.items():
		cd[fieldname]=len([w for w in words if w in fieldwords])

	return cd

def get_fields(fnfn='/Users/ryan/DH/Dissertation/abstraction/words/data.fields.txt'):
	import pytxt
	fd=field2words={}
	for d in pytxt.readgen(fnfn):
		field2words[d['field']]=set(d['words'].split())

	return field2words


# Nicknames
#get_fields = get_worddb_fields
