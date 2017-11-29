import argparse

from commands.base_command import BaseCommand


class UploadCommand(BaseCommand):
    NAME = 'upload'
    DESCRIPTION = 'Uploads a file.'

    def __init__(self, drive):
        super(UploadCommand, self).__init__(drive)

        self.parser.add_argument('local_path',
                                 help='Specifies the file to upload')

        self.parser.add_argument('remote_path', nargs='?',
                                 help='Specifies where to put the uploaded file',
                                 default='.')

    def execute(self, local_path, remote_path):
        self.drive.upload(local_path, remote_path)
