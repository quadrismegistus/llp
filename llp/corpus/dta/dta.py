import os
from llp.text import Text
from llp.corpus import Corpus
from llp import tools

########################################################################################################################
# [DTA]
# (1) Text Class
########################################################################################################################

class TextDTA(Text):
	# (b) Getting plain text from XML files
	def text_plain_from_xml(self):
		import bs4
		with open(self.path_xml) as f:
			txt=f.read()
			dom=bs4.BeautifulSoup(txt,'lxml')
			text = dom('text')[0].text
			text = text.replace(u'ſ',u's').replace(u'oͤ',u'ö').replace(u'aͤ',u'ä').replace(u'uͤ',u'ü')
			return text

	# (b) Get metadata from XML or other file
	def get_meta_from_file(self):
		hdr=[]
		for ln in self.lines_xml():
			hdr+=[ln]
			if '</teiHeader>' in ln: break

		hdr='\n'.join(hdr)
		source = hdr.split('<sourceDesc>')[1].split('</sourceDesc>')[0]

		dx={}

		# author
		author = source.split('<author>')[1].split('</author>')[0]
		author_name=[]
		try:
			author_lname = author.split('<surname>')[1].split('</surname>')[0]
			author_name+=[author_lname]
		except IndexError:
			pass
		try:
			author_fname = author.split('<forename>')[1].split('</forename>')[0]
			author_name+=[author_fname]
		except IndexError:
			pass
		dx['author'] = ', '.join(author_name)

		# title
		title_main = source.split('type="main">')[1].split('</title>')[0]
		try:
			title_sub = source.split('type="sub">')[1].split('</title>')[0]
		except IndexError:
			title_sub=None
		dx['title'] = title_main+': '+title_sub if title_sub else title_main

		# year
		try:
			dx['year']=source.split('<date type="publication">')[1].split('</date>')[0]
		except IndexError:
			try:
				dx['year']=source.split('<date type="creation">')[1].split('</date>')[0]
			except IndexError:
				raise Exception("no date?\n\n"+source)

		# genre
		for row in hdr.split('<classCode scheme="http://www.deutschestextarchiv.de/doku/klassifikation#')[1:]:
			row=row.split('</classCode>')[0]
			genre_type,genre = row.split('">',1)
			if genre_type[0]==genre_type[0].upper(): continue
			dx['genre_'+genre_type]=genre

		# id
		dx['id']=os.path.basename(self.path_xml).replace('.TEI-P5.xml','')

		for k,v in dx.items():
			dx[k]=v.replace('\r\n','//').replace('\r','//').replace('\n','//')

		## Medium
		gt0='genre_dwds1main'
		gt1='genre_dwds1sub'
		if dx[gt0]!='Belletristik':
			dx['genre']='Non-Fiction'
			#dx['medium']='Prose'
		elif 'roman' in dx[gt1].lower() or dx[gt1]==u'Märchen' or dx[gt1]==u'Novelle':
			dx['medium']='Prose'
			dx['genre']='Fiction'
		elif dx[gt1]=='Lyrik':
			dx['genre']='Poetry'
			dx['medium']='Verse'
		else:
			dx['genre']='Literature, Other'

		return dx


########################################################################################################################
# (2) Corpus Class
########################################################################################################################

class DTA(Corpus):
	TEXT_CLASS=TextDTA


	####################################################################################################################
	# (2.1) Installation methods
	####################################################################################################################

	def compile(self,**attrs):
		"""
		This is a custom installation function. By default, it will simply try to download itself,
		unless a custom function is written here which either installs or provides installation instructions.
		"""
		# move to raw folder
		if not os.path.exists(self.path_raw): os.makedirs(self.path_raw)
		if not os.path.exists(self.path_xml): os.makedirs(self.path_xml)

		# download file
		from llp import tools
		ofnfn=os.path.join(self.path_raw, f'_tmp_{self.id}_raw.zip')
		if not os.path.exists(ofnfn):
			print('>> downloading:',self.url_raw,'to',ofnfn)
			tools.download(self.url_raw, ofnfn)

		# unzip xml
		os.chdir(self.path_xml)
		tools.unzip(ofnfn)

		#return self.download(**attrs)


	def download(**attrs):
		"""
		This function is used to download the corpus. Leave as-is to use built-in LLP download system.
		Provide a

		So far, downloadable data types (for certain corpora) are:
			a) `txt` files
			b) `xml` files
			c) `metadata` files
			d) `freqs` files

		If you have another zip folder of txt files you'd like to download,
		you can specify with `url_txt` (i.e. url_`type`, where type is in `quotes` in (a)-(d) above):
			corpus.download(url_txt="https://www.etcetera.com/etc.zip")
		"""
		return super().download(**attrs)

	def install(self,parts=['metadata','txt','freqs','mfw','dtm'],force=False,**attrs):
		"""
		This function is used to boot the corpus, taking it from its raw (just downloaded) to refined condition:
			- metadata: Save metadata (if necessary)
			- txt: Save plain text versions (if necessary)
			- freqs: Save json frequency files per text
			- mfw: Save a long list of all words sorted by frequency
			- dtm: Save a document-term matrix
		"""
		return super().install(parts=parts,force=force,**attrs)




















########################################################################################################################
