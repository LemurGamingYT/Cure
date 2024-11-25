from argparse import ArgumentParser
from pathlib import Path
from io import StringIO


arg_parser = ArgumentParser(description='Get all c files')
arg_parser.add_argument('path', type=Path, help='Path to the directory')
args = arg_parser.parse_args()

paths = StringIO()
for file in args.path.rglob('*.c'):
    paths.write(f'{file} ')

print(paths.getvalue())
