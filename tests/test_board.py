from context import dotty
from dotty import asana

class TestDotCount:
    def test_task_dot_count(self):
        asana.task_dot_count(None)

class TestHistory:
    def test_creation_only(self):
        board_name = "Kanban Example II"
        stories = [
            {
                "created_at": "2017-05-13T15:01:31.287Z",
                "text": "added to Kanban Example II",
                "type": "system",
            },
        ]
        expected_history = [
            { "ts": 1494687691.287, "column": None },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_creation_and_move(self):
        board_name = "Kanban Example II"
        stories = [
            {
                "created_at": "2017-05-13T15:01:31.287Z",
                "text": "added to Kanban Example II",
                "type": "system",
            },
            {
                "created_at": "2017-05-13T15:02:17.502Z",
                "text": "moved from Ready to Develop (Max WIP: 1) (Kanban Example II)",
                "type": "system",
            },
        ]
        expected_history = [
            { "ts": 1494687691.287, "column": "Ready" },
            { "ts": 1494687737.502, "column": "Develop (Max WIP: 1)" },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_creation_after_move(self):
        board_name = "Kanban Example II"
        stories = [
            {
                "created_at": "2017-05-13T15:02:17.502Z",
                "text": "moved from Ready to Develop (Max WIP: 1) (Kanban Example II)",
                "type": "system",
            },
            {
                "created_at": "2017-05-13T15:01:31.287Z",
                "text": "added to Kanban Example II",
                "type": "system",
            },
        ]
        expected_history = [
            { "ts": 1494687691.287, "column": "Ready" },
            { "ts": 1494687737.502, "column": "Develop (Max WIP: 1)" },
        ]
        assert asana.task_history(board_name, stories) == expected_history

    def test_ignore_unrelated_projects(self):
        board_name = "Kanban Example II"
        stories = [
            {
                "created_at": "2017-05-13T15:01:31.287Z",
                "text": "added to Kanban Example IV",
                "type": "system",
            },
            {
                "created_at": "2017-05-13T15:02:17.502Z",
                "text": "moved from Ready to Develop (Max WIP: 1) (Kanban Example IV)",
                "type": "system",
            },
        ]
        expected_history = []
        assert asana.task_history(board_name, stories) == expected_history

    def test_ignore_unrelated_stories(self):
        board_name = "Kanban Example II"
        stories = [
            {
                "created_at": "2017-05-13T15:01:31.287Z",
                "text": "added to Kanban Example II",
                "type": "system",
            },
            {
                "created_at": "2017-05-13T15:02:17.502Z",
                "text": "moved from Ready to Develop (Max WIP: 1) (Kanban Example II)",
                "type": "system",
            },
            {
                "created_at": "2017-05-13T15:02:17.502Z",
                "text": "This is a comment",
                "type": "comment",
            },
        ]
        expected_history = [
            { "ts": 1494687691.287, "column": "Ready" },
            { "ts": 1494687737.502, "column": "Develop (Max WIP: 1)" },
        ]
        assert asana.task_history(board_name, stories) == expected_history
