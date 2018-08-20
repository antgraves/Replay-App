# import spotipy
# import sys
# import spotipy.util as util

# # lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
# url = sys.argv[1]
# # trackid = url[(url.find('track') + 6):]

# # https://open.spotify.com/track/1dQ84P0W0lOckT02lPEhhP

# spotify = spotipy.Spotify(auth = 'BQCBz9eDRAmnMYyuwKllCu2dcxJlZABgkeUVLustrZoWMzMRr8axkfWMtViu54CaSXPnjkXXHZXj8CLSTyNrvmajuyldYyjW-9XZpi1181tUyqlDkP12uesGutfNeFy4GIkgZPjU3Ro9cwiQGR8dCo2kaGOQv4A')
# trackinfo = spotify.track(url)

# # print(type(trackinfo))
# print("Name: " + trackinfo['name'] + ", Artist: " + trackinfo['album']['artists'][0]['name'])
# # for track in results['tracks'][:10]:
# #     print('track    : ' + track['name'])
# #     print('audio    : ' + track['preview_url'])
# #     print('cover art: ' + track['album']['images'][0]['url'])
# #     print()

import pprint
import sys
import os
import subprocess

import spotipy
import spotipy.util as util


client_id = 'ad51d663334348ad9e1542167cf88d24'
client_secret = '9d2cc2c091664191a1b12a75255a7e96'
redirect_uri = 'https://www.google.com/'

scope = 'user-library-read'

# 1230065337 - id
def autho(username):
	if len(sys.argv) > 1:
	    username = sys.argv[1]
	else:
	    print("Usage: %s username" % (sys.argv[0]))
	    sys.exit()

	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

	if token:
	    sp = spotipy.Spotify(auth=token)
	    results = sp.current_user_saved_tracks()
	    for item in results['items']:
	        track = item['track']
	        print(track['name'] + ' - ' + track['artists'][0]['name'])
	else:
	    print ("Can't get token for", username)




