import configparser
import sys

from dotty import asana, github

if len(sys.argv) != 2:
  print("usage: python -m dotty config_file")
  sys.exit(-1)

config_fn = sys.argv[1]
config = configparser.ConfigParser()
with open(config_fn) as config_file:
    config.read_file(config_file)

boards = []
for section_name in config.sections():
    section = config[section_name]
    board_type = section['type']

    if board_type == 'asana':
        board_class = asana.AsanaBoard
    else:
        print('Ignoring unknown board type: {}'.format(board_type))

    board = board_class(section['token'], section['id'])
    boards.append(board)

for board in boards:
    board.load()

