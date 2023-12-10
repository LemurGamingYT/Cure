from api import Args, OutputOp, Value, Arg, LiteralCode, GetAttr


def _print(compiler, args: Args) -> OutputOp:
    compiler.includes.add('iostream')
    return OutputOp(args=args)

def _println(compiler, args: Args) -> OutputOp:
    compiler.includes.add('iostream')
    
    args.args.append(Arg(Value(r"'\n'", 'string')))
    return OutputOp(args=args)

def _type(compiler, args: Args) -> LiteralCode:
    compiler.includes.add('iostream')
    compiler.includes.add('typeinfo')
    return LiteralCode(f'typeid({args.args[0].value.value}).name()')

def _len(compiler, args: Args) -> LiteralCode:
    if args.args[0].value.type == 'string':
        compiler.includes.add('iostream')
        return GetAttr(args.args[0].value, 'length', False, Args([]))


public_functions = {
    'print': _print,
    'println': _println,
    'type': _type,
    'len': _len,
}
