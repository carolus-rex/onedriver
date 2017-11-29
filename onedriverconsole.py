import shlex
import argparse

import readline

from onedriver import *

from commands.cd_command import CdCommand
from commands.cls_command import ClsCommand
from commands.pwd_command import PwdCommand
from commands.dir_command import DirCommand
from commands.mkdir_command import MkdirCommand
from commands.del_command import DelCommand
from commands.upload_command import UploadCommand
from commands.download_command import DownloadCommand

drive = OneDrive()

main_parser = argparse.ArgumentParser(add_help=False)
main_parser.add_argument('command')

COMMANDS = {'cd': CdCommand(drive),
            'cls': ClsCommand(drive),
            'pwd': PwdCommand(drive),
            'dir': DirCommand(drive),
            'mkdir': MkdirCommand(drive),
            'del': DelCommand(drive),
            'upload': UploadCommand(drive),
            'download': DownloadCommand(drive)}


def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

while True:
    data = input("%s>" % drive.pwd())

    user_args = shlex.split(data)

    if len(user_args) > 0:

        try:
            namespace, args_to_parse = main_parser.parse_known_args(user_args)

            command = namespace.command  # Esto es normal y correcto

            try:
                command_func = COMMANDS[command]
            except KeyError:
                print('"%s" command not found' % command)
                continue

            command_func(args_to_parse)

        except RemoteFileNotFoundError:
            print("System can't find the specified REMOTE route")

        except InvalidRemoteDirectoryError:
            print("Directory name is invalid")

        except SystemExit:
            # I think this is enough to
            # After all, i only care about avoid exit the console
            pass

        print("")
