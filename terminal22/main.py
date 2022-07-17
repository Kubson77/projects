import datetime
import logging

import os
import shutil
from pprint import pprint
from logging.handlers import RotatingFileHandler


def help():
    data_dict = {
        'command with args': [
            {
                'cd <path>': 'Change directory',
                'cr <file_name>': 'Create file',
                'mkdir <dir>': 'Create directory',
                'o <file_name>': 'Open file',
                'rm <name>': 'Remove file/direcotry',
                'stat <filename>': 'Show file info'
            }
        ],
        'command without args': [
            {
                'exit': 'Quit program',
                'help': 'Show help',
                'history': 'Show command history',
                'ls': 'Show files in current directory',
                'quit': 'Quit program',
                'tree': 'Show directory tree'
            }
        ]
    }

    return data_dict


def main():
    print('Terminal app')

    def __warning():
        print('You must pass at least one argument to invoke the command')

    while True:
        command = input(f'{os.getcwd()}$ ')
        logger_obj.info(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}, {command}')

        match command.split():
            case['quit' | 'exit']:
                print('Goodbye!')
                quit()
            case['help', *_]:
                pprint(help())
            case['ls', *_]:
                for item in os.listdir():
                    print(item)
            case['cr', *filenames]:
                if len(filenames) < 1:
                    __warning()
                    continue
                for file in filenames:
                    path_to_create = '/'.join(file.split('/')[:-1])
                    if not os.path.exists(file):
                        os.makedirs(path_to_create)
                    open(file, 'a').close()
            case['cd', *filenames]:
                if len(filenames) < 1:
                    __warning()
                    continue
                for file in filenames:
                    if not os.path.exists(file):
                        print('NOT a directory!')
                        continue
                    os.chdir(file)
            case ['mkdir', *paths]:
                if len(paths) < 1:
                    __warning()
                    continue
                for path in paths:
                    if not os.path.exists(path):
                        os.makedirs(path)
            case ['o', filename]:
                if not os.path.exists(filename):
                    print('File NOT found')
                    continue
                with open(filename, 'r') as file:
                    print(file.read())
            case ['rm', *filenames]:
                if len(filenames) < 1:
                    __warning()
                    continue
                for file in filenames:
                    if os.path.isfile(file):
                        os.remove(file)
                    elif os.path.isdir(file):
                        shutil.rmtree(file, ignore_errors=True)
                    else:
                        print(f'Not found: {file}')
            case ['stat', *filenames]:
                if len(filenames) < 1:
                    __warning()
                    continue
                for file in filenames:
                    if not os.path.exists(file):
                        print('NOT found!')
                        continue
                    stats = os.stat(file)
                    creation_date = datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%d-%m-%Y %H:%M:%S')
                    last_modification_date = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%d-%m-%Y %H:%M:%S')
                    print(f'\tFile name: {file}')
                    print(f'\tFile size: {stats.st_size} Bytes')
                    print(f'\tCreation date: {creation_date}')
                    print(f'\tLast modification date: {last_modification_date}')
                    print()
            case ['tree', *_]:
                for root, _, files in os.walk(os.getcwd()):
                    level = root.replace(os.getcwd(), '').count(os.sep)
                    indent = ' ' * 4 * level
                    print('{}{}/'.format(indent, os.path.basename(root)))
                    sub_indent = ' ' * 4 * (level + 1)
                    for f in files:
                        print('{}{}'.format(sub_indent, f))
            case ['history', *_]:
                try:
                    last_history_lines = int(input('How many lines do you want to see? '))
                except ValueError:
                    print('It is not a number!')
                    continue
                with open('log/app.log') as file:
                    lines = file.readlines()
                    for line in lines[-last_history_lines:]:
                        print(line, end='')
            case _:
                print(f'Command NOT found: {command}')
                print('Available commands:')
                pprint(help())


def configure_logger():
    logger_obj = logging.getLogger(__name__)
    logger_obj.setLevel(logging.INFO)

    if not os.path.exists('log'):
        os.makedirs('log')

    # roll over after 1000KB and keep backup logs app.log.1, app.log.2, etc.
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=5)
    logger_obj.addHandler(handler)

    return logger_obj


if __name__ == '__main__':
    logger_obj = configure_logger()
    main()
