import requests
from bs4 import BeautifulSoup
import json
import time


def extract_url(sub): #fix image url so it's valid
	ret = sub[sub.find('https://'):]
	ret = ret[:ret.find(' ')]
	ret = ret[:len(ret) - 11] + "640x640cc.jpg"
	return ret

def get_artists_tracks(url): #crawl Apple website and return dictionary with artists, songs, and images links
	returndict = {'Tracks' : [], 'Description' : "", 'Images' : []}
	page = requests.get(url) #request page
	html = BeautifulSoup(page.text, 'html.parser') #parse page
	image = html.find_all(class_ = 'we-artwork--less-round we-artwork ember-view')
	
	for item in image: #get image links
		item = str(item)
		sub = extract_url(item)
		returndict['Images'].append(sub)

	tracks = html.find(id = 'shoebox-ember-data-store').get_text()
	longdict = json.loads(tracks)
	
	returndict['Name'] = longdict['data']['attributes']['name'] #get playlist name
	if 'description' in longdict['data']['attributes'].keys(): #get playlist description
		returndict['Description'] = longdict['data']['attributes']['description']['standard']

	for thing in longdict['included']: #get all songs in playlist
		if 'song' in thing['type']:
			returndict['Tracks'].append("|Track|: " + str(thing['attributes']['name']) + ' |Artist|: ' + str(thing['attributes']['artistName']) + ' |URL|: ' + str(thing['attributes']['url']))
	
	changeid = False
	ind = 0
	return returndict







