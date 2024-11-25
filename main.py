from logging import basicConfig, DEBUG

from colorama import init

from args_parser import CureArgumentParser
# from repl import repl

init()
basicConfig(
    level=DEBUG, filename='compiler.log', filemode='w',
    format='%(asctime)s %(levelname)s %(message)s'
)


def main() -> None:
    arg_parser = CureArgumentParser()
    result = arg_parser.parse_args()
    if not result.success:
        print(result)


if __name__ == '__main__':
    main()
