from flask import Flask
import logging

app = Flask(__name__)
# Logging disabled on console as the shell client runs simultanously
log = logging.getLogger('werkzeug')
log.disabled = True

from app import routes