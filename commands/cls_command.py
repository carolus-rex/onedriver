import argparse

from commands.base_command import BaseCommand


class ClsCommand(BaseCommand):
    NAME = 'cls'
    DESCRIPTION = 'Clears the screen'

    def __init__(self, drive):
        super(ClsCommand, self).__init__(drive)

        self.parser.add_argument('useless_args', nargs='*',
                                 help=argparse.SUPPRESS)

    def execute(self, **useless_args):
        for a in range(200):
            print()
