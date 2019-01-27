
from lit.text import Text

class TextSellars(Text):
	@property
	def medium(self):
		if self.genre in {'Drama'}:
			return 'Unknown'
		elif self.genre in {'Poetry'}:
			return 'Verse'
		else:
			return 'Prose'
