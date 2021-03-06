import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.credentials import Credentials 


def get_user_id(url): #gets user id from url
	end = url[url.find('user/') + 5:]
	return end[:end.find('/')]

def get_artists_tracks(url): #generate dictionary with playlist's name, description, tracks, and artworks

	cred = Credentials()
	client_id = cred.spotify_client_id
	client_secret = cred.spotify_client_secret

	userid = get_user_id(url)
	client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	returndict = {'Tracks' : [], 'Images' : []}
	playlist = sp.user_playlist(userid,url)
	returndict['Description'] = playlist['description']
	returndict['Name'] = playlist['name']
	
	for item in playlist['tracks']['items']:
		returndict['Tracks'].append("|Track|: " + str(item['track']['name']) + ' |Artist|: ' + str(item['track']['artists'][0]['name'] + ' |URL|:'))
		returndict['Images'].append(item['track']['album']['images'][0]['url'])
		
	return returndict



