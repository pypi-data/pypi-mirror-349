import functools
import inspect
from typing import *

__all__ = ["getclass", "getdecorator"]


def _getclass(_cls: type, /, norm: Callable) -> type:
    "This decorator turns a norm function into a normed class."

    class Ans(_cls):
        "This class will be returned after overwriting this current doc string."

        def __new__(cls: type, /, *args: Any, **kwargs: Any) -> Self:
            "This magic method returns a new instance of the class."
            data: Any = norm(cls, *args, **kwargs)
            obj: Self = cls.__new__(cls, data)
            return obj

    return Ans


def getclass(cls: type, /, norm: Callable) -> type:
    "This decorator turns a norm function into a normed class."
    Ans: type = _getclass(cls, norm)
    Ans.__doc__ = norm.__doc__
    Ans.__module__ = norm.__module__
    Ans.__name__ = norm.__name__
    oldsig: inspect.Signature = inspect.signature(norm)
    params: Iterable = oldsig.parameters.values()
    newsig: inspect.Signature = inspect.Signature(
        parameters=params,
        return_annotation=Self,
    )
    Ans.__new__.__signature__ = newsig
    Ans.__qualname__ = norm.__qualname__
    return Ans


def getdecorator(cls: type) -> type:
    "This decorator turns a norm function into a normed class."
    return functools.partial(getclass, cls)
