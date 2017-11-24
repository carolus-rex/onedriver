import argparse

from commands.base_command import BaseCommand


class CdCommand(BaseCommand):
	NAME = 'cd'
	DESCRIPTION = 'Change directory'
	
	def __init__(self, drive):
		super(CdCommand, self).__init__(drive)										 								 

	def execute(self, path):
		self.drive.cd(path)
		
	def parse(self, args):
		data = self.parser.parse_known_args(args)
		
		path = " ".join(data[1])
				
		return {"path": path if path else "."}

