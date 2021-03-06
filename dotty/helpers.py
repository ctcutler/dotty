from datetime import datetime, timedelta
import json
import re

DAY = 24 * 60 * 60
WEEK = 7 * DAY
ADD_RE = re.compile(r'^added to (?P<board>.+)$')
MOVE_RE = re.compile(
    r'^moved from (?P<from_column>.+) to (?P<column>.+) \((?P<board>.+)\)$')
MOVE_RE2 = re.compile(r'^moved this Task from (?P<from_column>.+) to (?P<column>.+)$')
MOVE_RE3 = re.compile(r'^moved this Task from (?P<from_column>.+) to (?P<column>.+) in (?P<board>.+)$')

def iso8601_to_epoch(iso_string):
    dt = datetime.strptime(iso_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt.timestamp()

def is_relevant(board_name, story):
    if story['type'] != 'system':
        return False

    match = ADD_RE.search(story['text'])\
        or MOVE_RE.search(story['text'])\
        or MOVE_RE2.search(story['text'])\
        or MOVE_RE3.search(story['text'])

    if not match:
        return False

    board = match.groupdict().get('board')

    if board and board != board_name:
        return False

    return True

def history_item(story):
    match = ADD_RE.search(story['text'])\
        or MOVE_RE.search(story['text'])\
        or MOVE_RE2.search(story['text'])\
        or MOVE_RE3.search(story['text'])
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

def stint(history, now, idx):
    return {
        'start': history[idx]['ts'],
        'end': now if idx == len(history)-1 else history[idx+1]['ts'],
        'column': history[idx]['column'],
    }

def weektime(epoch):
    'Seconds since the beginning of the week'
    dt = datetime.fromtimestamp(epoch)
    return (dt.weekday() * 24 * 60 * 60) +\
        (dt.hour * 60 * 60) +\
        (dt.minute * 60) +\
        dt.second +\
        (dt.microsecond/1000000)

def on_weekend(epoch):
    'Is this timestamp on the weekend in the current time zone?'
    return datetime.fromtimestamp(epoch).weekday() > 4

def weekend_end(epoch):
    'Return the weekend end after this timestamp'
    dt = datetime.fromtimestamp(epoch)
    dt += timedelta(days=7-dt.weekday())
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt.timestamp()

def weekend_start(epoch):
    'Return the weekend start before this timestamp'
    dt = datetime.fromtimestamp(epoch)
    days = (dt.weekday() + 2) % 7
    dt -= timedelta(days=days)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt.timestamp()

def elapsed(stint):
    start = stint['start']
    end = stint['end']
    total = end - start

    # if start is on a weekend adjust it forward to the end of the weekend
    # and remove that time from the total
    if on_weekend(start):
        delta = min(end, weekend_end(start)) - start
        total -= delta
        start += delta

    # if end is on a weekend adjust it back to the start of the weekend
    # and remove that time from the total
    if on_weekend(end):
        delta = end - max(start, weekend_start(end))
        total -= delta
        end -= delta

    # now that start and end have been adjusted, account for any weekends
    # in the middle of the range
    adjusted_total = end - start
    spanned_weekends = int(adjusted_total/WEEK)
    if weektime(start) > weektime(end):
        spanned_weekends += 1
    total -= 2 * DAY * spanned_weekends

    return total

def task_dot_count(history, now, dot_factor):
    """
       Figure out how long (how many dots) the task has been in its
       current column.
       - calculate column stints with start and end for each stint
       - filter out stints in everything but the current column
       - calculate elapsed time (omitting weekends) for each stint
       - sum stints' elapsed time
    """
    stints = map(lambda idx: stint(history, now, idx), range(len(history)))
    filtered_stints = filter(
        lambda s: s['column'] == history[-1]['column'],
        stints
    )
    total_secs = sum(elapsed(stint) for stint in filtered_stints)
    return int(total_secs/dot_factor)
