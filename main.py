from platform import system, architecture, platform, processor, machine
from logging import info, DEBUG, basicConfig
from sys import argv

from colorama import init

from cure import ArgParser


def main():
    info(f"""Running Cure compiler
System = {system()}
Architecture = {architecture()[0]}
Platform = {platform()}
Processor = {processor()}
Machine = {machine()}
""")
    
    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()

    info('Successfully ran Cure compiler')


if __name__ == '__main__':
    init()
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(asctime)s [%(levelname)s] %(filename)s (line %(lineno)d) - %(message)s',
        datefmt='%H:%M:%S', encoding='utf-8', level=DEBUG
    )
    main()
