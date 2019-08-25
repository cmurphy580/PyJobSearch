from flask import Flask
from app.config import Config

application = Flask(__name__)
application.config.from_object(Config)
application.debug = True
application.templates_auto_reload = True

from app import routes
