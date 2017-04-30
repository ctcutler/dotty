from dotty import asana
import sys

b = asana.AsanaBoard(sys.argv[1])
b.load()
