from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['MAIL_USERNAME'] = "antgraves23@gmail.com"
app.config['MAIL_PASSWORD'] = "APrepAtPrep23"
app.config['DEFAULT_SENDER'] = "antgraves23@gmail.com"
mail = Mail(app)
# print(mail.config)


@app.route("/")
def index():
	msg = Message("Hello", recipients=app.config['MAIL_USERNAME'])
	mail.send(msg)
	return "SENT"

if __name__ == '__main__':
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	app.run('localhost', 8090, debug=True)