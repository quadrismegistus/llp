# -*- coding: utf-8 -*-

import os,codecs,gzip
from llp import tools
nlp=None


class Text(object):
	def __init__(self,idx,corpus,path_to_xml=None,path_to_txt=None):
		self.id=idx
		self.corpus=corpus
		self._sections=[]
		self._fnfn_xml=path_to_xml
		self._fnfn_txt=path_to_txt


	@property
	def nation(self):
		return self.meta.get('nation','')

	def sections_xml(self,divider_tag,text_section_class=None):
		xml=self.text_xml
		o=[]
		for part in xml.split('<'+divider_tag)[1:]:
			part_type=part.split(' TYPE="')[1].split('"')[0]
			part='<'+divider_tag+part
			o+=[(divider_tag,text_section_class,part_type,part)]
		return o

	def get_section(self,idx):
		for s in self.sections:
			if s.id==idx:
				return s

	def load_sections(self):
		o=[]
		for i,(divider_tag,text_section_class,section_type,section_xml) in enumerate(self.sections_xml()):
			if not text_section_class: text_section_class=TextSection
			o+=[text_section_class(text=self,section_num=i+1,section_type=section_type,section_xml=section_xml,section_txt=None,divider_tag=divider_tag)]
		self._sections=o

	def unload_sections(self):
		self._sections=[]

	@property
	def sections(self):
		if not hasattr(self,'_sections') or not self._sections:
			self.load_sections()
		return self._sections

	@property
	def is_metatext(self):
		return False

	@property
	def path_xml(self): return self.fnfn_xml

	@property
	def ext_xml(self): return self.corpus.ext_xml

	@property
	def ext_txt(self): return self.corpus.ext_txt

	@property
	def fnfn(self):
		return self.fnfn_xml if self.fnfn_xml and os.path.exists(self.fnfn_xml) else self.fnfn_txt

	@property
	def fnfn_txt(self):
		if hasattr(self,'_fnfn_txt') and self._fnfn_txt: return self._fnfn_txt
		return os.path.join(self.corpus.path_txt, self.id + self.ext_txt)

	@property
	def path_txt(self): return self.fnfn_txt

	@property
	def fnfn_xml(self):
		if hasattr(self,'_fnfn_xml') and self._fnfn_xml: return self._fnfn_xml
		return os.path.join(self.corpus.path_xml, self.id + self.ext_xml)

	@property
	def fnfn_spacy(self): return os.path.join(self.corpus.path_spacy, self.id + '.bin')

	@property
	def genre(self): return self.meta.get('genre','')

	@property
	def medium(self):
		medium=self.meta.get('medium','')
		#if not medium: medium=self.meta.get('genre','')
		#if medium=='Verse': medium='Poetry'
		return medium

	@property
	def author(self): return self.meta.get('author','')

	def get_author_gender(self,name):
		# Guess
		import re
		import gender_guesser.detector as gender
		isnt_this_problematic_just_to=gender.Detector()
		genders = [isnt_this_problematic_just_to.get_gender(x) for x in re.split('\W',self.author)]
		for x in genders:
			if x!='unknown':
				return x
		return 'unknown'

	@property
	def author_gender(self):
		if 'gender' in self.meta and self.meta['gender']: return self.meta['gender']
		if 'author_gender' in self.meta and self.meta['author_gender']: return self.meta['author_gender']
		return self.get_author_gender(self.author)

	def get_is_posthumous(self,author,year):
		author_dates=self.get_author_dates(author)
		if year and author_dates[0] and year>author_dates[0]:
			if not author_dates[1]:
				if author_dates[0] > 1900: # so it's plausible they're still alive
					return False
			else: # has death date
				if year>author_dates[1]:
					return True
				else:
					return False
		return None


	@property
	def is_posthumous(self):
		return self.get_is_posthumous(self.author,self.year)



	@property
	def year(self):
		try:
			yearstr=''.join([x for x in self.meta['year'] if x.isdigit()])[:4]
			while len(yearstr)<4:
				yearstr+='0'
			return int(float(yearstr))
		except (ValueError,TypeError,KeyError) as e:
			return 0

	@property
	def title(self): return unicode(self.meta['title'])

	@property
	def decade(self): return int(self.year)/10*10

	@property
	def twentyyears(self): return int(self.year)/20*20

	@property
	def quartercentury(self): return int(self.year)/25*25

	@property
	def halfcentury(self): return int(self.year)/50*50

	@property
	def century(self): return int(self.year)/100*100

	def get_author_dates(self,author):
		return get_author_dates(self.author)

	@property
	def author_dates(self):
		if not hasattr(self,'_author_dates'): self._author_dates=get_author_dates(self.author)
		return self._author_dates



	@property
	def meta(self):
		if not hasattr(self,'_meta'):
			if os.path.exists(self.corpus.path_metadata):
				#print '>> meta by path_metadata'
				self._meta=d=self.corpus.metad[self.id]
			else:
				#print '>> meta by file'
				self._meta=d=self.meta_by_file
			d['corpus']=self.corpus.name
			#d['medium']=getattr(self,'medium') if hasattr(self,'medium') else ''
			self._meta=d
		return self._meta

	def spacy(self,load_from_file=False,model_name='en_core_web_sm'):
		import spacy
		global nlp
		if not nlp:
			print '>> loading spacy...'
			nlp = spacy.load(model_name)

		doc=None
		if self.parsed and load_from_file:
			#print self.fnfn_spacy
			from spacy.tokens.doc import Doc

			try:
				for byte_string in Doc.read_bytes(open(self.fnfn_spacy, 'rb')):
					doc = Doc(nlp.vocab)
					doc.from_bytes(byte_string)
			except UnicodeDecodeError:
				print "!! UNICODE ERROR:",self.fnfn_spacy
		#else:

		if not doc:
			#print '>> making spacy document for text',self.id
			txt=self.text
			txt=clean_text(txt)
			doc=nlp(txt)

		return doc

	@property
	def parsed(self):
		return os.path.exists(self.fnfn_spacy)

	@property
	def txt(self):
		return self.text
	
	@property
	def text(self):
		return self.text_plain()
		#if not hasattr(self,'_text'):
		#	self._text=codecs.open(self.fnfn,encoding='utf-8').read()
		#return self._text
		#print self.path_xml, self.fnfn
		"""
		if not self.fnfn or not os.path.exists(self.fnfn): return ''
		of=codecs.open(self.fnfn,encoding='utf-8',errors='ignore')
		txt=of.read()
		of.close()
		return txt
		"""

	@property
	def text_xml(self):
		return '\n'.join([line for line in self.lines_xml()])

	@property
	def exists(self):
		return os.path.exists(self.fnfn_xml) or os.path.exists(self.fnfn_txt)

	@property
	def exists_txt(self):
		return os.path.exists(self.fnfn_txt)

	@property
	def exists_xml(self):
		return os.path.exists(self.fnfn_xml)

	@property
	def dom(self):
		import bs4
		return bs4.BeautifulSoup(self.text_xml,'lxml')


	def split(self,doc_tag='doc'):
		md={}
		docnum=0
		for line in self.lines_xml():
			if '<'+doc_tag+'>' in line:
				docnum+=1
				print '>>',self.id,docnum,'...'
				newfn=self.fnfn_xml.replace('_xml_','_xml_split_').replace(self.ext_xml,'.'+str(docnum).zfill(2)+self.ext_xml)
				if not os.path.exists(os.path.split(newfn)[0]): os.makedirs(os.path.split(newfn)[0])
				#if os.path.exists(newfn): continue
				if newfn.endswith('.gz'):
					f=gzip.open(newfn,'wb')
				else:
					f=codecs.open(newfn,'w','utf-8')
			if not docnum: continue


			if newfn.endswith('.gz'):
				f.write(line.encode('utf-8'))
			else:
				f.write(line)


	## GETTING TEXT

	def text_plain(self, OK=['p','l'], BAD=[], body_tag='text', force_xml=False, text_only_within_medium=True):
		if not self.exists: return ''
		if not force_xml and os.path.exists(self.fnfn_txt):
			#print '>> text_plain from stored text file:',self.fnfn_txt
			txt=tools.read(self.fnfn_txt).replace('\r\n','\n').replace('\r','\n')
			return txt
		return self.text_plain_from_xml(OK=OK,BAD=BAD,body_tag=body_tag,text_only_within_medium=text_only_within_medium)


	## TOKENS

	@property
	def tokens(self,pos_tag=False):
		return self.tokens_plain
		## No spacy for now
		#if not os.path.exists(self.fnfn_spacy):
		if not pos_tag:
			tuples = [(tools.noPunc(unicode(tok).strip().lower()),'') for tok in self.tokens_plain]
		else:
			tuples = [ (tools.noPunc(unicode(tok).strip().lower()), tok.tag_) for tok in self.spacy ]
			tuples = [(a,b) for a,b in tuples if a]
		tuples = [(a,b) for a,b in tuples if a]
		return tuples

	@property
	def words(self):
		return [a for a,b in self.tokens]

	@property
	def tokens_plain(self):
		from nltk import word_tokenize
		try:
			txt=self.text_plain()
			return word_tokenize(txt)
		except IOError:
			return []


	@property
	def num_words(self,keys=['num_words_adorn','num_words']):
		for k in keys:
			if k in self.meta:
				return float(self.meta[k])
		return len(self.tokens)

	@property
	def ocr_accuracy(self):
		return float(self.meta['ocr_accuracy']) if 'ocr_accuracy' in self.meta else ''

	@property
	def minhash(self):
		from datasketch import MinHash
		m = MinHash()
		for word in self.tokens:
			m.update(word.encode('utf-8'))
		return m

	@property
	def length(self):
		return self.num_words

	@property
	def num_words_recognized(self):
		return int(self.num_words * self.ocr_accuracy) if self.ocr_accuracy else self.num_words

	@property
	def length_recognized(self):
		return self.num_words_recognized


	@property
	def freqs_tokens(self):
		from collections import Counter
		return Counter([x.lower() for x in self.tokens])

	@property
	def is_tokenized(self):
		ofolder=os.path.join(self.corpus.path, 'freqs', self.corpus.name)
		ofnfn=os.path.join(ofolder,self.id+'.json')
		return os.path.exists(ofnfn) and os.stat(ofnfn).st_size

	@property
	def freqs_json(self):
		import json,codecs
		fnfn=self.fnfn_freqs
		if not os.path.exists(fnfn): return {}
		with codecs.open(fnfn,encoding='utf-8') as f:
			dx={}
			try:
				for k,v in json.load(f).items():
					k2=tools.noPunc(k)
					if not k2 in dx: dx[k2]=0
					dx[k2]+=v
			except ValueError:
				print "!? JSON LOADING FAILED ON TEXT:",self.id
				return {}

			return dx

	@property
	def fnfn_freqs(self):
		fnfn=os.path.join(self.corpus.path, 'freqs', self.corpus.name, self.id+'.json')
		return fnfn

	#@property
	def freqs(self,modernize_spelling=False,modernize_spelling_before=3000,use_text_if_nec=True):
		fnfn=self.fnfn_freqs
		if not os.path.exists(fnfn):
			#print '!! no freqs file for:',self.id,'--?-->',fnfn
			#return {}
			if use_text_if_nec:
				dx=self.freqs_tokens
			else:
				return {}
		else:
			dx=self.freqs_json

		if modernize_spelling and self.year<modernize_spelling_before:
			dx2={}
			for k,v in dx.items():
				k2=self.corpus.modernize_spelling(k).lower()
				dx2[k2]=v
			dx=dx2

		return dx

	def freqs_ngram(self,n=2):
		return tools.toks2freq(tools.ngram([x for x in self.tokens], n))


	def get_passages(self,phrases=[],window=500):
		import time
		tic=time.clock()
		#print '>> loading passages (I/O)..'
		txt=self.text
		passages=list(tools.passages(txt,phrases=phrases,window=window))
		for dx in passages:
			dx['id']=self.id
			dx['corpus']=self.corpus.name
			for k,v in self.meta.items(): dx[k]=v
		toc=time.clock()
		#print '\tdone loading passages(I/O)... ('+str(toc-tic)+' seconds)'
		return passages

	def lines_xml(self):
		if self.fnfn_xml.endswith('.gz'):
			with gzip.open(self.fnfn_xml,'rb') as f:
				for line in f:
					yield line.decode('utf-8',errors='ignore')
		else:
			with codecs.open(self.fnfn_xml,'r','utf-8') as f:
				for line in f:
					yield line

	def lines_txt(self):
		if self.fnfn_txt.endswith('.gz'):
			with gzip.open(self.fnfn_txt,'rb') as f:
				for line in f:
					yield line.decode('utf-8')
		else:
			with codecs.open(self.fnfn_txt,'r','utf-8') as f:
				for line in f:
					yield line


	def save_plain_text(self,txt=None,compress=True):
		fnfn_txt = os.path.join(self.corpus.path_txt,self.id+'.txt')
		if compress: fnfn_txt+='.gz'
		#if os.path.exists(fnfn_txt): return

		if txt is None: txt=self.text_plain()

		path_fnfn=os.path.dirname(fnfn_txt)
		if not os.path.exists(path_fnfn): os.makedirs(path_fnfn)

		if not compress:
			tools.write2(fnfn_txt, txt)
		else:
			import gzip
			with gzip.open(fnfn_txt,'wb') as f:
				f.write(txt.encode('utf-8'))
			print '>> saved:',fnfn_txt





	def save_vector_html(self,tsne_dd,fn=None):
		if not fn: fn=self.id+'.html'
		vals=[[],[],[]]
		word2vals={}
		for word in tsne_dd:
			if not word in word2vals: word2vals[word]=[]
			keys=sorted(tsne_dd[word].keys())
			vkeys = [k for k in keys if 'tsne_V' in k]
			for i,vk in enumerate(vkeys):
				val=float(tsne_dd[word][vk])
				vals[i]+=[val]
				word2vals[word]+=[val]

		minmaxes = [(min(vs),max(vs)) for vs in vals]
		for word in word2vals:
			for i,val in enumerate(word2vals[word]):
				OldMin,OldMax=minmaxes[i]
				NewMin,NewMax=0.0,255.0
				OldValue=val
				OldRange = (OldMax - OldMin)
				NewRange = (NewMax - NewMin)
				NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
				word2vals[word][i]=str(int(NewValue))

		html=[]
		for line in self.lines_txt():
			words=line.strip().split()
			line_html=[]
			for word in words:
				wordl=tools.noPunc(word.lower())
				if wordl in word2vals:
					span=u'<span style="color:rgb({0})">{1}</span>'.format(','.join(word2vals[wordl]), word)
				else:
					span=u'<span>'+word+'</span>'
				line_html+=[span]
			html+=[u' '.join(line_html)]
		htmlstr=u'<br/>\n'.join(html)

		tools.write2(fn,htmlstr)


	"""
	def incorporate_match(self,other):
		if not hasattr(self,'_meta'): self.meta
		if not hasattr(other,'_meta'): other.meta
		for k,v in other._meta.items():
			if k in self._meta: k+='_'+other._meta['corpus']
			self._meta[k]=v
	"""


REPLACEMENTS={
				'&hyphen;':'-',
				'&mdash;':' -- ',
				'&ndash;':' - ',
				'&longs;':'s',
				u'\u2223':'',
				u'\u2014':' -- ',
				'|':'',
				'&ldquo;':u'“',
				'&rdquo;':u'”',
				'&lsquo;':u'‘’',
				'&rsquo;':u'’',
				'&indent;':'     ',
				'&amp;':'&',


			}

import bleach
def clean_text(txt,replacements=REPLACEMENTS):
	for k,v in replacements.items():
		txt=txt.replace(k,v)
	return bleach.clean(txt,strip=True)






class TextMeta(Text):
	def __init__(self,texts):
		self.texts=texts

	@property
	def id(self):
		return self.texts[0].id

	@property
	def corpus(self):
		return self.texts[0].corpus

	def lines_txt(self):
		return self.texts[0].lines_txt()

	@property
	def meta(self):
		if not hasattr(self,'_meta'):
			self._meta=md={'corpus':self.corpus.name}
			for t in reversed(self.texts):
				for k,v in t.meta.items():
					#if k in md and md[k]:
					#	k=k+'_'+t.__class__.__name__.replace('Text','').lower()
					md[k]=v
		return self._meta


	@property
	def is_metatext(self):
		return True




class TextSection(Text):
	def __init__(self,text,section_num,section_type,section_xml=None,section_txt=None,divider_tag=None):
		self.parent=text
		self.num=section_num
		self.type=section_type
		self.is_text_section = True
		self._xml=section_xml
		self._txt=section_txt
		if divider_tag:
			self.divider_tag=divider_tag.lower()
		elif hasattr(self,'DIVIDER_TAG') and self.DIVIDER_TAG:
			self.divider_tag=self.DIVIDER_TAG
		else:
			self.divider_tag=None

	@property
	def fnfn_freqs(self):
		fnfn=os.path.join(self.corpus.path, 'freqs', self.corpus.parent.name, self.id+'.json')
		return fnfn

	@property
	def text_xml(self):
		if not self._xml:
			self.parent.load_sections()
		return self._xml

	def unload(self):
		self._xml=''
		self._txt=''



	@property
	def id(self):
		return self.parent.id+'/section'+str(self.num).zfill(3)

	@property
	def corpus(self):
		return self.parent.corpus.sections

	def text_plain(self):
		return self.parent.text_plain_from_xml(self.text_xml,text_only_within_medium=True,body_tag=self.divider_tag)

	def lines_txt(self):
		for ln in self.text_plain().split('\n'):
			yield ln

	def load_metadata(self):
		# #md=self._meta=dict(self.parent.meta.items())
		# if not hasattr(self,'_meta'):
		# 	md=self._meta={}
		# else:
		# 	md=self._meta
		#
		md={}
		md['id']=self.id
		md['text_id']=self.parent.id
		md['section_type']=self.type
		return md


	@property
	def meta(self):
		if not hasattr(self,'_meta'):
			md=self._meta={}
		else:
			md=self._meta
		for k,v in self.parent.meta.items():
			if not k in md or not md[k]:
				md[k]=v
		#for k,v in self.load_metadata().items(): md[k]=v
		return self._meta


	@property
	def meta_by_file(self):
		self._meta=self.load_metadata()
		return self._meta


def text_plain_from_xml(xml, OK={'p','l'}, BAD=[], body_tag='text'):
	#print '>> text_plain from stored XML file...'
	import bs4

	## get dom
	dom = bs4.BeautifulSoup(xml,'lxml') if type(xml) in [str,unicode] else xml
	txt=[]
	## remove bad tags
	for tag in BAD:
		[x.extract() for x in dom.findAll(tag)]
	## get text
	for doc in dom.find_all(body_tag):
		for tag in doc.find_all():
			if tag.name in OK:
				txt+=[clean_text(tag.text)]
	TXT='\n\n'.join(txt).replace(u'∣','')
	return TXT


def get_author_dates(author):
	import re
	dates = [x for x in re.split('\W',author) if x.isdigit() and len(x)==4]
	if not dates:
		return (None,None)
	elif len(dates)==1:
		return (int(dates[0]),None)
	else:
		return tuple([int(x) for x in dates[:2]])
	return (None,None)
