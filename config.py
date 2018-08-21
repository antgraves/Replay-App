import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
# print(os.path.join(basedir, '.env'))
#b'6T\xbavE\xb3\xbe\xf8\xd0\xf1\xce\xd6(\x7f\x95\x1f\xa6\xf0\xc3\x89\xcb\xaa\xa2\xa7'
# print(os.environ.get('CLIENT_ID'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    TIDAL_USERNAME = os.environ.get('TIDAL_USERNAME')
    TIDAL_PASSWORD = os.environ.get('TIDAL_PASSWORD')
    CLIENT_SECRETS_FILE = 'client_secret_file.json'