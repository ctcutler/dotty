from datetime import datetime
import json
import re

import asana

from dotty import board

ADD_RE = re.compile(r'^added to (?P<board>.+)$')
MOVE_RE = re.compile(r'^moved from (?P<from_column>.+) to (?P<column>.+) \((?P<board>.+)\)$')

def iso8601_to_epoch(iso_string):
    dt = datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    epoch_diff = dt - datetime(1970, 1, 1)
    return epoch_diff.total_seconds()

def is_relevant(board_name, story):
    if story['type'] != 'system':
        return False

    match = ADD_RE.search(story['text']) or MOVE_RE.search(story['text'])

    if not match:
        return False

    board = match.groupdict().get('board')

    if board != board_name:
        return False

    return True

def history_item(story):
    match = ADD_RE.search(story['text']) or MOVE_RE.search(story['text'])
    column = match.groupdict().get('column')
    ts = iso8601_to_epoch(story['created_at'])

    return { 'ts': ts, 'column': column }

def set_start_column(history, stories):
    '''
    The first story doesn't mention a column so we have to update the first
    item in the history based on the *from* column of the second story
    (the first move).
    '''
    if len(stories) < 2:
        return history

    story = stories[1]
    match = MOVE_RE.search(story['text'])

    if not match:
        return history

    column = match.groupdict().get('from_column')
    new_item = history[0].copy()
    new_item['column'] = column

    return [new_item] + history[1:]

def task_history(board_name, stories):
    '''
    Converts a list of task stories to a history of that task.

    See unit tests for examples.
    '''
    sorted_stories = sorted(stories, key=lambda s: s['created_at'])
    relevant_stories = list(
        filter(lambda s: is_relevant(board_name, s), sorted_stories)
    )
    history = list(map(history_item, relevant_stories))
    return set_start_column(history, relevant_stories)

def task_dot_count(history):
    return 4

class AsanaBoard(board.Board):
    ''' Asana implementation of Board abstract base class. '''
    def __init__(self, token, board_id):
        self.token = token
        self.board_id = board_id

    def load(self):
        client = asana.Client.access_token(self.token)
        project = client.projects.find_by_id(self.board_id)
        for task in client.tasks.find_by_project(self.board_id):
            # skip sections
            if task['name'].endswith(':'):
                continue
            print()
            print(task['name'])
            stories = client.tasks.stories(task['id'])
            history = task_history(project['name'], stories)
            print(history)
            dot_count = task_dot_count(history)
            print(dot_count)
