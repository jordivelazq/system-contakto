from PIL import Image as ImagePillow

class ImgOpt(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ImgOpt, self).__init__()
		self.arg = arg
		
	@staticmethod
	def resize(file_path, size_x=None , size_y=None ):
		try:
			img_original = ImagePillow.open(file_path)
			original_size = img_original.size

			if not size_x and not size_y:
				new_size = (800,600)

			if size_x and size_y:
				new_size = (size_x,size_y)
			else:
				ratio = round(float(size_x/float(original_size[0])),10) if not size_y else round(float(size_y/float(original_size[1])),10)
				new_size = (int(ratio*original_size[0]), int(ratio*original_size[1]))
			nueva = img_original.resize(new_size)
			nueva.save(file_path,"JPEG")
		except Exception, e:
			raise e