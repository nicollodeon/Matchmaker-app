# what initializes everything
from flask import Flask, escape # make an instance of "Flask" from "flask" package
from config import Config       # from config packages import the Config class/instance
from flask_socketio import SocketIO, send, join_room, emit
import logging


# from pydantic import Basemodel, validator

#database stuff
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# keeping track of users logged in state
from flask_login import LoginManager


app = Flask(__name__)                       # assign initial app to be a flask object, __name__ is like an module environment variable
app.config.from_object(Config)              # tell app to use config.py
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)                        # make the database
migrate = Migrate(app, db)                  # make the migration software (i think can remove)
login = LoginManager(app)
login.login_view = 'login'                  # tells flask where the view function for handling logins is, allows forcing users to log in
logging.basicConfig(level=logging.DEBUG)

from app import routes, models, chat              # app here is the directory not the instance fo flask
                                            # routes are different urls that app handles
                                            # models is to define our db structure


