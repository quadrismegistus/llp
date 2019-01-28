# -*- coding: utf-8 -*-

### TEXT CLASS
import codecs,os
from lit import tools
from lit.text import Text

class TextChadwyckPoetry(Text):
	STANZA_TAGS = ['stanza','versepara','pdiv']
	LINE_TAGS = ['l','lb']

	@property
	def genre(self): return 'Poetry'

	@property
	def meta_by_file(self):
		md={}
		num_lines=0
		num_stanzas=0

		for line in self.lines_xml():
			#if '<doc>' in line: break
			if '<T1>' in line: md['title']=line.split('<T1>')[1].split('</T1>')[0].strip()
			if '<t1>' in line: md['title']=line.split('<t1>')[1].split('</t1>')[0].strip()
			if '<A1>' in line: md['author']=line.split('<A1>')[1].split('</A1>')[0].strip()
			if '<a1>' in line: md['author']=line.split('<a1>')[1].split('</a1>')[0].strip()
			if '<Y1>' in line: md['year']=line.split('<Y1>')[1].split('</Y1>')[0].strip()
			if '<y1>' in line: md['year']=line.split('<y1>')[1].split('</y1>')[0].strip()
			if '<T2>' in line: md['title_volume']=line.split('<T2>')[1].split('</T2>')[0].strip()
			if '<t2>' in line: md['title_volume']=line.split('<t2>')[1].split('</t2>')[0].strip()
			if '<ID>' in line: md['idz']=line.split('<ID>')[1].split('</ID>')[0].strip()
			if '<id>' in line: md['idz']=line.split('<id>')[1].split('</id>')[0].strip()
			for lntag in self.LINE_TAGS:
				if '<'+lntag+'>' in line or '</'+lntag+'>' in line:
					num_lines+=1
			for stanzatag in self.STANZA_TAGS:
				if stanzatag in line:
					num_stanzas+=1


		if not 'modern/' in self.id and not 'faber' in self.id:
			if 'american' in self.id:
				md['nation']='American'
			else:
				md['nation']='British'
		md['medium']='Verse'
		md['genre']='Poetry'
		md['id']=self.id
		md['num_lines']=num_lines
		md['num_stanzas']=num_stanzas
		md['subcorpus']=self.id.split('/')[0]
		md['author_id']=self.id.split('/')[1]
		md['text_id']=self.id.split('/')[1]

		return md


	def text_plain(self, OK=['l','lb'], BAD=['note'], body_tag='poem'):
		REPLACEMENTS={
			'&indent;':'    ',
			'&hyphen;':'-',
			u'\u2014':' -- ',
			u'\u2013':' -- ',
		}

		if not self.exists: return ''
		if os.path.exists(self.fnfn_txt):
			print '>> text_plain from stored text file:',self.fnfn_txt
			return tools.read(self.fnfn_txt)

		#print '>> text_plain from stored XML file...'

		txt=[]
		dom = self.dom

		for tag in BAD:
			[x.extract() for x in dom.findAll(tag)]

		# standardize lines:
		for tag in self.LINE_TAGS:
			if tag=='l': continue
			for ent in dom(tag):
				ent.name='l'

		## replace stanzas
		num_stanzas=0
		for tag in self.STANZA_TAGS:
			for ent in dom(tag):
				ent.name='stanza'
				num_stanzas+=1
		txt=[]
		if not num_stanzas:
			for line in dom('l'):
				txt+=[line.text]
		else:
			for stanza in dom('stanza'):
				for line in stanza('l'):
					txt+=[line.text.strip()]
				txt+=['']

		txt='\n'.join(txt).replace(u'∣','').strip()
		for k,v in REPLACEMENTS.items():
			txt=txt.replace(k,v)
		return txt





### CORPUS CLASS
from lit.corpus import Corpus
import os,codecs,re
from lit import tools

class ChadwyckPoetry(Corpus):
	"""
	Steps taking in bringing this corpus from raw to refined.

	from lit.corpus.chadwyck_poetry import ChadwyckPoetry
	corpus = ChadwyckPoetry()
	corpus.gen_xml()
	corpus.tokenize_texts()
	corpus.save_metadata()
	corpus.refine_metadata()
	corpus.gen_mfw(yearbin=50,year_min=1600,year_max=2000)
	corpus.gen_freq_table()
	"""

	TEXT_CLASS=TextChadwyckPoetry
	PATH_TXT = 'chadwyck_poetry/_txt_chadwyck_poetry'
	PATH_XML = '/Volumes/Present/DH/corpora/chadwyck_poetry/xml'
	PATH_RAW = '/Volumes/Present/DH/corpora/chadwyck_poetry/raw'
	PATH_METADATA = 'chadwyck_poetry/corpus-metadata.ChadwyckPoetry.txt'
	EXT_XML='.xml'

	def __init__(self):
		super(ChadwyckPoetry,self).__init__('ChadwyckPoetry',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA,ext_xml=self.EXT_XML)
		self.path = os.path.dirname(__file__)

	def gen_xml(self, split_start='<poem>', split_end='</poem>', id_split_start='<ID>', id_split_end='</ID>'):
		"""
		Mapping from raw to this corpus's data.
		Will generate XML snippets from raw data, one per poem, stored in author folders.
		"""
		import multiprocessing as mp

		objects = []

		for subcorpus in os.listdir(self.PATH_RAW):
			subpath = os.path.join(self.PATH_RAW, subcorpus)
			opath = os.path.join(self.path_xml, subcorpus)
			for author_fn in os.listdir(subpath):
				author_fnfn=os.path.join(subpath,author_fn)
				if not author_fnfn.endswith('.new'): continue

				objects+=[(author_fnfn,opath)]


		pool=mp.Pool()
		pool.map(save_poems_from_raw_author_folder, objects)

	def refine_metadata(self,save=True,guess_gender=False,detect_posthumous=False,fudge_dates=False):
		if guess_gender: import gender_guesser.detector as gender

		gender_d={}
		for i,t in enumerate(self.texts()):
			print i
			#if not i%10000: print '>> processing text #',i,'...'
			metad=self.metad[t.id]

			if fudge_dates:
				try:
					metad['year']=int(metad['year'])
					dates_in_title = [int(x) for x in re.split('\W',t.title) if x.isdigit() and len(x)==4]
					for dt in dates_in_title:
						if dt<metad['year']:
							print t.year, t.title
							print '>>',dt
							metad['year_old']=t.year
							metad['year']=metad['year_new']=dt

				except ValueError:
					pass

			if detect_posthumous:
				metad['author_dob'],metad['author_dod']=t.author_dates
				metad['posthumous']=''
				if t.year and t.author_dates[0] and t.year>t.author_dates[0]:
					if not t.author_dates[1]:
						if t.author_dates[0] > 1900: # so it's plausible they're still alive
							metad['posthumous']=False
					else: # has death date
						if t.year>t.author_dates[1]:
							metad['posthumous']=True
						else:
							metad['posthumous']=False

			if guess_gender:
				import gender_guesser.detector as gender

				if t.author in gender_d:
					metad['author_gender']=gender_d[t.author]
				else:
					isnt_this_problematic_just_to=gender.Detector()
					genders = [isnt_this_problematic_just_to.get_gender(x) for x in re.split('\W',t.author)]
					for x in genders:
						if x!='unknown':
							metad['author_gender']=x
							gender_d[t.author]=x
							break
						else:
							metad['author_gender']='unknown'
							gender_d[t.author]='unknown'



		timestamp=tools.now().split('.')[0]
		tools.write2(os.path.join(self.path,'corpus-metadata.%s.%s.txt' % (self.name,timestamp)), self.meta)












## FUNCTIONS

def save_poems_from_raw_author_folder((author_fnfn, opath), use_bs4=False):
	import bs4
	author_fn=os.path.split(author_fnfn)[-1]
	author_id = author_fn.split('.')[0]
	opath = os.path.join(opath, author_id)
	if not os.path.exists(opath): os.makedirs(opath)

	print '>>',opath,'...'
	with codecs.open(author_fnfn,encoding='latin1') as f:
		txt=f.read()
		txt=unicode(txt.replace('\r\n','\n').replace('\r','\n'))
		if use_bs4:
			dom = bs4.BeautifulSoup(txt,'lxml')
			for poem_i,poem in enumerate(dom('poem')):
				poem_num=poem_i+1
				ids=poem('id')
				if not ids: continue
				idx=ids[0].text
				if not idx: continue
				poem_xml_str = unicode(poem)

				ofnfn = os.path.join(opath, idx+'.xml')
				with codecs.open(ofnfn,'w',encoding='utf-8') as of:
					of.write(poem_xml_str)
		else:
			txt=txt.replace('<poem ','<poem>')
			for poem in txt.split('<poem>')[1:]:
				idx=None
				try:
					poem = '<poem>'+ poem.split('</poem>')[0]+'</poem>'
					idx=poem.split('</ID>')[0].split('<ID>')[1]
				except IndexError as e:
					pass
				if not idx or not poem: continue
				poem_xml_str = poem

				ofnfn = os.path.join(opath, idx+'.xml')
				with codecs.open(ofnfn,'w',encoding='utf-8') as of:
					of.write(poem_xml_str)
			#print '>> saved:',ofnfn


class ChadwyckPoetrySample(ChadwyckPoetry):
	def __init__(self):
		super(ChadwyckPoetrySample,self).__init__('ChadwyckPoetrySample',path_txt=self.PATH_TXT,path_xml=self.PATH_XML,path_metadata=self.PATH_METADATA,ext_xml=self.EXT_XML)
		self.path = os.path.dirname(__file__)

	def gen(self,n_texts=100,per_n_years=10):
		"""
		Logic of this sample:
		Just get everything posthumous.
		"""
		pass
