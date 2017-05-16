import configparser
import sys

from dotty import board

if len(sys.argv) != 2:
  print('usage: python -m dotty config_file')
  sys.exit(-1)

config_fn = sys.argv[1]
config = configparser.ConfigParser()
with open(config_fn) as config_file:
    config.read_file(config_file)

boards = []
for section_name in config.sections():
    section = config[section_name]
    weekly_dots = section['weekly_dots'].lower() == 'true'
    columns = [c.strip() for c in section['columns'].split(',')]
    b = board.Board(section['token'], section['id'], weekly_dots, columns)
    boards.append(b)

for board in boards:
    board.load()

