import time

from context import dotty
from dotty import asana

HOUR = 3600
DAY = 24 * HOUR
WEEK = 7 * DAY

MID_SATURDAY = 1494691200 # in EST

class TestDotCount:
    def test_week_granularity(self):
        history = [
            {'ts': MID_SATURDAY - 8*DAY, 'column': 'In Progress'},
        ]
        assert 1 == asana.task_dot_count(
            history, MID_SATURDAY - DAY, asana.WEEKLY_DOTS
        )
        history = [
            {'ts': MID_SATURDAY - ((8*DAY)-HOUR), 'column': 'In Progress'},
        ]
        assert 0 == asana.task_dot_count(
            history, MID_SATURDAY - DAY, asana.WEEKLY_DOTS
        )

    def test_day_granularity(self):
        history = [
            {'ts': MID_SATURDAY - 2*DAY, 'column': 'In Progress'},
        ]
        assert 1 == asana.task_dot_count(history, MID_SATURDAY - DAY)
        history = [
            {'ts': MID_SATURDAY - (2*DAY - HOUR), 'column': 'In Progress'},
        ]
        assert 0 == asana.task_dot_count(history, MID_SATURDAY - DAY)

    def test_within_single_weekend(self):
        history = [ {'ts': MID_SATURDAY, 'column': 'Foo'} ]
        assert 0 == asana.task_dot_count(history, MID_SATURDAY+DAY)

    def test_start_on_weekend(self):
        history = [ {'ts': MID_SATURDAY, 'column': 'Foo'} ]
        assert 1 == asana.task_dot_count(history, MID_SATURDAY + 3*DAY)

    def test_end_on_weekend(self):
        history = [ {'ts': MID_SATURDAY - 2*DAY, 'column': 'Foo'} ]
        assert 1 == asana.task_dot_count(history, MID_SATURDAY)

    def test_spanning_weekend(self):
        history = [ {'ts': MID_SATURDAY - 2*DAY, 'column': 'Foo'} ]
        assert 3 == asana.task_dot_count(history, MID_SATURDAY + 3*DAY)

    def test_spanning_two_weekend(self):
        history = [ {'ts': MID_SATURDAY - 9*DAY, 'column': 'Foo'} ]
        assert 8 == asana.task_dot_count(history, MID_SATURDAY + 3*DAY)

    def test_start_on_weekend_span_weekend(self):
        history = [ {'ts': MID_SATURDAY, 'column': 'Foo'} ]
        assert 6 == asana.task_dot_count(history, MID_SATURDAY + 10*DAY)

    def test_span_weekend_end_on_weekend(self):
        history = [ {'ts': MID_SATURDAY - 8*DAY, 'column': 'Foo'} ]
        assert 5 == asana.task_dot_count(history, MID_SATURDAY)

    def test_start_on_weekend_span_weekend_end_on_weekend(self):
        history = [ {'ts': MID_SATURDAY - 14*DAY, 'column': 'Foo'} ]
        assert 10 == asana.task_dot_count(history, MID_SATURDAY)

    def test_multiple_column_stints(self):
        history = [
            {'ts': MID_SATURDAY - 4*DAY, 'column': 'In Progress'},
            {'ts': MID_SATURDAY - 3*DAY, 'column': 'Code Review'},
            {'ts': MID_SATURDAY - 2*DAY, 'column': 'In Progress'},
        ]
        assert 2 == asana.task_dot_count(history, MID_SATURDAY-DAY)

    def test_single_history_item(self):
        history = [
            {'ts': MID_SATURDAY - 3*DAY, 'column': None},
        ]
        assert 2 == asana.task_dot_count(history, MID_SATURDAY-DAY)

class TestHistory:
    def test_creation_only(self):
        board_name = 'Kanban Example II'
        stories = [
            {
                'created_at': '2017-05-13T15:01:31.287Z',
                'text': 'added to Kanban Example II',
                'type': 'system',
            },
        ]
        expected_history = [
            { 'ts': 1494702091.287, 'column': None },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_creation_and_move(self):
        board_name = 'Kanban Example II'
        stories = [
            {
                'created_at': '2017-05-13T15:01:31.287Z',
                'text': 'added to Kanban Example II',
                'type': 'system',
            },
            {
                'created_at': '2017-05-13T15:02:17.502Z',
                'text': 'moved from Ready to Develop (Max WIP: 1) (Kanban Example II)',
                'type': 'system',
            },
        ]
        expected_history = [
            { 'ts': 1494702091.287, 'column': 'Ready' },
            { 'ts': 1494702137.502, 'column': 'Develop (Max WIP: 1)' },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_creation_after_move(self):
        board_name = 'Kanban Example II'
        stories = [
            {
                'created_at': '2017-05-13T15:02:17.502Z',
                'text': 'moved from Ready to Develop (Max WIP: 1) (Kanban Example II)',
                'type': 'system',
            },
            {
                'created_at': '2017-05-13T15:01:31.287Z',
                'text': 'added to Kanban Example II',
                'type': 'system',
            },
        ]
        expected_history = [
            { 'ts': 1494702091.287, 'column': 'Ready' },
            { 'ts': 1494702137.502, 'column': 'Develop (Max WIP: 1)' },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_ignore_unrelated_projects(self):
        board_name = 'Kanban Example II'
        stories = [
            {
                'created_at': '2017-05-13T15:01:31.287Z',
                'text': 'added to Kanban Example IV',
                'type': 'system',
            },
            {
                'created_at': '2017-05-13T15:02:17.502Z',
                'text': 'moved from Ready to Develop (Max WIP: 1) (Kanban Example IV)',
                'type': 'system',
            },
        ]
        expected_history = []
        assert asana.task_history(board_name, stories) == expected_history

    def test_ignore_unrelated_stories(self):
        board_name = 'Kanban Example II'
        stories = [
            {
                'created_at': '2017-05-13T15:01:31.287Z',
                'text': 'added to Kanban Example II',
                'type': 'system',
            },
            {
                'created_at': '2017-05-13T15:02:17.502Z',
                'text': 'moved from Ready to Develop (Max WIP: 1) (Kanban Example II)',
                'type': 'system',
            },
            {
                'created_at': '2017-05-13T15:02:17.502Z',
                'text': 'This is a comment',
                'type': 'comment',
            },
        ]
        expected_history = [
            { 'ts': 1494702091.287, 'column': 'Ready' },
            { 'ts': 1494702137.502, 'column': 'Develop (Max WIP: 1)' },
        ]
        assert asana.task_history(board_name, stories) == expected_history
