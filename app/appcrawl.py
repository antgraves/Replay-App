import requests
from bs4 import BeautifulSoup
import json
import time

# start_time = time.time()
# print('here')
# print("--- %s seconds ---" % (time.time() - start_time))
def extract_url(sub):
	ret = sub[sub.find('https://'):]
	ret = ret[:ret.find(' ')]
	ret = ret[:len(ret) - 11] + "640x640cc.jpg"
	return ret

def get_artists_tracks(url):
	returndict = {'Tracks' : [], 'Description' : "", 'Images' : []}
	page = requests.get(url)
	html = BeautifulSoup(page.text, 'html.parser')
	# print()
	# print("--- %s seconds ---" % (time.time() - start_time))
	image = html.find_all(class_ = 'we-artwork--less-round we-artwork ember-view')
	# print(html)
	# print()
	# print("--- %s seconds ---" % (time.time() - start_time))
	for item in image:
		# count += 1
		item = str(item)
		sub = extract_url(item)
		returndict['Images'].append(sub)
	tracks = html.find(id = 'shoebox-ember-data-store').get_text()
	longdict = json.loads(tracks)
	# print()
	# print("--- %s seconds ---" % (time.time() - start_time))
	# print()
	# print(longdict)
	# print()
	# print()
	returndict['Name'] = longdict['data']['attributes']['name']
	if 'description' in longdict['data']['attributes'].keys():
		returndict['Description'] = longdict['data']['attributes']['description']['standard']
	# misses = []
	# counter = 0
	for thing in longdict['included']:
		# print(thing['type'])
		if 'song' in thing['type']:
			returndict['Tracks'].append("|Track|: " + str(thing['attributes']['name']) + ' |Artist|: ' + str(thing['attributes']['artistName']) + ' |URL|: ' + str(thing['attributes']['url']))
	changeid = False
	ind = 0
	# print()
	# print("--- %s seconds ---" % (time.time() - start_time))
	# for i in range(len(returndict['Tracks'])):
	# 	if i >= len(returndict['Images']):
	# 		break
	# 	# print(returndict['Tracks'][i])
	# 	artid = returndict['Tracks'][i][:returndict['Tracks'][i].find('|')]
	# 	# print(changeid)
	# 	# print(artid)
	# 	imid = returndict['Images'][ind][returndict['Images'][ind].find(' ') + 1:]
	# 	# print(imid)
	# 	if artid != imid:
	# 		misses.append(returndict['Tracks'][i])
	# 		changeid = True
	# 	else:
	# 		changeid = False
	# 	# print()
	# 	if not changeid:
	# 		ind += 1

	# for i in range(len(returndict['Tracks'])):
	# 	returndict['Tracks'][i] =  str(i) + " " + str(returndict['Tracks'][i])

	# for i in range(len(returndict['Images'])):
	# 	returndict['Images'][i] =  str(i) + " " + str(returndict['Images'][i])


	# print(returndict['Tracks'])
	# print()
	# print(returndict['Images'])
	# print()
	# print(returndict['Name'])
	# print()
	# print(returndict['Description'])
	# print(len(returndict['Tracks']))
	# print(len(returndict['Images']))
	# print()
	return returndict

# print('there')
# print("--- %s seconds ---" % (time.time() - start_time))
# dic = get_artists_tracks('https://itunes.apple.com/us/playlist/test-long/pl.u-06oxDj6tJ8ZRd4')
# print(len(dic['Tracks']))
# print(len(dic['Images']))
# print(dic)
# print("--- %s seconds ---" % (time.time() - start_time))
#print(get_artists_tracks('https://itunes.apple.com/us/playlist/testtwo/pl.u-MDAWvR9FeVkpyN'))





