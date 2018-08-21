from spotipy import oauth2, Spotify
import json
import requests
import app.spotifyapi

from bs4 import BeautifulSoup

def removeParen(s):
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

def removeBrack(s):
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


def spotify_playlist(token, service, url):
	
	apple = service == 'apple'
	tidal = service == 'tidal'

	if apple:
		import app.appcrawl
		try:
			indict = app.appcrawl.get_artists_tracks(url)
		except:
			yield "data:ERROR\n\n"
			return None

	elif tidal:
		import app.tidapi
		try:
			indict = app.tidapi.tidal_to_dict(url)
		except:
			yield "data:ERROR\n\n"
			return None
	
	else:
		yield "data:ERROR\n\n"
		return None
	yield "data: 10\n\n"

	spotifyObject = Spotify(auth = token)
	user = spotifyObject.current_user()
	userid = user['id']

	idlist = []

	name = indict['Name']
	description = indict['Description']
	headers = {'Authorization': 'Bearer {0}'.format(token)}
	headers['Content-Type'] = 'application/json'
	data = {'name': name, 'public': 'True', 'description': description}
	r = spotifyObject._internal_call('POST',"users/%s/playlists" % userid, data, None)

	plid = r['id']
	misses = []
	yield "data: 15\n\n"

	displaypercent = 15
	exactpercent = 15.0
	length = len(indict['Tracks'])

	for i in range(length // 100 + 1):
		firstls = []

		for item in indict['Tracks'][(100 * i): ((i + 1) * 100)]:
			searchsec = ""
			artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')]
			trackname = item[(item.find('|Track|:') + 9):item.find('|Artist|:')] 
			query = trackname + artistname
			query = query.replace("  "," ")
			retquery = artistname + ' - ' + trackname
			searchprim = spotifyObject.search(query, type = "track" , limit = 2)

			addbool = False
			for thing in searchprim['tracks']['items']:
				
				for stuff in thing['artists']:

					if (artistname.lower() in stuff['name'].lower()) or (stuff['name'].lower() in artistname.lower()):
						firstls.append(thing['id'])
						addbool = True
						break

				if addbool:
					break

			if not addbool and (" & " in artistname or ("(" in trackname and ")" in trackname)):

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

				for thing in searchsec['tracks']['items']:
					addbool = False

					for stuff in thing['artists']:

						if (secartist.lower() in stuff['name'].lower()) or (stuff['name'].lower() in secartist.lower()):

							firstls.append(thing['id'])
							addbool = True
							break

					if addbool:
						break

			if not addbool and apple:
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

			if not addbool and apple and (" & " in artistname or ("(" in trackname and ")" in trackname)):
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

			if not addbool and tidal:

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

			if not addbool and tidal and (" & " in artistname or ("(" in trackname and ")" in trackname)):
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

			if not addbool:
				misses.append(retquery)

			exactpercent = ((65) / length) + exactpercent
			displaypercent = int(exactpercent)
			if displaypercent > 80:
				displaypercent = 80
			yield "data:" +str(displaypercent) + "\n\n"

		if firstls:
			idlist.append(firstls)

	idlength = len(idlist)
	for item in idlist:
		spotifyObject.user_playlist_add_tracks(userid, plid, item)

		exactpercent = ((20) / idlength) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 100:
			displaypercent = 100
		yield "data:" +str(displaypercent) + "\n\n"
		
	yield "data:100\n\n"

	urlstring = 'https://open.spotify.com/user/%s/playlist/%s' % (userid, str(plid))
	# print(misses)
	yield "data:URL"+urlstring+"\n\n"

	for item in misses:
		yield "data:MISS"+item+"\n\n"

	yield "data:NAME"+name+"\n\n"
	
	yield "data:COMPLETE\n\n"

# print('yae')
#spotify_playlist('BQBnMi6sRmqpBvGoz9ZwOLt_MLV0vBHLEw4NWN5DhZiGvfCCjadpfeTf3JN1rZ49pQtPb-iq4WY5ya8L1FQQTi5GrBrrela2ONXCWO3he2uOMs8zHXMyCZLGmeKLph7AeEJL0D7mRFkXhznvIAkE8TrRx3nPmj9ZedNN54JQ2YcLtbbIGlYbZEMCDBjVTJcxWSkwBdxOXerHkm8', 'apple', 'https://itunes.apple.com/us/playlist/test/pl.u-06oxpyatJ8ZRd4')



