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

# def get_authenticated_service():
#   flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#   credentials = flow.run_console()
#   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

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
  # print(resource)
  return resource

def playlist_items_insert(client, properties, **kwargs):
  # See full sample for function
  resource = build_resource(properties)

  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.playlistItems().insert(
    body=resource,
    **kwargs
  ).execute()


    
def add_playlist(youtube, pl):
  
  body = dict(
    snippet=dict(
      title=pl['Name'],
      description=pl['Description']
    ),
    status=dict(
      privacyStatus='public'
    ) 
  ) 
    
  playlists_insert_response = youtube.playlists().insert(
    part='snippet,status',
    body=body
  ).execute()

  yield "data:75\n\n"
  idlength = len(pl['IDs'])
  for item in pl['IDs']:
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

  return playlists_insert_response['id']





def get_playlist_dict(youtube, url, service):
  
  
  apple = service == 'apple'
  tidal = service == 'tidal'
  spotify = service == 'spotify'

  if apple:
    import app.appcrawl
    try:
      retdict = app.appcrawl.get_artists_tracks(url)
    except:
      yield "data:ERROR\n\n"
      return None

  elif tidal:
    import app.tidapi
    try:
      retdict = app.tidapi.tidal_to_dict(url)
    except:
      yield "data:ERROR\n\n"
      return None

  elif spotify:
    import app.spotifyapi
    try:
      retdict = app.spotifyapi.get_artists_tracks(url)
    except:
      yield "data:ERROR\n\n"
      return None

  else:
    yield "data:ERROR\n\n"
    return None

  yield "data:20\n\n"
  retdict['IDs'] = []
  # retdict = {'Name' : searchdict['Name'], 'Description' : searchdict['Description'], 'IDs' : [] , "Images" : searchdict['Images']}
  displaypercent = 20
  exactpercent = 20.0
  length = len(retdict['Tracks'])
  
  for item in retdict['Tracks']:
    artistname = item[(item.find('|Artist|:') + 10):item.find(' |URL|:')]
    trackname = item[(item.find('|Track|:') + 9):item.find(' |Artist|:')] 
    query = trackname + " " + artistname 
    yield "data:SONG" + artistname + " - " + trackname + "\n\n"
    #query = item[(item.find('|Track|:') + 9):item.find('|Artist|:')] + item[(item.find('|Artist|:') + 10):]
    payload = {'type': 'video', 'q': (query +' ' + 'video')  ,'key' : 'AIzaSyCzW8ySMW-rvjItMk9s-RbIk4p2DeGZooU','maxResults': 1 , 'part' : 'snippet' }
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params = payload )
    retdict['IDs'].append(r.json()['items'][0]['id']['videoId'])
    exactpercent = ((50) / length) + exactpercent
    displaypercent = int(exactpercent)
    if displaypercent > 70:
      displaypercent = 70
    yield "data:" +str(displaypercent) + "\n\n"

  # add_playlist(youtube, retdict)
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
  for item in retdict['Images']:
      yield "data:IMAGE" + item + "\n\n"
      if item in colordict:
        yield "data:COLOR" + colordict[item] + "\n\n"
      else:
        colorstr = app.color.avgcolor(item)
        colordict[item] = colorstr
        yield "data:COLOR" + colorstr + "\n\n"


  #ls = ['[' + str(len(retdict['IDs'])), retdict['IDs'], retdict['Name']]

  for item in retdict['IDs']:
      yield "data:IDS" + str(item) + "\n\n"

  yield "data:NAME" + retdict['Name'] + "\n\n"

  try: 
    straa= "";
    playlists_insert_response = youtube.playlists().insert(
      part='snippet,status',
      body=body).execute()

  except HttpError:
    #print('create error')
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

  # if playlists_insert_response:
  urlstring = 'https://www.youtube.com/playlist?list=%s' % playlists_insert_response['id']
  # urlstring = 'sads'
  yield "data:URL" +urlstring + "\n\n"

  yield "data:COMPLETE\n\n"
  # print(playlists_insert_response['id'])



