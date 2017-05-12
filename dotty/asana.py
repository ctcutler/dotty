import json

import asana

from dotty import board

def task_history(stories):
    return [story for story in stories]

class AsanaBoard(board.Board):
    """ Asana implementation of Board abstract base class. """
    def __init__(self, token, board_id):
        self.token = token
        self.board_id = board_id

    def load(self):
        client = asana.Client.access_token(self.token)
        for task in client.tasks.find_by_project(self.board_id):
            # skip sections
            if task['name'].endswith(':'):
                continue
            print()
            print(task['name'])
            stories = client.tasks.stories(task['id'])
            history = task_history(stories)
            print(json.dumps(history))
