import json

import asana

from dotty import board

class AsanaBoard(board.Board):
    """ Asana implementation of Board abstract base class. """
    def __init__(self, token):
        self.token = token

    def load(self):
        client = asana.Client.access_token(self.token)
        me = client.users.me()
        print(json.dumps(me))
