import argparse

from commands.base_command import BaseCommand


class DirCommand(BaseCommand):
	NAME = 'dir'
	DESCRIPTION = 'Show the list of subdirectories and files from a directory'
	
	def __init__(self, drive):
		super(DirCommand, self).__init__(drive)

		self.parser.add_argument('path', nargs='?',
		 						 help='Specifies the directory to show',
		 						 default='.')

	def execute(self, path):
		drive = self.drive
	
		print(' Directory of %s' % drive.abspath(path))
		print()

		item = drive.get_item(drive.find_item_id(path))

		base_dir_data = [item.last_modified_date_time.strftime('%d/%m/%Y  %I:%M %p'),
						 '<DIR>']

		for dir_name in ('.', '..'):
			dir_name_data = list(base_dir_data)
			dir_name_data.append(dir_name)

			print('{}    {:14} {}'.format(*dir_name_data))
		
		items = drive.dir(path)

		file_count = 0
		total_data_size = 0

		for item in items:
			display_item_data = [item.last_modified_date_time.strftime('%d/%m/%Y  %I:%M %p'),
								 '<DIR>' if item.file is None else item.size,
								 item.name]

			if item.file is not None:
				file_count += 1
				total_data_size += item.size
			
			print('{}    {:{dir_size_align}14{separator}} {}'.format(*display_item_data,
																	 dir_size_align='>' if item.file is not None else '<',
																	 separator=',' if item.file is not None else ''))

		print('{:>16} {:8} {:>12,} bytes'.format(file_count, 'files', total_data_size))
		print('{:>16} dirs'.format(len(items) - file_count))

