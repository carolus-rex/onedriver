import argparse

from shutil import get_terminal_size

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

		self.parser.add_argument('/W', '/w',
								 help="Use wide list format.",
								 action="store_true",
								 dest='use_wide_format')

	def execute(self, path, use_simple_format, use_thousand_separator,
				use_lowercase, use_wide_format):
		output_lines = []

		items = list(self.drive.dir(path))

		if not use_simple_format:
			item = self.drive.get_item(self.drive.find_item_id(path))

			output_lines.extend(self.build_header(path))
			
			for dir in ('..', '.'):
				items.insert(0, argparse.Namespace(name=dir,
												   folder='holder',
												   file=None,
												   last_modified_date_time=item.last_modified_date_time))

		file_count = 0
		total_data_size = 0

		if use_wide_format:
			item_max_length = self.get_max_item_name_length(items)
			column_count = get_terminal_size().columns // item_max_length
			#column_width = column_count * item_max_length
			column_width = item_max_length

			current_line = []

		for item in items:
			if not use_simple_format:
				if item.file is not None:
					file_count += 1
					total_data_size += item.size

				if not use_wide_format:
					output_lines.append(self.build_detailed_item(item,
															 	 use_thousand_separator,
															 	 use_lowercase))
				else:
					if len(current_line) == column_count:
						output_lines.append(' '.join(current_line))
						current_line = []

					current_line.append(self.build_wide_item(item, 
															 column_width))
				
			else:
				output_lines.append(item.name.lower() if use_lowercase else item.name)

		if use_wide_format and not use_simple_format:
			output_lines.append(' '.join(current_line))

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

		return header

	def build_detailed_item(self, item, use_thousand_separator, use_lowercase):
		display_item_data = [item.last_modified_date_time.strftime('%d/%m/%Y  %I:%M %p'),
							 '<DIR>' if item.file is None else item.size,
							 item.name.lower() if use_lowercase else item.name]
	
				
		return '{}    {:{dir_size_align}14{separator}} {}'.format(*display_item_data,
																  dir_size_align='>' if item.file is not None else '<',
																  separator=',' if item.file is not None and use_thousand_separator else '')

	def build_wide_item(self, item, column_width):
		return '{:{column_width}}'.format(item.name if item.folder is None else '[%s]' % item.name,
									   	  column_width=column_width)

	def build_summary(self, file_count, folder_count, total_data_size, use_thousand_separator):
		return ['{:>16} {:8} {:>12{separator}} bytes'.format(file_count, 'files', total_data_size,
															 separator=',' if use_thousand_separator else ''),
				'{:>16} dirs'.format(folder_count)]

	def get_max_item_name_length(self, items):
		sortKey = lambda item : len(item.name) if item.folder is None else len(item.name) + 2
		item_list = list(items)
		item_list.sort(key=sortKey)

		return len(item_list.pop(-1).name) + 1
