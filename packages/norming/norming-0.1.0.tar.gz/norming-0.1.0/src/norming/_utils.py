import inspect
from typing import *

__all__ = [
    "getannotations",
    "getclass",
    "getdoc",
    "getparams",
    "getsignature",
]


def getannotations(norm: Callable, /) -> dict:
    "This function returns an annotations dict for the __new__ magic method."
    ans: dict = dict(norm.__annotations__)
    ans["return"] = Self
    return ans


def getclass(norm: Callable, /, *_args: Any, **_kwargs: Any) -> type:
    "This function creates a class using a given base and a given norm."

    class Ans(*_args, **_kwargs):
        "This class will be returned after overwriting this current doc string."

        def __new__(cls: type, /, *args: Any, **kwargs: Any) -> Self:
            "This magic method returns a new instance of the class."
            data: Any = norm(cls, *args, **kwargs)
            obj: Self = super().__new__(cls, data)
            return obj

    return Ans


def getdoc(norm: Callable) -> Optional[str]:
    "This function returns a doc string."
    doc: Any = norm.__doc__
    ans: Optional[str] = None if doc is None else str(doc)
    return ans


def getparams(norm: Callable) -> tuple:
    "This function returns the parameter typing."
    return tuple(norm.__type_params__)


def getsignature(norm: Callable) -> inspect.Signature:
    "This function returns a signature for the __new__ magic method."
    oldsig: inspect.Signature = inspect.signature(norm)
    params: Iterable = oldsig.parameters.values()
    newsig: inspect.Signature = inspect.Signature(
        parameters=params,
        return_annotation=Self,
    )
    return newsig
