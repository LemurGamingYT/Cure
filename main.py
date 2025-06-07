from pathlib import Path

from click import command, argument

from cure import compile_to_exe, ir


@command()
@argument('file', type=Path)
def main(file: Path):
    scope = ir.Scope(file)
    compile_to_exe(scope)


if __name__ == '__main__':
    main()
