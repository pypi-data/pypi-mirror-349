__all__ = [
    "count",
    "ConvertibleToCount",
    "definition",
    "ConvertibleToDefinition",
    "module",
    "ConvertibleToModule",
    "definition",
    "ConvertibleToDefinition",
    "module",
    "ConvertibleToModule",
    "ConvertibleToPath",
    "FilePath",
    "DirectoryPath",
    "Path",
    "Model",
    "Documented",
    "Blob",
    "TypedDict",
    "Any",
    "NoReturn",
    "Never",
    "Self",
    "LiteralString",
    "ClassVar",
    "Final",
    "TypeVar",
    "Union",
    "Optional",
    "Literal",
    "TypeAlias",
    "Concatenate",
    "TypeGuard",
    "ForwardRef",
    "overload",
    "Callable",
    "cast",
    "verify",
    "check",
    "require",
    "Serialized",
    "Serializable",
]

# * lib types
from ._alias import (
    Serialized,
    Serializable,
)
from ._count import (
    count,
    ConvertibleToCount,
    # BitCount,
    # ByteCount,
)
from ._source import (
    definition,
    ConvertibleToDefinition,
    module,
    ConvertibleToModule,
)

# from ._extended import estr
from ._path import (
    ConvertibleToPath,
    FilePath,
    DirectoryPath,
    Path,
)
from ._model import Model, Documented, Blob
from ._guard import verify, check, require
from ._typeshed import (
    ConvertibleToFloat,
    ConvertibleToInt,
)
from ._decimal import (
    decimal,
    ConvertibleToDecimal,
)

# literals

from .lt._character_encoding import CharacterEncoding
from .lt._uuid import UUIDVersion

# * other common types from various standard libs/dependencies

# NOTE: typing_extensions is used over the default `typing` module for
# more compatibility with pydantic for these types
from typing_extensions import (
    TypedDict,  # TODO: add others where pydantic requires typing_extensions type
)

from typing import (
    Any,
    Callable,
    NoReturn,
    Never,
    Protocol,
    Self,
    LiteralString,
    ClassVar,
    Final,
    TypeVar,
    Union,
    Optional,
    Literal,
    TypeAlias,
    Concatenate,
    TypeGuard,
    ForwardRef,
    overload,
    cast,
    # TODO: add others as needed
)
from re import (
    Match,
    Pattern,
)


# ~typevars glitch if not defined in local scope of module seemingly
# class of:
#     """
#     Various type variables. Called `of` so can be used like:

#     ```python
#     import typically as t

#     # t.of.M - as in: "type of M"
#     def load(path: t.ConvertibleToPath, model: type[t.of.M]) -> t.of.M:
#         ...
#     ```
#     """

#     T = TypeVar("T")
#     M = TypeVar("M", bound=Model)
#     F = TypeVar("F", bound=Callable)


class to:
    """
    Type Operations
    """

    @staticmethod
    def serialize(): ...


class lens: ...
