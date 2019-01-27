# -*- coding: utf-8 -*-

import codecs

from lit.text import Text
from lit.text.tcp import TextTCP

class TextEEBO_TCP(TextTCP):
	@property
	def meta_by_file(self):
		if not hasattr(self,'_meta'):
			mtxt=''
			for line in self.lines_xml():
				mtxt+=line
				if '</HEADER>' in line:
					break
			md=self.extract_metadata(mtxt)
			md['fnfn_xml']=self.fnfn
			md['id']=self.id
			md['genre'],md['medium']=self.return_genre()
			del md['notes']
			self._meta=md
		return self._meta
