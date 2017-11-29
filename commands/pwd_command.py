import argparse

from commands.base_command import BaseCommand


class PwdCommand(BaseCommand):
    NAME = 'pwd'
    DESCRIPTION = 'Prints working directory'

    def __init__(self, drive):
        super(PwdCommand, self).__init__(drive)

        self.parser.add_argument('useless_args', nargs='*',
                                 help=argparse.SUPPRESS)

    def execute(self, **useless_args):
        print(self.drive.pwd())
