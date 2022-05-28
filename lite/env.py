"""
Made by Cyclone and other Contributers.
This code is under the CC0 1.0 License
"""

import os, sys
import logging
import secrets
import sched
import time
import requests

class Enviroment:
    def __init__(self, path, src, shared) -> None:
        self.name = path.split(".")[0]
        self.path = path
        
        self.secret = secrets.token_urlsafe(16) # This is so other plugins cannot edit/transmit to others

        shared.flow["plugins"][self.secret] = {}
        self.flow = shared.flow["plugins"][self.secret]
        self.flow_path = f"plugins.{self.secret}"
        
        self.pages = {
        }

        env = {
            "plugin": self,
            "flow": self.flow,
            "server": False,
            "lite": True
        }

        exec(compile(src, path, "exec"), env, {})

    def create_loop(self):
        # Thanks to https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
        return sched.scheduler(time.time, time.sleep)

class Deployer:
    def __init__(self, shared) -> None:
        if not os.path.exists("plugins"): # Creates plugins folder if not done already
            os.mkdir("plugins")

        sources = {}
        self.enviroments = []

        shared.logging.info("Reading Plugins")
        for i in os.listdir("plugins"): # Lists plugins and read them all, then sends them in a dict
            with open(f"plugins/{i}") as f:
                sources[i] = f.read()

        shared.logging.info("Initializing Plugins")
        for i in sources:
            self.enviroments.append(Enviroment(i, sources[i], shared))