# -*- coding: utf-8 -*-

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

		print '>> text_plain from stored XML file...'

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
