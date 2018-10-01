from PIL import Image
import requests
from io import BytesIO
import time


def avgcolor(url): #return average rgb values of an image
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	(width,height) = img.size
	pixvalues = [0,0,0]
	totpixels = (width / 10) * (height / 10)
	for x in range(0,width, 10):

		for y in range(0,height, 10):
			color = img.getpixel((x,y))
			pixvalues[0] += color[0]
			pixvalues[1] += color[1]
			pixvalues[2] += color[2]

	for i in range(len(pixvalues)):
		pixvalues[i] = int(pixvalues[i] / (totpixels))
	retstr = str(pixvalues)
	return retstr[1:retstr.find(']')]


	