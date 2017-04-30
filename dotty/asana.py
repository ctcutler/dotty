import configparser
import json

import asana

from dotty import board

class AsanaBoard(board.Board):
    """ Asana implementation of Board abstract base class. """
    def __init__(self, config_file):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_file)

    def load(self):
        token = self.cfg['asana']['AsanaAccessToken']
        client = asana.Client.access_token(token)
        me = client.users.me()
        print(json.dumps(me))
