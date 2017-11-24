import argparse


class BaseCommand(object):
	self.NAME = ''
	self.DESCRIPTION = ''

	def __init__(self, drive):
		self.drive = drive

		self.parser = argparse.ArgumentParser(prog=self.NAME,
											  description=self.DESCRIPTION,
											  prefix_chars='/',
											  add_help=False)
											  
		self.parser.add_argument("/?", action="help",
								 help="show this help message and exit")

	def execute(**args):
		pass

	def parse(self, args):
		return vars(self.parser.parse_args(args))

	def __call__(self, args):
		parsed_args = self.parse(args)

		return self.execute(**parsed_args)

