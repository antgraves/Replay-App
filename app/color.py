from PIL import Image
import requests
from io import BytesIO
import time

# start_time = time.time()
# print('here')
# print("--- %s seconds ---" % (time.time() - start_time))

def avgcolor(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	(width,height) = img.size
	pixvalues = [0,0,0]
	totpixels = (width / 10) * (height / 10)
	for x in range(0,width, 10):
		for y in range(0,height, 10):
			#print(img.getpixel((x,y))[0])
			color = img.getpixel((x,y))
			pixvalues[0] += color[0]
			pixvalues[1] += color[1]
			pixvalues[2] += color[2]

	for i in range(len(pixvalues)):
		pixvalues[i] = int(pixvalues[i] / (totpixels))
	# print(pixvalues)
	retstr = str(pixvalues)
	return retstr[1:retstr.find(']')]

# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

#print(avgcolor("https://i.scdn.co/image/04e9ebd52af8de7d734120497b3a10e3fece8a2c"))
# print("--- %s seconds ---" % (time.time() - start_time))

	