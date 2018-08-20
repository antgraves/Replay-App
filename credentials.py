import os




class Credentials(object):

	secret_key = os.urandom(24)
	tidal_username = "antgraves23@gmail.com"
	tidal_password = 'Mustang23'
	spotify_client_id = 'ad51d663334348ad9e1542167cf88d24'
	spotify_client_secret = '9d2cc2c091664191a1b12a75255a7e96'

	# def __init__(self, spotify_client_id = 'ad51d663334348ad9e1542167cf88d24', spotify_client_secret = '9d2cc2c091664191a1b12a75255a7e96'):
	#     self.spotify_client_id = spotify_client_id
	#     self.spotify_client_secret = spotify_client_secret
	#     # self.tidal_username = tidal_username
	#     # self.tidal_password = tidal_password