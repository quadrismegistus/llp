import os
from lit.text import Text

class TextDialNarr(Text):

	@property
	def meta_by_file(self):
		# 1825.Child.Am.F.The_Rebels_Or_Boston_Before_The_Revolution.dialogue
		md={}
		fn=os.path.basename(self.fnfn_txt)
		fn=fn.replace('.ascii','')
		md['year'],md['author'],md['nation'],md['gender'],md['title'],md['genre'],txt=fn.split('.')
		md['title']=md['title'].replace('_',' ')
		md['genre']='Fictional '+md['genre'].title()
		md['medium']='Prose'
		return md
