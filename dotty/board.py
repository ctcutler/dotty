# -*- coding: UTF-8 -*-

import time
import re

import asana

from dotty import helpers

DOT = '•'
# dots show up either as 'foo bar | •••' or as 'foo bar | • x 12'
DOTS_RE = re.compile(r'^.+ \| ('+DOT+'+|'+DOT+' x \d+)$')
DAY = 24 * 60 * 60
WEEK = 7 * DAY
WEEKLY_DOTS = 5 * DAY
DAILY_DOTS = DAY
MAX_DOTS = 5

class Board:
    ''' Asana implementation of Board abstract base class. '''
    def __init__(self, token, board_id, weekly_dots, columns, reqd_fields):
        self.token = token
        self.board_id = board_id
        self.weekly_dots = weekly_dots
        self.columns = columns
        self.reqd_fields = reqd_fields.items()

    def load(self):
        now = time.time()
        client = asana.Client.access_token(self.token)
        project = client.projects.find_by_id(self.board_id)
        project_name = project['name']
        params = { 'opt_expand': 'memberships,custom_fields' }
        for task in client.tasks.find_by_project(self.board_id, params):
            task_name = task['name']
            task_id = task['id']
            custom_fields = [
                (custom_field['name'], custom_field['enum_value']['name'])
                for custom_field in task['custom_fields']
                if custom_field.get('enum_value')]
            section_name = None
            for membership in task['memberships']:
                if membership['project']['name'] == project_name\
                    and membership['section']:
                    section_name = membership['section']['name']
                    break

            # skip sections
            if task_name == section_name:
                continue

            # skip columns that weren't requested
            if section_name not in self.columns:
                continue

            # skip tasks that don't have the correct custom fields
            if not all(reqd in custom_fields for reqd in self.reqd_fields):
                continue

            stories = client.tasks.stories(task_id)
            history = helpers.task_history(project_name, stories)
            dot_factor = WEEKLY_DOTS if self.weekly_dots else DAILY_DOTS
            dot_count = helpers.task_dot_count(history, now, dot_factor)

            if DOTS_RE.search(task_name):
                new_task_name = task_name.rsplit(' | ', 1)[0]
            else:
                new_task_name = task_name

            if dot_count > MAX_DOTS:
                new_task_name += ' | {} x {}'.format(DOT, dot_count)
            elif dot_count > 0:
                new_task_name += ' | ' + DOT * dot_count

            if new_task_name != task_name:
                print('{} => {}'.format(task_name, new_task_name))
                client.tasks.update(task_id, {'name': new_task_name})
