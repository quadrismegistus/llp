# -*- coding: utf-8 -*-

import codecs,json,pytxt,re

from lit.text import Text
from collections import defaultdict



class TextESTC(Text):
	META_SEP=' | '

	@property
	def json(self):
		with open(self.fnfn) as f:
			return json.loads(f.read())

	@property
	def estcid(self):
		return self.id.split('/')[-1]

	@property
	def id_estc(self):
		return self.estcid

	@property
	def codes(self):
		codes=[]
		jsonx=self.json
		for fieldd in jsonx['fields']:
			for field_code,field_value in fieldd.items():
				if type(field_value)==dict and 'subfields' in field_value:
					for subfieldd in field_value['subfields']:
						for subfield_code,subfield_value in subfieldd.items():
							codes+=[(field_code+'_'+subfield_code, subfield_value)]
				else:
					codes+=[(field_code,field_value)]
		return codes

	@property
	def coded(self):
		coded=defaultdict(list)
		for code,val in self.codes:
			val=pytxt.noPunc(val).strip()
			if not val in coded[code]:
				coded[code]+=[val]
		return coded


	@property
	def meta_by_file(self):
		md={}
		md['id']=self.id
		md['id_estc']=self.id.split('/')[-1]

		coded = self.coded

		## marc data in 008
		marc=''.join(coded['008'])
		md['year']=marc[7:11]
		md['year_end']=marc[11:15].strip()
		md['year_type_marc']=marc[6]
		md['form_marc']=marc[33]
		md['lang']=marc[35:38]

		# author
		md['author']=coded['100_a']
		md['author_dates']=coded['100_c']

		# title
		md['title']=coded['245_a']
		md['title_sub']=coded['245_b']

		# pubinfo
		#md['pubplace']=pytxt.noPunc(coded.get('260_a','')).strip()
		md['pub_statement']=coded['260_b']
		md['pub_nation']=coded['752_a']
		md['pub_region']=coded['752_b']
		md['pub_city']=coded['752_d']

		# book
		ansi_escape = re.compile(r'\x1b.')
		md['book_extent']=coded['300_a']
		md['book_dimensions']=[ansi_escape.sub('',x).replace('0',u'⁰') for x in coded['300_c']]

		# book v2
		md['book_extent_num_pages']=''
		if md['book_extent']:
			extent=md['book_extent'][0]
			nums_in_extent = [int(x) for x in re.findall(r'\d+', extent)]
			md['book_extent_num_pages']=str(max(nums_in_extent)) if nums_in_extent else ''

		md['book_dimensions_standard']=''
		if md['book_dimensions']:
			dim=md['book_dimensions'][0]
			if u'⁰' in dim and dim[dim.index(u'⁰')-1].isdigit():
				md['book_dimensions_standard']=dim[dim.index(u'⁰')-1]



		# notes
		#"""
		md['notes']=[]
		for key in coded:
			if int(key[:3])>=500 and int(key[:3])<510 and key.endswith('a'):
				md['notes']+=coded[key]
		#"""

		# subject tags
		md['subject_topic']=coded['650_a']
		md['subject_place']=coded['651_a']
		md['subject_person']=coded['700_a']
		md['form']=coded['655_a']

		# stringify
		for k,v in md.items():
			if type(v)==list:
				md[k]=self.META_SEP.join(v)

		return md


	@property
	def features(self):
		pass


	#@property
	#def title(self):
	#	return self.meta['title']+' '+self.meta['title_sub']
