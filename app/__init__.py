from flask import Flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from whitenoise import WhiteNoise
from config import Config



def create_app(config_class=Config): #create app blueprint to as framework

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')
   

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

