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

		self.parser.add_argument('/B', '/b',
								 help="Use simple format.",
								 action="store_true",
								 dest='use_simple_format')

		self.parser.add_argument('/C', '/c',
								 help="Shows the thousand separator in file size. This is the default option. Use /-C to disable.",
								 action="store_true",
								 dest='use_thousand_separator',
								 default=True)

		self.parser.add_argument('/-C', '/-c',
								 help=argparse.SUPPRESS,
								 action="store_false",
								 dest='use_thousand_separator')

		self.parser.add_argument('/L', '/l',
								 help="Use lowercase.",
								 action="store_true",
								 dest='use_lowercase')

	def execute(self, path, use_simple_format, use_thousand_separator,
				use_lowercase):
		output_lines = []

		if not use_simple_format:
			output_lines.extend(self.build_header(path))

		items = self.drive.dir(path)

		file_count = 0
		total_data_size = 0

		for item in items:
			if not use_simple_format:
				if item.file is not None:
					file_count += 1
					total_data_size += item.size

				output_lines.append(self.build_detailed_item(item,
															 use_thousand_separator,
															 use_lowercase))
				
			else:
				output_lines.append(item.name.lower() if use_lowercase else item.name)

		if not use_simple_format:
			output_lines.extend(self.build_summary(file_count,
												   len(items) - file_count,
												   total_data_size,
												   use_thousand_separator))

		print('\n'.join(output_lines))

	def build_header(self, path):
		header = []

		header.append(' Directory of %s' % self.drive.abspath(path))
		header.append('')

		item = self.drive.get_item(self.drive.find_item_id(path))

		base_dir_data = [item.last_modified_date_time.strftime('%d/%m/%Y  %I:%M %p'),
						 '<DIR>']

		for dir_name in ('.', '..'):
			dir_name_data = list(base_dir_data)
			dir_name_data.append(dir_name)

			header.append('{}    {:14} {}'.format(*dir_name_data))

		return header

	def build_detailed_item(self, item, use_thousand_separator, use_lowercase):
		display_item_data = [item.last_modified_date_time.strftime('%d/%m/%Y  %I:%M %p'),
							 '<DIR>' if item.file is None else item.size,
							 item.name.lower() if use_lowercase else item.name]
	
				
		return '{}    {:{dir_size_align}14{separator}} {}'.format(*display_item_data,
																  dir_size_align='>' if item.file is not None else '<',
																  separator=',' if item.file is not None and use_thousand_separator else '')

	def build_summary(self, file_count, folder_count, total_data_size, use_thousand_separator):
		return ['{:>16} {:8} {:>12{separator}} bytes'.format(file_count, 'files', total_data_size,
															 separator=',' if use_thousand_separator else ''),
				'{:>16} dirs'.format(folder_count - file_count)]
