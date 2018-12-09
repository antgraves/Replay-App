import requests
import json
from bs4 import BeautifulSoup
import argparse
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import app.color

CLIENT_SECRETS_FILE = 'client_secret1.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  
  return resource

def playlist_items_insert(client, properties, **kwargs):
  
  resource = build_resource(properties)

  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().insert(
    body=resource,
    **kwargs
  ).execute()

def get_playlist_dict(youtube, url, service): #generate youtube playlist
  
  apple = service == 'apple'
  tidal = service == 'tidal'
  spotify = service == 'spotify'

  if apple:
    import app.appcrawl
    try:
      retdict = app.appcrawl.get_artists_tracks(url)
    except:
      yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
      return None

  elif tidal:
    import app.tidapi
    try:
      retdict = app.tidapi.tidal_to_dict(url)
    except:
      yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
      return None

  elif spotify:
    import app.spotifyapi
    try:
      retdict = app.spotifyapi.get_artists_tracks(url)
    except:
      yield "data:ERROR\n\n" #yield error, stop program, user imput wrong URL
      return None

  else:
    yield "data:ERROR\n\n" #yield error, stop program, something wrong on my end
    return None

  yield "data:20\n\n" #about 20% done
  retdict['IDs'] = []
  displaypercent = 20
  exactpercent = 20.0
  length = len(retdict['Tracks'])
  
  for item in retdict['Tracks']: #get video ids
    artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')]
    trackname = item[(item.find('|Track|:') + 9):item.find(' |Artist|:')] 
    query = trackname + " " + artistname 
    
    
    payload = {'type': 'video', 'q': (query +' ' + 'video')  ,'key' : 'MYAPIKEY','maxResults': 1 , 'part' : 'snippet' }
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params = payload ) #perform search

    if len(r.json()['items']) > 0: #check if video exists
      retdict['IDs'].append(r.json()['items'][0]['id']['videoId'])
      yield "data:SONG" + artistname + " - " + trackname + "\n\n"
    else:
      retdict['IDs'].append('')
      retdict['Images'][len(retdict['IDs']) - 1] = ""
    exactpercent = ((50) / length) + exactpercent
    displaypercent = int(exactpercent)
    if displaypercent > 70:
      displaypercent = 70 #70% done
    yield "data:" +str(displaypercent) + "\n\n"

  body = dict(
    snippet=dict(
      title=retdict['Name'],
      description=retdict['Description']
    ),
    status=dict(
      privacyStatus='public'
    ) 
  ) 

  colordict = {}
  for item in retdict['Images']: #get average colors of track artwork
    if len(item) > 0:
      yield "data:IMAGE" + item + "\n\n"
      if item in colordict:
        yield "data:COLOR" + colordict[item] + "\n\n"
      else:
        colorstr = app.color.avgcolor(item)
        colordict[item] = colorstr
        yield "data:COLOR" + colorstr + "\n\n"

  for item in retdict['IDs']:
    if len(item) > 0:
      yield "data:IDS" + str(item) + "\n\n"

  yield "data:NAME" + retdict['Name'] + "\n\n"

  try:  #create playlist
    straa= "";
    playlists_insert_response = youtube.playlists().insert(
      part='snippet,status',
      body=body).execute()

  except HttpError: #app has exceded max playlist number for the day
    yield "data:100\n\n"
    yield "data:YTERROR\n\n"
    return None

  yield "data:75\n\n"
  displaypercent = 75
  exactpercent = 75.0
  idlength = len(retdict['IDs'])
  for item in retdict['IDs']:
    playlist_items_insert(youtube,{'snippet.playlistId': playlists_insert_response['id'],
         'snippet.resourceId.kind': 'youtube#video',
         'snippet.resourceId.videoId': item,
         'snippet.position': ''},
        part='snippet',
        onBehalfOfContentOwner='')

    exactpercent = ((25) / idlength) + exactpercent
    displaypercent = int(exactpercent)
    if displaypercent > 100:
      displaypercent = 100
    yield "data:" +str(displaypercent) + "\n\n" 

  yield "data:100\n\n"

  urlstring = 'https://www.youtube.com/playlist?list=%s' % playlists_insert_response['id'] #link to playlist
  yield "data:URL" +urlstring + "\n\n"

  yield "data:COMPLETE\n\n"