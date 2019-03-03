from flask import Flask

# Setting instance_relative_config=True will load configuration variables from an instance folder
# This instance folder will be kept out of version control

app = Flask(__name__, instance_relative_config=True)

# Variables defined in the instance/config.py file will override the value in config.py
# In order to use this functionality config calls must be in this order
app.config.from_object('config')
app.config.from_pyfile('config.py')

from app import routes