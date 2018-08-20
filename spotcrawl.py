import requests
from bs4 import BeautifulSoup
import json
import time


def get_artists_tracks(url):
	returndict = {'Tracks': [], 'Images' : []}
	page = requests.get(url)
	html = BeautifulSoup(page.text, 'html.parser')
	lyrics = html.find_all('script')
	for line in lyrics:
		if '@context' in line.get_text():
			dic = json.loads(line.get_text().strip())
			# print()
			# print(dic)
			# print()
			returndict['Name'] = dic['name']
			returndict['Description'] = dic['description']
		elif "Spotify.Entity =" in line.get_text():
			first = line.get_text().strip()
			text = first[first.find("Spotify.Entity = ")+ len("Spotify.Entity = "):len(first)-1]
			longdict = json.loads(text)
			# print()
			# print(longdict)
			# print()
			for item in longdict['tracks']['items']:
				# print(item)
				# print()
				returndict['Tracks'].append("|Track|: " + str(item['track']['name']) + ' |Artist|: ' + str(item['track']['artists'][0]['name'] + ' |URL|:'))
				# for thing in item['track']:
				# 	# print(thing)
				returndict['Images'].append(item['track']['album']['images'][0]['url'])
			break
	return returndict
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
#print(get_artists_tracks('https://open.spotify.com/user/1230065337/playlist/2rCtJ4xiRrBDwCaGuAYQna'))



