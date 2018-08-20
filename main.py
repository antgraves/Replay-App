from flask import Flask, request, render_template, url_for, session, redirect, jsonify, flash, Response
import stringComparison
import spotifyapi
import ytcreate 
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from ytcreds import Secrets
from forms import Form
import os
from whitenoise import WhiteNoise
from flask_jsglue import JSGlue
import mySpotify
import base64
import urllib
import six
import requests
import json
import appcrawl
import tidapi
from werkzeug import secure_filename
from credentials import Credentials


API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
configy = Secrets()
app = Flask(__name__)
# jsglue = JSGlue(app)
# app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')


formboy = Form()
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# app.run(debug = True)


cred = Credentials()
app.secret_key = cred.secret_key

CLIENT_ID = cred.spotify_client_id
CLIENT_SECRET = cred.spotify_client_secret

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
SPOTIFY_API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, SPOTIFY_API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 8090
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_str = "true"


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route('/')
def my_form():
  return render_template("test.html")

@app.route('/', methods=['POST'])
def my_form_post():
 
  formboy.url = request.form['url']
  if request.method == "POST":

    if request.form.get('top') is not None:
      formboy.top = request.form.get('top')

    if request.form.get('bottom') is not None:
      formboy.bottom = request.form.get('bottom')
      
    if formboy.bottom == 'spotify':
      url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
      auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
      return redirect(auth_url)

    if formboy.bottom == 'tidal':
      return redirect(url_for('tidal_auth'))

    if formboy.bottom == 'youtub':
      return redirect('/authorize')
    
  return redirect(url_for('my_form'))

@app.route('/auth')
def tidal_auth():
  return render_template('tidal.html')

@app.route('/auth', methods=['GET','POST'])
def tidal_auth_post():

  if request.method == "POST":
    formboy.username = request.form['username']
    formboy.password = request.form['password']
    return redirect(url_for('final'))

  return render_template('tidal.html')

def index():
  return render_template("index.html")

# @app.route('/tidal')
# def tid():

#   return render_template('ind.html')

@app.route("/callback/q")
def callback():

    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode(six.text_type(CLIENT_ID + ':' + CLIENT_SECRET).encode('ascii'))
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers, verify = True)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    formboy.auth = access_token

    return redirect(url_for("final"))
   
@app.route('/complete')
def final():
  return render_template('ind.html', bottom = formboy.bottom, top = formboy.top)

@app.route('/progress')
def progress():
  
  if formboy.bottom == 'spotify':
    return Response(mySpotify.spotify_playlist(formboy.auth, formboy.top ,formboy.url), mimetype= 'text/event-stream')

  if formboy.bottom == 'tidal':
    return Response(tidapi.dict_to_tidal(formboy.username, formboy.password, formboy.url, formboy.top), mimetype= 'text/event-stream')

  if formboy.bottom == 'youtub':
    try:
      credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    except: 
      return render_template('error.html')

    formboy.ytclient = googleapiclient.discovery.build(API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

    return Response(ytcreate.get_playlist_dict(formboy.ytclient, formboy.url, formboy.top), mimetype= 'text/event-stream')


@app.route('/submit')
def submitted():
  credentials = google.oauth2.credentials.Credentials(**session['credentials'])
  print(credentials)
  formboy.ytclient = googleapiclient.discovery.build(API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
  #link = ytcreate.add_playlist(client, ytcreate.get_playlist_dict('https://open.spotify.com/user/1230065337/playlist/6Jdth5oqhKglLsuWAvdIZq'))
  return render_template("submit.html", link = link)
  # link = ytcreate.add_playlist(client, ytcreate.get_playlist_dict(formboy.url))
  # youtube = ytcreate.get_authenticated_service()
	# plagiarismPercent = stringComparison.stringcomp(text1)
	
	# if plagiarismPercent > 5 :
	# 	return "Plagiarism Detected !"
	# else :
	# 	return "<h1>No Plagiarism Detected !</h1>"

@app.route('/authorize')
def authorize():
  # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
  # steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      configy.CLIENT_SECRETS_FILE, scopes=configy.SCOPES)
  flow.redirect_uri = url_for('oauth2callback', _external=True)
  authorization_url, state = flow.authorization_url(
      # This parameter enables offline access which gives your application
      # both an access and refresh token.
      access_type='offline',
      # This parameter enables incremental auth.
      include_granted_scopes='true')

  # Store the state in the session so that the callback can verify that
  # the authorization server response.
  session['state'] = state

  # print('here ' + str(authorization_url))

  return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verify the authorization server response.
  state = session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      configy.CLIENT_SECRETS_FILE, scopes=configy.SCOPES, state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  print(type(authorization_response))
  try:
    flow.fetch_token(authorization_response=authorization_response)
  except:
    return render_template('error.html')

  # Store the credentials in the session.
  # ACTION ITEM for developers:
  #     Store user's access and refresh tokens in your data store if
  #     incorporating this code into your real app.
  credentials = flow.credentials
  session['credentials'] = {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes
  }

  # print(url_for('index'))

  return redirect(url_for('final'))

@app.route('/report', methods=['GET','POST'])
def report():
  if request.method == "POST":
    print(request.form.get('bug'))
    email = request.form.get('bug')
    print(email)
    import yagmail
    #yagmail.register('antgraves24', 'mustang23')
    yag = yagmail.SMTP('app.replay.me', 'Mustang23')
    yag.send(to = "antgraves23@gmail.com", subject = "test", contents = email)
    return redirect(url_for('thanks'))
  return render_template('report.html')

@app.route('/report-submission')
def thanks():
  return render_template('return.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('localhost', 8090, debug=True)


