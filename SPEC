Goal
----
Runs periodically, tracking how long every item on a board has been in a
particular column and updating a label on every item with the appropriate
number of dots to indicate how long it has been in that column.

Useful Side Effect
------------------
Maintains a comprehensive history of items' progress across the board.
This data can be used to track team metrics like lead/cycle time,
throughput, etc. As this code matures, this will become less of a side
effect and more of the main point of the project.

Compatibility
-------------
Initially should work with GitHub Projects and Asana.

Requirements
------------
- Easy to run as a cron job
- Support multiple boards through separate config files
- Support multiple "resolutions" for a dot (i.e. one dot might equal a day,
  a week, or some other configurable length of time)
- "dot" character is actually configurable, doesn't have to be a bullet
- Remembers how long an item has been in a particular column, even if it
  leaves that column and then returns.

Data Format
-----------
- Requirements:
  - Per board lists of items where every item has:
    - id
    - URL
    - subject/summary
    - owners
    - history (list of column entry/exit events)
- Example:
```
[
  {
    "boardURL": "http://foobar.com/board/123",
    "items": [
      {
        "id": "proj#123",
        "url": "http://foobar.com/board/123/proj/123",
        "summary": "fix the plange",
        "owners": ["mork", "mindy"],
        "history": [
          {
            "ts": 1234567890,
            "type": "ENTER", // or "EXIT"
            "column": "backlog",
          },
          ...
        ]
    ]
  }
  ...
]
```

Implementation Thoughts
-----------------------
- Do this completely TDD.  Always write the tests first.
