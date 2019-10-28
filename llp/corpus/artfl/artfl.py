import os
from llp.text import Text
from llp.corpus import Corpus
from llp import tools


urlprefix = 'http://artflsrv02.uchicago.edu'
metafn = 'ARTFL-Frantext Results.html'









########################################################################################################################
# [ARTFL]
# (1) Text Class
########################################################################################################################

class TextARTFL(Text):
	pass






########################################################################################################################
# (2) Corpus Class
########################################################################################################################

class ARTFL(Corpus):
	TEXT_CLASS=TextARTFL


	####################################################################################################################
	# (2.1) Installation methods
	####################################################################################################################

	@property
	def path_raw_metadata(self):
		return os.path.join(self.path_raw,'metadata.htm')

	def download_raw_metadata(self):
		if not os.path.exists(self.path_raw): os.makedirs(self.path_raw)
		metadata_fn=self.path_raw_metadata
		if os.path.exists(metadata_fn): return
		with open(metadata_fn,'w') as of:
			import requests
			url=urlprefix+'/cgi-bin/philologic/search3t?dbname=frantext0513&word='
			txt = requests.get(url).text
			of.write(txt)

	def compile_metadata(self):
		self.download_raw_metadata()
		with open(self.path_raw_metadata) as f:
			old=[]
			for ln in f:
				if not ln.startswith('<a name'): continue
				#print ln
				idx=ln.split('navigate.pl?')[1].split('">')[0].strip()
				date=ln.split('[<b>')[1].split('</b>]')[0].strip()
				author=ln.split('[<b>')[0].split('">')[-1].strip()
				title=ln.split('</a></i>')[0].split('">')[-1].strip()
				edition=ln.split('</a></i>')[1].split(')')[0].replace('(','').replace(')','').strip()
				genre=ln.split('[genre: ')[1].split(']')[0].strip() if '[genre: ' in ln else ''
				url_wordcount = ln.split('[<a href="')[-1].split('">')[0]
				url_text=ln.split('<i><a href="')[-1].split('">')[0]

				#print [idx,date,author,title,edition,genre,url_wordcount,url_text]
				odx={'id':idx, 'year':date, 'author':author, 'title':title, 'edition':edition, 'genre':genre, 'url_wordcount':url_wordcount, 'url_text':url_text}
				genrel=genre.lower()
				if 'conte' in genrel or 'narratif' in genrel or 'roman' in genrel:
					odx['genre']='Fiction'
				elif u'poésie' in genrel or 'poesie' in genrel:
					odx['genre']='Poetry'
				elif 'theatre' in genrel:
					odx['genre']='Drama'
				elif 'correspond' in genrel:
					odx['genre']='Letter'
				elif 'memoir' in genrel:
					odx['genre']='Memoir'
				elif 'voyage' in genrel:
					odx['genre']='Travel'
				elif 'traite' in genrel or 'prose' in genrel or 'pamphlet' in genrel or 'essai' in genrel or 'eloquence' in genrel:
					odx['genre']='Non-Fiction'
				else:
					odx['genre']=''

				old+=[odx]
			tools.write(self.path_metadata, old)

	@property
	def path_raw_freqs(self):
		return os.path.join(self.path_raw,'wordcounts')

	def download_raw_freqs(self):
		import requests
		opath=self.path_raw_freqs
		if not os.path.exists(opath): os.makedirs(opath)
		for t in self.texts():
			d=t.meta
			url = urlprefix + d['url_wordcount']
			req = requests.get(url)
			txt = req.text

			countstr=txt.split('<pre>')[1].split('</pre>')[0].strip()
			countstr=countstr.replace(' ','\t')
			tools.write(os.path.join(opath, t.id+'.txt'), countstr)

	def compile_freqs(self):
		import ujson as json
		ipath=self.path_raw_freqs

		if not os.path.exists(self.path_freqs): os.makedirs(self.path_freqs)
		for t in self.texts():
			fnfn=os.path.join(ipath,t.id+'.txt')
			if not os.path.exists(fnfn): continue
			countd={}

			with open(fnfn) as f:
				for ln in f:
					ln=ln.strip()
					if not ln: continue
					if not '\t' in ln: continue
					word,count=ln.split('\t',1)
					countd[word]=int(count)

			with open(t.path_freqs,'w') as of:
				json.dump(countd, of)
				print('>> saved:',t.path_freqs)


















########################################################################################################################
