from PIL import Image

class ImgOpt(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ImgOpt, self).__init__()
		self.arg = arg
		
	@staticmethod
	def resize(file_path, size_x=None , size_y=None ):
		basewidth = 800

		try:
			with Image.open(file_path) as img:
				wpercent = (basewidth/float(img.size[0]))
				hsize = int((float(img.size[1])*float(wpercent)))
				img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
				img = img.convert('RGB')
				img.save(file_path, "JPEG")
		except Exception as e:
			raise e
