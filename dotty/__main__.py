import json
import sys

from dotty import board

if len(sys.argv) != 2:
  print('usage: python -m dotty config_file')
  sys.exit(-1)

config_fn = sys.argv[1]
with open(config_fn) as config_file:
    config = json.load(config_file)

boards = []
for board_config in config['boards']:
    weekly_dots = board_config['weekly_dots']
    columns = board_config['columns']
    token = board_config['token']
    board_id = board_config['id']
    custom_fields = board_config['custom_fields']
    b = board.Board(token, board_id, weekly_dots, columns, custom_fields)
    boards.append(b)

for board in boards:
    board.load()

