import configparser
import sys

from dotty import asana, github

if len(sys.argv) != 2:
  print("usage: python -m dotty config_file")
  sys.exit(-1)

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

boards = []
for section_name in config.sections():
    section = config[section_name]
    board_type = section['type']
    if board_type == 'asana':
        board = asana.AsanaBoard(section['token'])
        boards.append(board)
    else:
        print('Ignoring unknown board type: {}'.format(board_type))

for board in boards:
    board.load()

