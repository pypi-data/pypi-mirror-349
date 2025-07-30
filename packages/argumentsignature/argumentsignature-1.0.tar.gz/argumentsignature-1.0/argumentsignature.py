from typing import Type, Generic, TypeVar

__version__ = '1.0'

TCallable = TypeVar("TCallable")

class ArgumentType:
    def __init__(self, name:str):
        self.name = name
          
    def __str__(self):
        return self.name

ARG = ArgumentType(name='ARG')
ARGS = ArgumentType(name='ARGS')
KWARGS = ArgumentType(name='KWARGS')
RETURN = ArgumentType(name='RETURN')

class Argument(Generic[TCallable]):
    def __init__(self, name:str, type:Type[TCallable], default:TCallable=..., argtype:ArgumentType=ARG):
        self.name = name
        self.type = type
        self.default = default
        self.argtype = argtype
    
    def to_argument_value(self, value:TCallable) -> 'ArgumentValue[TCallable]':
        return ArgumentValue(
            name = self.name,
            type = self.type,
            value = value,
            default = self.default,
            argtype = self.argtype       
        )
    
    def __str__(self):
        items = list(map(lambda i: i[0]+': '+str(i[1]), self.__dict__.items()))
        return "{}({})".format(self.__class__.__name__, ', '.join(items))


class ArgumentValue(Argument, Generic[TCallable]):
    def __init__(self, name:str, type:Type[TCallable], value:TCallable, default:TCallable=..., argtype:ArgumentType=ARG):
        super().__init__(name=name, type=type, default=default, value=value, argtype=argtype)
        self.value = value

    def to_argument(self) -> Argument[TCallable]:
        return Argument(
            name = self.name,
            type = self.type,
            default = self.default,
            argtype = self.argtype       
        )

__all__ = [
    'ArgumentType',
    'Argument',
    'ArgumentValue',
    'ARG',
    'ARGS',
    'KWARGS',
    'RETURN'
]
