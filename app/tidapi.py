import tidalapi
from app.credentials import Credentials




def removeParen(s): #remove parentheses to optimize search
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

def removeBrack(s): #remove brackets to optimize search
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


def urlsplit(url):
	urllist = url.split('/')
	return urllist[4]

def playlist_to_favs(playid, favs, session): #add entire playlist to user's favorite tracks
	for track in reversed(session.get_playlist_tracks(playid)):
		favs.add_track(track.id)

def track_to_favs(trackid, favs): #add single track to user's favorite tracks
	favs.add_track(trackid)

def tidal_to_dict(url): #generate a dictionary of artists, tracks, and images given a Tidal url
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
	

def dict_to_tidal(username, password, url,service): #take in a dict from another service, add tracks to favorites

	idlist = []
	misses = []

	apple = service == 'apple'
	spotify = service == 'spotify'

	if apple:
		import app.appcrawl
		try:
			indict = app.appcrawl.get_artists_tracks(url)
		except:
			yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
			return None

	elif spotify:
		import app.spotifyapi
		try:
			indict = app.spotifyapi.get_artists_tracks(url)
		except:
			yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
			return None
	
	else:
		yield "data:ERROR\n\n" #yield error, stop program, something wrong on my end
		return None

	session = tidalapi.Session() #create Tidal session
	session.login(username, password)
	favs = tidalapi.Favorites(session,session.user.id)

	yield "data: 20\n\n" #about 20% done
	displaypercent = 20
	exactpercent = 20.0
	length = len(indict['Tracks'])
	for item in indict['Tracks']: #begin adding songs ids to be added to favs
		artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')] #search queries
		trackname = item[(item.find('|Track|:') + 9):item.find('|Artist|:')] 
		query = trackname + artistname
		query = query.replace("  "," ")
		retquery = artistname + ' - ' + trackname
		searches = session.search('track', query)
		miss = True
		
		for thing in searches.tracks:
		
			if thing.artist.name.lower() == artistname.lower():
				
				idlist.append(str(thing.id)) #add id
				miss = False
				break

		else: #search again using different queries
			if '-' in trackname:
				searches = session.search('track', trackname[:trackname.find('-')] + artistname)
				for stuff in searches.tracks:
					if stuff.artist.name.lower() == artistname.lower():
						idlist.append(str(stuff.id))
						miss = False
						break
			if miss and " & " in artistname or ("(" in trackname and ")" in trackname):
				
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
				
				searchsec = session.search('track', secquery )

				for stuff in searchsec.tracks:

					if stuff.artist.name.lower() == secartist.lower():
						idlist.append(str(stuff.id))
						miss = False
						break
			if '*' in trackname:
				trackname = uncensor(trackname)
				query = trackname + artistname
				query = query.replace("  "," ")
				searches = session.search('track', query)
				for stuff in searches.tracks:
					if stuff.artist.name.lower() == artistname.lower():
						idlist.append(str(stuff.id))
						miss = False
						break


		if miss: #add all missed songs to a list
			misses.append(retquery)

		exactpercent = ((50) / length) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 70:
			displaypercent = 70
		yield "data:" +str(displaypercent) + "\n\n" #about 70% done

	idlength = len(idlist)
	for item in reversed(idlist): #reverse; Tidal adds songs backwards
		try:
			track_to_favs(item, favs) #add track
		except:
			yield "data: ERROR\n\n"
		exactpercent = ((30) / idlength) + exactpercent
		displaypercent = int(exactpercent)
		if displaypercent > 100:
			displaypercent = 100 #we're done
		yield "data:" +str(displaypercent) + "\n\n"	

	yield "data:100\n\n"	

	urlstring = 'https://listen.tidal.com/my-music/tracks' 

	yield "data:URL"+urlstring+"\n\n" #link to URL
	for item in misses:
		yield "data:MISS"+item+"\n\n"

	yield "data:NAME"+indict['Name']+"\n\n"
	
	yield "data:COMPLETE\n\n"
