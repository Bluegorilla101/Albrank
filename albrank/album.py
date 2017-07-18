"""Contains classes of album lists and an album class with the
purpose of ranking albums based on the user's input and maintaing
a 'todo' list of albums which the user intends to listen to.
All results are saved to files.
"""
import bisect
import random
import re


class AlbumList:
    """Contains a generic, unique list of albums"""

    def __init__(self):
        self.list = []

    def __str__(self):
        string = ''
        for song in self.list:
            string += '{}\n'.format(str(song))
        return string

    def add(self, album):
        if album not in self.list:
            self.list.append(album)

    def write_to_file(self, file_name='album.txt'):
        f = open(file_name, 'w+')
        f.write(str(self))
        f.close()

    def choose_random(self):
        """Return a random album from the list."""
        return random.choice(self.list)

    def read_file(self, file_name='album.txt'):
        """Read the contents of file_name into self.list.
        Will skip any lines which do not fit into the format of
        '*name* - *artist*'
        """
        f = open(file_name, 'r')
        text = f.readlines()

        for line in text:
            # If the line matches the format for an album.
            if re.match(r'(.+\s)+-(\s.+)+\n', line) is not None:
                album = Album()
                # Don't include the newline character as part of the album.
                album.set(line[:-1])
                self.list.append(album)


class RankedList(AlbumList):
    """Contains a unique list of ordered albums
    where the albums with the lower index are considered to
    be be better than the albums with a greater index by the user.
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Ranked List:\n{}'.format(super().__str__())

    def add(self, album):
        bisect.insort(self.list, album)

    def write_to_file(self, file_name='ranked.txt'):
        super().write_to_file(file_name)


class TodoList(AlbumList):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'To-do List:\n{}'.format(super().__str__())

    def write_to_file(self, file_name='todo.txt'):
        super().write_to_file(file_name)


class Album:
    def __init__(self, name=None, artist=None):
        self.name = name
        self.artist = artist

    def __str__(self):
        return '{} - {}'.format(self.name, self.artist)

    def __eq__(self, other):
        return self.name == other.name and self.artist == other.artist

    def set(self, line=None):
        """Sets the name and artist for the album.
        :line: String: If provided, the album will be set from the
        provided string in the format '*name* - *artist*'.
        Otherwise the album will be set from user input.
        """
        if line is not None:
            details = line.split(' - ')
            self.name = details[0]
            self.artist = details[1]
        else:
            self.name = input('Name of album: ')
            self.artist = input('Name of artist: ')

    def __lt__(self, other):
        """Required for bisect to work."""
        choice = ''
        while choice not in ('1', '2'):
            choice = input(
                'Which is better?\n1) {}\n2) {}\nEnter \'1\' or \'2\': '
                .format(other, self))
        return choice == '2'

    def __is_valid_line(self, line):
        """Returns True if the provided line is in the appropriate format
        for getting infomration for an album.
        """
