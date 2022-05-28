import requests, os
from time import sleep
import threading

class OpenLoop:
    def __init__(self, shared, url, auth) -> None:
        """Object that calls on OpenLoop via a cache design with threading"""
        self._shared = shared
        self._url = url
        self._auth = auth
        self.mongo = {}
        self.login_ok = True
        self.check_error = False
        self.server_version = 0

        self.check_in()

    def check_in(self):
        no_err = True

        try:
            data = requests.get(self._url+"/lite/check", auth=self._auth)
            json = data.json()
        except:
            no_err = False

        if data.ok and no_err:
            self.check_error = False
            self.mongo = json["config"]["mongo"]
            self.server_version = json["version"]
            self.login_ok = json["login"]
        else:
            self.check_error = True

    def refresh(self):
        if not self.check_error:
            data = requests.get(self._url+"")
        else:
            self._shared.logging.warn("Could not refresh due to being not checked in")