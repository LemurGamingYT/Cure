from logging import basicConfig, DEBUG
from pathlib import Path

from click import command, argument
from colorama import init

from cure import compile_to_exe, ir


@command()
@argument('file', type=Path)
def main(file: Path):
    scope = ir.Scope(file)
    compile_to_exe(scope)


def setup_logger():
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(asctime)s [%(levelname)s] %(funcName)s (line %(lineno)d) - %(message)s',
        datefmt='%H:%M:%S', encoding='utf-8', level=DEBUG
    )



if __name__ == '__main__':
    init()
    setup_logger()
    main()
