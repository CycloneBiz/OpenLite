from flask import render_template
import openloop
import requests

def ping():
    try:
        d = requests.get("https://httpbin.org/get").json()
        return d.get("origin", "No Origin")
    except:
        return False

class Webserver:
    def __init__(self, app, logs, share) -> None:
        @app.route("/")
        def index():
            if share.database.working:
                try:
                    share.database.client.server_info()
                    mongo = True
                except:
                    mongo = False
            else:
                mongo = False
            return render_template(
                "index.html",
                version = f"{openloop.comb_code} ({openloop.num*10}/{openloop.code})",
                logs=logs,
                mongo = mongo,
                online = ping(),
                plugins = len(share.plugins.enviroments)
            )