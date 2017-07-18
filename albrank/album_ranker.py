#!/usr/bin/env python
"""
Usage:
    album_ranker.py print (ranked | todo)
    album_ranker.py add (ranked | todo)
    album_ranker.py random (ranked | todo)

Options:
    -h --help     Show this screen.
    -v --version  Show version.

"""
import album
from docopt import docopt
arguments = docopt(__doc__, version='1.0')
#  print(arguments, end='\n\n')

if __name__ == '__main__':
    ranked = album.RankedList()
    todo = album.TodoList()
    ranked.read_file('ranked.txt')
    todo.read_file('todo.txt')
    if arguments['print']:
        if arguments['ranked']:
            print(ranked)
        elif arguments['todo']:
            print(todo)
    elif arguments['add']:
        if arguments['ranked']:
            album = album.Album()
            album.set()
            ranked.add(album)
            ranked.write_to_file()
            print('\n{}'.format(ranked))
        elif arguments['todo']:
            album = album.Album()
            album.set()
            todo.add(album)
            todo.write_to_file()
            print('\n{}'.format(todo))
    elif arguments['random']:
        if arguments['ranked']:
            print(ranked.choose_random())
        elif arguments['todo']:
            print(todo.choose_random())
