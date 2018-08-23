import tidalapi
from app.credentials import Credentials




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

def uncensor(s):
	firstind = s.find('*')
	count = firstind + 1
	lastind = firstind
	while True:
		if count == len(s):
			lastind = count - 1
			break
		if s[count] != '*':
			lastind = count - 1
			break
		count += 1

	if firstind > 0:
		if s[firstind - 1].lower() == 'n':
			return s[:firstind] + 'igga' + s[lastind + 1:]
		if s[firstind - 1].lower() == 's':
			return s[:firstind] + 'hit' + s[lastind + 1:]
		if s[firstind - 1].lower() == 'f':
			return s[:firstind] + 'uck' + s[lastind + 1:]
		if s[firstind - 1].lower() == 'h':
			return s[:firstind] + 'oe' + s[lastind + 1:]
		if s[firstind - 1].lower() == 'b':
			return s[:firstind] + 'itch' + s[lastind + 1:]

def urlsplit(url):
	urllist = url.split('/')
	return urllist[4]

def playlist_to_favs(playid, favs, session):
	for track in reversed(session.get_playlist_tracks(playid)):
		favs.add_track(track.id)

def track_to_favs(trackid, favs):
	favs.add_track(trackid)

def tidal_to_dict(url):
	cred = Credentials()
	session = tidalapi.Session()
	plid = urlsplit(url)
	print(cred.secret_key)
	session.login(cred.tidal_username, cred.tidal_password)
	retdict = {'Tracks' : [], 'Images' : []}
	playlist = session.get_playlist(plid)
	retdict['Name'] = playlist.name
	retdict['Description'] = playlist.description
	for item in session.get_playlist_tracks(plid):
		retdict['Tracks'].append("|Track|: " + item.name + ' |Artist|: ' + item.artist.name + ' |URL|: ' +  item.album.name)
		retdict['Images'].append(item.album.image)
	return(retdict)
	# print(len(session.get_playlist('83c220c1-18ba-493a-8f1f-cc3f44f8defe').description))
	# for item in session.get_playlist_tracks('96e5ef29-bbf6-44e0-927a-7cc4257e6003'):
	# 	print(item.album.image)

def dict_to_tidal(username, password, url,service):

	idlist = []
	misses = []

	apple = service == 'apple'
	spotify = service == 'spotify'

	if apple:
		import app.appcrawl
		try:
			indict = app.appcrawl.get_artists_tracks(url)
		except:
			yield "data:ERROR\n\n"
			return None

	elif spotify:
		import app.spotifyapi
		try:
			indict = app.spotifyapi.get_artists_tracks(url)
		except:
			yield "data:ERROR\n\n"
			return None
	
	else:
		yield "data:ERROR\n\n"
		return None

	session = tidalapi.Session()
	session.login(username, password)
	favs = tidalapi.Favorites(session,session.user.id)

	yield "data: 20\n\n"
	displaypercent = 20
	exactpercent = 20.0
	length = len(indict['Tracks'])
	for item in indict['Tracks']:
		artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')]
		trackname = item[(item.find('|Track|:') + 9):item.find('|Artist|:')] 
		query = trackname + artistname
		query = query.replace("  "," ")
		retquery = artistname + ' - ' + trackname
		# searches = session.search('track', query, limit = 3)
		searches = session.search('track', query)
		miss = True
		# print(query)
		# print()
		# print(searches.tracks)
		# print()
		for thing in searches.tracks:
		
			if thing.artist.name.lower() == artistname.lower():
				
				idlist.append(str(thing.id))
				miss = False
				break

		else:
			if '-' in trackname:
				# searches = session.search('track', trackname[:trackname.find('-')] + artistname, limit = 3)
				searches = session.search('track', trackname[:trackname.find('-')] + artistname)
				for stuff in searches.tracks:
					if stuff.artist.name.lower() == artistname.lower():
						idlist.append(str(stuff.id))
						miss = False
						break
			if miss and " & " in artistname or ("(" in trackname and ")" in trackname):
				# print(item)
				# print()
				# print(searchsec)
				secartist = artistname
				sectrack = trackname
				if " & " in artistname:
					secartist = artistname[:artistname.find(" & ")]
					if ',' in secartist:
						secartist = secartist[:secartist.find(",")]

				if "(" in trackname and ")" in trackname:
					sectrack = removeParen(trackname)
				if "[" in trackname and "]" in trackname:
					sectrack = removeBrack(trackname)
				secquery = sectrack + secartist
				secquery = secquery.replace("  "," ")
				# searchsec = session.search('track', secquery , limit = 3)
				searches = session.search('track', trackname[:trackname.find('-')] + artistname)

				for stuff in searchsec.tracks:

					if stuff.artist.name.lower() == secartist.lower():
						idlist.append(str(stuff.id))
						miss = False
						break
			if '*' in trackname:
				trackname = uncensor(trackname)
				query = trackname + artistname
				query = query.replace("  "," ")
				# searches = session.search('track', query, limit = 3)
				searches = session.search('track', query)
				for stuff in searches.tracks:
					if stuff.artist.name.lower() == artistname.lower():
						idlist.append(str(stuff.id))
						miss = False
						break


		if miss:
			misses.append(retquery)

		exactpercent = ((50) / length) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 70:
			displaypercent = 70
		yield "data:" +str(displaypercent) + "\n\n"

	idlength = len(idlist)
	for item in reversed(idlist):
		try:
			track_to_favs(item, favs)
		except:
			yield "data: ERROR\n\n"
		exactpercent = ((30) / idlength) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 100:
			displaypercent = 100
		yield "data:" +str(displaypercent) + "\n\n"	

	yield "data:100\n\n"	

	urlstring = 'https://listen.tidal.com/my-music/tracks' 

	yield "data:URL"+urlstring+"\n\n"
	for item in misses:
		yield "data:MISS"+item+"\n\n"

	yield "data:NAME"+indict['Name']+"\n\n"
	
	yield "data:COMPLETE\n\n"


# print(tidal_to_dict('https://listen.tidal.com/playlist/26aba6ef-3d57-47f7-8380-97badde90212'))
#print(dict_to_tidal('s','s', 'https://itunes.apple.com/us/playlist/test/pl.u-06oxpyatJ8ZRd4'))
