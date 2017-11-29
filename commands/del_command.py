from commands.base_command import BaseCommand


class DelCommand(BaseCommand):
    NAME = 'del'
    DESCRIPTION = 'Deletes one or more files'

    def __init__(self, drive):
        super(DelCommand, self).__init__(drive)

        self.parser.add_argument('path',
                                 help='Specifies the file to delete')

    def execute(self, path):
        self.drive.delete(path)
