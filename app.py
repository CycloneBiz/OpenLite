import logging

logging.info("Loading OpenLite Loader")

from lite.loader import Loader
from flask import Flask

app = Flask(__name__)

load = Loader(app, logging)