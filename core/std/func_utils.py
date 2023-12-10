from api import Args

from core.error import report_error


def check_args_length(args: Args, required_length: int):
    if len(args.args) > required_length:
        report_error('Type', 'Too many arguments given')
    elif len(args.args) < required_length:
        report_error('Type', 'Not enough arguments')
