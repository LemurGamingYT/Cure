from logging import basicConfig, DEBUG
from sys import argv

from colorama import init

from cure import ArgParser


def main():
    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(asctime)s [%(levelname)s] %(filename)s (line %(lineno)d) - %(message)s',
        datefmt='%H:%M:%S', encoding='utf-8', level=DEBUG
    )
    main()
