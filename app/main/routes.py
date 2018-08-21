from flask import Flask, request, render_template, url_for, session, redirect, Response, current_app
import app.spotifyapi
import app.ytcreate 
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import app.mySpotify
import base64
import urllib
import six
import requests
import json
import app.appcrawl
import app.tidapi
from app.main import bp
from app.main.form import Form


API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


YT_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl' , 'https://www.googleapis.com/auth/youtube']

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
SPOTIFY_API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, SPOTIFY_API_VERSION)


# Server-side Parameters
# CLIENT_SIDE_URL = "http://localhost"
# PORT = 8090
SOURCE_URL = 'https://replaylist-app.herokuapp.com'
# REDIRECT_URI = "%s/callback/q" % SOURCE_URL
CLIENT_SIDE_URL = "http://localhost"
PORT = 8090
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_str = "true"




# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@bp.route('/')
def my_form():
	
	return render_template("test.html")

@bp.route('/', methods=['POST'])
def my_form_post():
  
	current_app.config['url'] = request.form['url']
  	session['url'] = request.form['url']
	if request.method == "POST":
		
		if request.form.get('top') is not None:
	      # formboy.top = request.form.get('top')
			current_app.config['top'] = request.form.get('top')
			session['top'] = request.form.get('top')

		if request.form.get('bottom') is not None:
	      #formboy.bottom = request.form.get('bottom')
			current_app.config['bottom'] = request.form.get('bottom')
			session['bottom'] = request.form.get('bottom')
	      
	    # if formboy.bottom == 'spotify':
	    print(session['bottom'])
		if current_app.config['bottom'] == 'spotify':
			auth_query_parameters = {
   				"response_type": "code",
    			"redirect_uri": REDIRECT_URI,
    			"scope": SCOPE,
    			# "state": STATE,
    			"show_dialog": SHOW_DIALOG_str,
    			"client_id": current_app.config['CLIENT_ID']
}
			url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
			auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
			return redirect(auth_url)

    # if formboy.bottom == 'tidal':
	if current_app.config['bottom'] == 'tidal':
		return redirect(url_for('main.tidal_auth'))

    #if formboy.bottom == 'youtub':
	if current_app.config['bottom'] == 'youtub':
		return redirect('/authorize')
	
	return redirect(url_for('main.my_form'))

@bp.route('/auth')
def tidal_auth():
	
	return render_template('tidal.html')

@bp.route('/auth', methods=['GET','POST'])
def tidal_auth_post():

	if request.method == "POST":
		
		current_app.config['username'] = request.form['username']
		current_app.config['password'] = request.form['password']
		return redirect(url_for('main.final'))

	return render_template('tidal.html')
# @app.route('/tidal')
# def tid():

#   return render_template('ind.html')

@bp.route("/callback/q")
def callback():

	auth_token = request.args['code']
	code_payload = {
		"grant_type": "authorization_code",
		"code": str(auth_token),
		"redirect_uri": REDIRECT_URI
	}
	base64encoded = base64.b64encode(six.text_type(current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET']).encode('ascii'))
	headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
	post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers, verify = True)
	response_data = json.loads(post_request.text)
	access_token = response_data["access_token"]
	current_app.config['auth'] = access_token

	return redirect(url_for("main.final"))
   
@bp.route('/complete')
def final():
  #return render_template('ind.html', bottom = formboy.bottom, top = formboy.top)
	return render_template('ind.html', bottom = current_app.config['bottom'], top = current_app.config['top'])

@bp.route('/progress')
def progress():
  
  # if formboy.bottom == 'spotify':
  #   return Response(mySpotify.spotify_playlist(formboy.auth, formboy.top ,formboy.url), mimetype= 'text/event-stream')

	if current_app.config['bottom'] == 'spotify':
		return Response(app.mySpotify.spotify_playlist(current_app.config['auth'], current_app.config['top'] ,current_app.config['url']), mimetype= 'text/event-stream')

  # if formboy.bottom == 'tidal':
  #   return Response(tidapi.dict_to_tidal(formboy.username, formboy.password, formboy.url, formboy.top), mimetype= 'text/event-stream')

	if current_app.config['bottom'] == 'tidal':
		return Response(app.tidapi.dict_to_tidal(current_app.config['username'], current_app.config['password'], current_app.config['url'], current_app.config['top']), mimetype= 'text/event-stream')

  # if formboy.bottom == 'youtub':
  #   try:
  #     credentials = google.oauth2.credentials.Credentials(**session['credentials'])

  #   except: 
  #     return render_template('error.html')

  #   formboy.ytclient = googleapiclient.discovery.build(API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

  #   return Response(ytcreate.get_playlist_dict(formboy.ytclient, formboy.url, formboy.top), mimetype= 'text/event-stream')

	if current_app.config['bottom'] == 'youtub':
		try:
			credentials = google.oauth2.credentials.Credentials(**session['credentials'])

		except: 
			return render_template('error.html')

	current_app.config['ytclient'] = googleapiclient.discovery.build(API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

	return Response(app.ytcreate.get_playlist_dict(current_app.config['ytclient'], current_app.config['url'], current_app.config['top']), mimetype= 'text/event-stream')


@bp.route('/authorize')
def authorize():
  # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
  # steps.
	
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	current_app.config['CLIENT_SECRETS_FILE'], scopes=YT_SCOPES)
	
	flow.redirect_uri = url_for('main.oauth2callback', _external=True)
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

@bp.route('/oauth2callback')
def oauth2callback():
# Specify the state when creating the flow in the callback so that it can
# verify the authorization server response.
	
	state = session['state']
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
		current_app.config['CLIENT_SECRETS_FILE'], scopes=YT_SCOPES, state=state)
	flow.redirect_uri = url_for('main.oauth2callback', _external=True)
	
# Use the authorization server's response to fetch the OAuth 2.0 tokens.
	authorization_response = request.url
	
	try:
		print('there')
		print(current_app.config['top'])
		print(current_app.config['bottom'])
		flow.fetch_token(authorization_response=authorization_response)
		
	except:
		print('here')
		print(current_app.config['top'])
		print(current_app.config['bottom'])
		return render_template('error.html')

	
  
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

	return redirect(url_for('main.final'))

@bp.route('/report', methods=['GET','POST'])
def report():
	if request.method == "POST":
		
		email = request.form.get('bug')
		
		import yagmail
		#yagmail.register('antgraves24', 'mustang23')
		yag = yagmail.SMTP(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
		yag.send(to = "antgraves23@gmail.com", subject = "test", contents = email)
		return redirect(url_for('main.thanks'))
	return render_template('report.html')

@bp.route('/report-submission')
def thanks():
	return render_template('return.html')
