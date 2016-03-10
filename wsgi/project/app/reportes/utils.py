from reportlab.lib.units import inch

class TextUtility:

	def __init__(self, canvas):
		self.canvas = canvas

	def align_right(self, text):
		max_inches = 7.3
		text_len = self.canvas.stringWidth(text)
		x_pos = max_inches * inch - text_len
		return x_pos