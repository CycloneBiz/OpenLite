from openloop.loader import load_data
from dotenv import load_dotenv
from flask import Flask
from os import getenv
from datetime import datetime
from openlite.pages import Webserver

global logs
logs = ["Logging below:"]

def add_log(string):
    logs.append(f"[{datetime.utcnow()}] {string}")

load_dotenv()
add_log("Loaded dotenv")

app = Flask(__name__)
share = load_data(app, {
    "lite": True,
    "Plugins": {
        "identity": getenv("OPENLOOP_IDENTITY", "lite"),
        "name": getenv("OPENLOOP_NAME", "Lite Device"),
        "id": getenv("OPENLOOP_ID", "self")
    },
    "MongoDB": {
        "uri": getenv("MONGODB_URI", "mongodb://localhost:27017"),
        "name": getenv("MONGODB_NAME", "OpenLoop")
    },
})

add_log("Finished Loading Core")

Webserver(app, logs, share)

add_log("Finished OpenLite extention")

if not share.database.working:
    add_log("MongoDB cannot connect")
    add_log("OpenLoop Core could not load MongoDB plugins")

app.run()