import argparse

from commands.base_command import BaseCommand


class DownloadCommand(BaseCommand):
	NAME = 'download'
	DESCRIPTION = 'Downloads a file.'
	
	def __init__(self, drive):
		super(DirCommand, self).__init__(drive)

		self.parser.add_argument('remote_path',
		 						 help='Specifies the file to download')
		
		self.parser.add_argument('local_path', nargs='?',
		 						 help='Specifies where to put the downloaded file',
		 						 default='.')
								 
	def execute(self, remote_path, local_path):
		self.drive.download(remote_path, local_path)

