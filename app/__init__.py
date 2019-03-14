from flask import Flask

# Setting instance_relative_config=True will load configuration variables from an instance folder
# This instance folder will be kept out of version control

app = Flask(__name__)

from app import routes

"""
This is a demo for later implementations

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')
"""