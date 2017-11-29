import argparse

from commands.base_command import BaseCommand


class MkdirCommand(BaseCommand):
    NAME = 'mkdir'
    DESCRIPTION = 'Creates a directory.'

    def __init__(self, drive):
        super(MkdirCommand, self).__init__(drive)

        self.parser.add_argument('paths', nargs='+',
                                 help='The directory or directories to create')

    def execute(self, paths):
        self.drive.mkdir(*paths)
