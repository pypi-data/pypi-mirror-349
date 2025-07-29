import dataclasses
import functools
from collections import namedtuple
from typing import *

from norming import _utils

__all__ = ["Norming"]

BaseNorming = namedtuple("BaseNorming", ["args", "kwargs"])


class Norming(BaseNorming):
    "This class helps to create normed classes."

    def __new__(cls: type, /, *args: Any, **kwargs: Any) -> None:
        "This magic method returns a new instance."
        return BaseNorming.__new__(cls, args=args, kwargs=kwargs)

    def __call__(self: Self, norm: Callable) -> type:
        "This magic method implements calling the current instance."
        Ans: type = _utils.getclass(norm, *self.args, **self.kwargs)
        Ans.__doc__ = _utils.getdoc(norm)
        Ans.__module__ = str(norm.__module__)
        Ans.__name__ = str(norm.__name__)
        Ans.__qualname__ = str(norm.__qualname__)
        Ans.__new__.__annotations__ = _utils.getannotations(norm)
        Ans.__new__.__signature__ = _utils.getsignature(norm)
        Ans.__new__.__type_params__ = _utils.getparams(norm)
        return Ans
