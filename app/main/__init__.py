from flask import Blueprint
from app.main import form

bp = Blueprint('main', __name__)
formboy = form.Form()

from app.main import routes