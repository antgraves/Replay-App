from spotipy import oauth2, Spotify
import json
import requests
import app.spotifyapi

from bs4 import BeautifulSoup

def removeParen(s): #remove parentheses in song name to optimize search
	if '(' not in s or ')' not in s:
		return s
	if s.find("(") > s.rfind(')'):
		return s
	initial = s[:s.rfind(')') + 1]
	begin = initial[:initial.rfind('(')]
	rest = initial[initial.rfind('(') + 1:]
	ind = rest.find(')')
	final = s[(len(begin) + 1) + (ind + 1):]
	sub = begin + final
	return removeParen(sub)

def removeBrack(s): #remove brackets in song name to optimize search
	if '[' not in s or ']' not in s:
		return s
	if s.find("[") > s.rfind(']'):
		return s
	initial = s[:s.rfind(']') + 1]
	begin = initial[:initial.rfind('[')]
	rest = initial[initial.rfind('[') + 1:]
	ind = rest.find(']')
	final = s[(len(begin) + 1) + (ind + 1):]
	sub = begin + final
	return removeParen(sub)


def spotify_playlist(token, service, url): #generate new spotify playlist; yield info to update progress bar
	
	apple = service == 'apple'
	tidal = service == 'tidal'

	if apple: 
		import app.appcrawl
		try: #get dictionary of songs from Apple playlist
			indict = app.appcrawl.get_artists_tracks(url) 
		except:
			yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
			return None

	elif tidal:
		import app.tidapi
		try:
			indict = app.tidapi.tidal_to_dict(url)
		except:
			yield "data:ERROR\n\n" #yield error, stop program, user input wrong URL
			return None
	
	else:
		yield "data:ERROR\n\n" #yield error, stop program, something went wrong on my end
		return None
	yield "data: 10\n\n"

	spotifyObject = Spotify(auth = token) #use token to validate responses
	user = spotifyObject.current_user()
	userid = user['id']

	idlist = []

	name = indict['Name']
	description = indict['Description']
	headers = {'Authorization': 'Bearer {0}'.format(token)}
	headers['Content-Type'] = 'application/json'
	data = {'name': name, 'public': 'True', 'description': description}
	r = spotifyObject._internal_call('POST',"users/%s/playlists" % userid, data, None) #create playlist

	plid = r['id'] #playlist ID
	misses = []
	yield "data: 15\n\n"

	displaypercent = 15 #approximately 15% done with program at this point
	exactpercent = 15.0 
	length = len(indict['Tracks'])

	for i in range(length // 100 + 1): #continuously call search function of API to find corresponding songs
		firstls = []

		for item in indict['Tracks'][(100 * i): ((i + 1) * 100)]: #create proper string to search
			searchsec = ""
			artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')]
			trackname = item[(item.find('|Track|:') + 9):item.find('|Artist|:')] 
			query = trackname + artistname
			query = query.replace("  "," ")
			retquery = artistname + ' - ' + trackname
			searchprim = spotifyObject.search(query, type = "track" , limit = 2) #search object

			addbool = False
			for thing in searchprim['tracks']['items']: #parse search object to find track
				
				for stuff in thing['artists']:

					if (artistname.lower() in stuff['name'].lower()) or (stuff['name'].lower() in artistname.lower()):
						firstls.append(thing['id'])
						addbool = True
						break

				if addbool:
					break

			if not addbool and (" & " in artistname or ("(" in trackname and ")" in trackname)): #try again but with different query

				secartist = artistname
				sectrack = trackname

				if " & " in artistname:
					secartist = artistname[:artistname.find(" & ")]

				if "(" in trackname and ")" in trackname:
					sectrack = removeParen(trackname)
				if "[" in trackname and "]" in trackname:
					sectrack = removeBrack(trackname)

				secquery = sectrack + secartist
				secquery = secquery.replace("  "," ")
				searchsec = spotifyObject.search(secquery, type = "track" , limit = 2)

				for thing in searchsec['tracks']['items']: #try again but with different query
					addbool = False

					for stuff in thing['artists']:

						if (secartist.lower() in stuff['name'].lower()) or (stuff['name'].lower() in secartist.lower()):

							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool and apple: #try again but with different query, search using album name
				url = item[(item.find(' |URL|:') + 7):]
				albumpage = requests.get(url)
				albumhtml = BeautifulSoup(albumpage.text, 'html.parser')
				album = albumhtml.find(id = 'shoebox-ember-data-store').get_text()
				albdic = json.loads(album)
				albumname = albdic['data']['attributes']['name']
				query = trackname + artistname + " " + albumname
				query = query.replace("  "," ")
				searchprim = spotifyObject.search(query, type = "track" , limit = 1)

				for thing in searchprim['tracks']['items']:
					addbool = False

					for stuff in thing['artists']:

						if (artistname.lower() in stuff['name'].lower()) or (stuff['name'].lower() in artistname.lower()):
							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool and apple and (" & " in artistname or ("(" in trackname and ")" in trackname)): #try again but with different query, search using album name
				url = item[(item.find(' |URL|:') + 7):]
				albumpage = requests.get(url)
				albumhtml = BeautifulSoup(albumpage.text, 'html.parser')
				album = albumhtml.find(id = 'shoebox-ember-data-store').get_text()
				albdic = json.loads(album)
				albumname = albdic['data']['attributes']['name']
				secquery = sectrack + secartist + " " + albumname
				secquery = secquery.replace("  "," ")
				searchsec = spotifyObject.search(secquery, type = "track" , limit = 1)

				for thing in searchsec['tracks']['items']:
					addbool = False

					for stuff in thing['artists']:

						if (secartist.lower() in stuff['name'].lower()) or (stuff['name'].lower() in secartist.lower()):

							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool and tidal: #try again but with different query

				album = item[(item.find(' |URL|: ') + 7):]
				query = trackname + artistname + " " + album
				query = query.replace("  "," ")
				searchprim = spotifyObject.search(query, type = "track" , limit = 1)

				for thing in searchprim['tracks']['items']:
					addbool = False

					for stuff in thing['artists']:

						if (artistname.lower() in stuff['name'].lower()) or (stuff['name'].lower() in artistname.lower()):
							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool and tidal and (" & " in artistname or ("(" in trackname and ")" in trackname)): #try again but with different query
				album = item[(item.find(' |URL|: ') + 7):]
				secquery = sectrack + secartist + " " + album
				secquery = secquery.replace("  "," ")
				searchsec = spotifyObject.search(secquery, type = "track" , limit = 1)
				for thing in searchsec['tracks']['items']:
					addbool = False

					for stuff in thing['artists']:

						if (secartist.lower() in stuff['name'].lower()) or (stuff['name'].lower() in secartist.lower()):

							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool: #if no search attempts worked, add song to list of missed songs
				misses.append(retquery)

			exactpercent = ((65) / length) + exactpercent
			displaypercent = int(exactpercent)
			if displaypercent > 80: #about 80% done here
				displaypercent = 80
			yield "data:" +str(displaypercent) + "\n\n"

		if firstls: #make list of lists, each sublist is up to 100 tracks (Spotify only allows 100 at a time)
			idlist.append(firstls)

	idlength = len(idlist)
	for item in idlist: #add songs to playlist
		spotifyObject.user_playlist_add_tracks(userid, plid, item)

		exactpercent = ((20) / idlength) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 100:
			displaypercent = 100
		yield "data:" +str(displaypercent) + "\n\n"
		
	yield "data:100\n\n"

	urlstring = 'https://open.spotify.com/user/%s/playlist/%s' % (userid, str(plid))  #link to playlist
	
	yield "data:URL"+urlstring+"\n\n"

	for item in misses:
		yield "data:MISS"+item+"\n\n"

	yield "data:NAME"+name+"\n\n"
	
	yield "data:COMPLETE\n\n"