import json
from flask import Flask, request, redirect, g, render_template, url_for, session
import requests
import base64
import urllib
import six
# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response. 


app = Flask(__name__)
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

#  Client Keys
CLIENT_ID = 'ad51d663334348ad9e1542167cf88d24'
CLIENT_SECRET = '9d2cc2c091664191a1b12a75255a7e96'

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}
truestat = True

@app.route("/")
def index():
    # Auth Step 1: Authorization
    
    # if 'truestat' not in session:
    #     session['truestat'] = True

    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    print(url_args)
    print(request.args)
    print()
    # print(session['truestat'])
    # if session['truestat']:
        
    return redirect(auth_url)
    # else:
    #     return('flask.html')


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    print()
    print(request.args)
    print()
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    print(auth_token)
    base64encoded = base64.b64encode(six.text_type(CLIENT_ID + ':' + CLIENT_SECRET).encode('ascii'))
    # base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    # print(base64encoded)
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('ascii'))}
    # print(headers)
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers, verify = True)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    
    # Combine profile and playlist data to display
    display_arr = [profile_data] + playlist_data["items"]
    return render_template("git.html",sorted_array=display_arr)

if __name__ == "__main__":
    app.run(debug=True,port=PORT)