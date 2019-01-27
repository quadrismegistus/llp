
from lit.text import Text

class TextCLMET(Text):
	genre2Genre={u'Drama':'Drama',
	 u'LET':'Letter',
	 u'Narrative fiction':'Fiction',
	 u'Narrative non-fiction':'Biography',
	 u'Other':'Other',
	 u'Treatise':'Treatise'}

	@property
	def meta_by_file(self,bad_tags={'html','body'}):
		import codecs,bs4,os
		md={}
		md['medium']='Prose'

		txt=self.text_xml
		meta,text = txt.split('<text>')
		dom=bs4.BeautifulSoup(meta,'lxml')
		for tag in dom():
			if tag.name in bad_tags: continue
			md[tag.name]=tag.text

		md['id_orig']=md['id']
		md['id']=self.id
		md['genre']=self.genre2Genre[md['genre']]
		return md


	def text_plain(self, force_xml=False, text_only_within_medium=True):
		return super(TextCLMET,self).text_plain(OK=['p'], BAD=['page'], body_tag='text', force_xml=force_xml)
