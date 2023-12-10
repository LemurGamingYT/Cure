from core.std.func_utils import check_args_length
from api import Args, Call, LiteralCode


class math:
    _INF = LiteralCode('std::INFINITY')
    
    @staticmethod
    def _min(compiler, args: Args) -> Call:
        check_args_length(args, 2)

        compiler.includes.add('iostream')
        return Call('std::min', args)
    
    @staticmethod
    def _max(compiler, args: Args) -> Call:
        check_args_length(args, 2)

        compiler.includes.add('iostream')
        return Call('std::max', args)
    
    @staticmethod
    def _abs(compiler, args: Args) -> Call:
        check_args_length(args, 1)

        compiler.includes.add('iostream')
        return Call('std::abs', args)
    
    @staticmethod
    def _pow(compiler, args: Args) -> Call:
        check_args_length(args, 2)

        compiler.includes.add('cmath')
        return Call('std::pow', args)
    
    @staticmethod
    def _sqrt(compiler, args: Args) -> Call:
        check_args_length(args, 1)

        compiler.includes.add('cmath')
        return Call('std::sqrt', args)
    
    @staticmethod
    def _log(compiler, args: Args) -> Call:
        check_args_length(args, 1)

        compiler.includes.add('cmath')
        return Call('std::log', args)
    
    @staticmethod
    def _acos(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::acos', args)
    
    @staticmethod
    def _asin(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::asin', args)
    
    @staticmethod
    def _atan(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::atan', args)
    
    @staticmethod
    def _atan2(compiler, args: Args) -> Call:
        check_args_length(args, 2)
        
        compiler.includes.add('cmath')
        return Call('std::atan2', args)
    
    @staticmethod
    def _cos(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::cos', args)
    
    @staticmethod
    def _sin(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::sin', args)
    
    @staticmethod
    def _tan(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::tan', args)
    
    @staticmethod
    def _ceil(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::ceil', args)
    
    @staticmethod
    def _floor(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::floor', args)
    
    @staticmethod
    def _round(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::round', args)
    
    @staticmethod
    def _trunc(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::trunc', args)
    
    @staticmethod
    def _fmod(compiler, args: Args) -> Call:
        check_args_length(args, 2)
        
        compiler.includes.add('cmath')
        return Call('std::fmod', args)
    
    @staticmethod
    def _cosh(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::cosh', args)
    
    @staticmethod
    def _sinh(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::sinh', args)
    
    @staticmethod
    def _tanh(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::tanh', args)
    
    @staticmethod
    def _exp(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::exp', args)
    
    @staticmethod
    def _log10(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::log10', args)
    
    @staticmethod
    def _log2(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::log2', args)
    
    @staticmethod
    def _hypot(compiler, args: Args) -> Call:
        check_args_length(args, 2)
        
        compiler.includes.add('cmath')
        return Call('std::hypot', args)
    
    @staticmethod
    def _erf(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::erf', args)
    
    @staticmethod
    def _erfc(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::erfc', args)
    
    @staticmethod
    def _tgamma(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::tgamma', args)
    
    @staticmethod
    def _lgamma(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::lgamma', args)
    
    @staticmethod
    def _isinf(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::isinf', args)
    
    @staticmethod
    def _isnan(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::isnan', args)
    
    @staticmethod
    def _isfinite(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::isfinite', args)
    
    @staticmethod
    def _isnormal(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::isnormal', args)
    
    @staticmethod
    def _signbit(compiler, args: Args) -> Call:
        check_args_length(args, 1)
        
        compiler.includes.add('cmath')
        return Call('std::signbit', args)
    
    @staticmethod
    def _copysign(compiler, args: Args) -> Call:
        check_args_length(args, 2)
        
        compiler.includes.add('cmath')
        return Call('std::copysign', args)
