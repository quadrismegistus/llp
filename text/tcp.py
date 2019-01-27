# -*- coding: utf-8 -*-

import os,codecs,pytxt
from lit.text import Text,TextSection
from lit.text import clean_text


class TextSectionTCP(TextSection):
	DIVIDER_TAG='DIV1'

	def load_metadata(self):
		md=super(TextSectionTCP,self).load_metadata()
		md['genre'],md['medium']=self.parent.return_genre()
		return md

	@property
	def meta(self):
		md=super(TextSectionTCP,self).meta
		genre=self.corpus.parent.sectiontype2genre(self.type)
		if genre: md['genre']=genre
		return md

class TextTCP(Text):
	def sections_xml(self,divider_tag='DIV1'):
		return super(TextTCP,self).sections_xml(divider_tag=divider_tag,text_section_class=self.corpus.TEXT_SECTION_CLASS)

	def text_plain_from_xml(self, xml=None, OK=['p','l'], BAD=[], body_tag='text', force_xml=False, text_only_within_medium=True):
		print '>> text_plain from stored XML file...'
		import bs4

		## get dom
		txt=[]
		if not xml:
			text_xml=xml=self.text_xml
			dom = bs4.BeautifulSoup(xml,'lxml')
		elif type(xml)==bs4.BeautifulSoup:
			dom = xml
			text_xml=unicode(xml)
		else:
			text_xml=xml
			dom = bs4.BeautifulSoup(xml,'lxml')

		## remove bad tags
		for tag in BAD:
			[x.extract() for x in dom.findAll(tag)]

		## get only correct text for medium
		if text_only_within_medium:
			medium=self.medium
			if not medium:
				genre,medium=self.return_genre(text_xml)
			if 'Verse' in medium or 'Poetry' in medium:
				OK = ['l']
			elif 'Prose' in medium or 'Fiction' in medium or 'Non-Fiction' in medium:
				OK = ['p']

		for doc in dom.find_all(body_tag):
			for tag in doc.find_all():
				if tag.name in OK:
					txt+=[clean_text(tag.text)]
		return '\n\n'.join(txt).replace(u'∣','')

	def text_plain_by_tag(self,OK=['p','l']):
		dom = self.dom
		body = dom.find('text')
		#print len(dom), len(body)
		last_tag=None
		tag2lists={}
		for tag in OK: tag2lists[tag]=[]
		for tag in body.find_all():
			if not tag.name in OK: continue
			tagtxt=clean_text(tag.text)
			if tag.previous_sibling == last_tag and len(tag2lists[tag.name]):
				tag2lists[tag.name][-1]+=[tagtxt]
			else:
				tag2lists[tag.name]+=[ [tagtxt] ]

			last_tag = tag

		return tag2lists

	def extract_metadata(self,mtxt):
		md={}
		## IDs
		for idnox in mtxt.split('</IDNO>')[1:-1]:
			idno_type=idnox.split('TYPE="')[1].split('">')[0]
			idno_id=idnox.split('">')[-1]

			md['id_'+idno_type.replace(' ','_')]=idno_id

		biblio = pytxt.yank(mtxt,'BIBLFULL')
		md['title'] = biblio.split('</TITLE>')[0].split('">')[-1]
		md['author'] = pytxt.yank(biblio,'AUTHOR')
		md['extent'] = pytxt.yank(biblio,'EXTENT')
		md['pubplace'] = pytxt.yank(biblio,'PUBPLACE')
		md['publisher'] = pytxt.yank(biblio,'PUBLISHER')
		md['date'] = pytxt.yank(biblio,'DATE')
		md['notes']=pytxt.yank(biblio,'NOTESSTMT')

		try:
			md['year']=int(''.join([x for x in md['date'] if x.isdigit()][:4]))
		except (ValueError,TypeError) as e:
			md['year']=0

		return md

	def return_genre(self,text_xml=None):
		speaker_tag=False
		l_tag=False
		p_tag=False

		txt=text_xml.upper() if text_xml else self.text_xml.upper()

		tags = ['</SPEAKER>', '</L>', '</P>']
		tag_counts={}
		for tag in tags: tag_counts[tag]=txt.count(tag)

		# print self.id,self.title
		# print tag_counts
		# print

		drama = tag_counts['</SPEAKER>'] > 100
		verse = tag_counts['</L>'] > tag_counts['</P>']
		prose = tag_counts['</L>'] <= tag_counts['</P>']

		"""if drama and verse:
			genre='Drama [Verse]'
		elif drama and not verse:
			genre = 'Drama [Prose]'
		elif not drama and verse:
			genre = 'Verse'
		elif not drama and not verse:
			genre = 'Prose'
		else:
			genre = 'Unknown'"""

		medium = 'Verse' if verse else 'Prose'
		genre = 'Drama' if drama else medium

		return genre,medium
