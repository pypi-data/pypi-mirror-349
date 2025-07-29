from typing import *

__all__ = ["staticmeta", "staticclass"]


class StaticClassError(TypeError):
    def __init__(self: Self, /, msg: Any) -> None:
        "This magic method initializes a new instance."
        return super().__init__(str(msg))


class staticmeta(type):
    def __call__(cls: type, /, *args: Any, **kwargs: Any) -> None:
        "This magic method implements calling the class."
        e = "Not allowed to instantiate static class %r!"
        e %= cls.__name__
        raise StaticClassError(e)


class staticclass(metaclass=staticmeta): ...
