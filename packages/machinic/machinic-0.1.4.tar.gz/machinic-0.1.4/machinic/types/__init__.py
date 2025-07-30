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
    "Serialized",
    "Serializable",
    "ConvertibleToFloat",
    "ConvertibleToInt",
    "decimal",
    "ConvertibleToDecimal",
    "Match",
    "Pattern",
    "Annotated",
    "Any",
    "Callable",
    "ClassVar",
    "Concatenate",
    "Final",
    "ForwardRef",
    "Generic",
    "Literal",
    "Optional",
    "ParamSpec",
    "Protocol",
    "TypeVar",
    "TypeVarTuple",
    "Union",
    "AbstractSet",
    "ByteString",
    "Container",
    "ContextManager",
    "Hashable",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "Sequence",
    "Sized",
    "ValuesView",
    "Awaitable",
    "AsyncIterator",
    "AsyncIterable",
    "Coroutine",
    "Collection",
    "AsyncGenerator",
    "AsyncContextManager",
    "Reversible",
    "SupportsAbs",
    "SupportsBytes",
    "SupportsComplex",
    "SupportsFloat",
    "SupportsIndex",
    "SupportsInt",
    "SupportsRound",
    "ChainMap",
    "Counter",
    "FrozenSet",
    "Generator",
    "BinaryIO",
    "IO",
    "TextIO",
    "AnyStr",
    "assert_type",
    "assert_never",
    "cast",
    "clear_overloads",
    "dataclass_transform",
    "final",
    "get_args",
    "get_origin",
    "get_overloads",
    "get_type_hints",
    "is_typeddict",
    "LiteralString",
    "Never",
    "NewType",
    "no_type_check",
    "no_type_check_decorator",
    "NoReturn",
    "NotRequired",
    "overload",
    "ParamSpecArgs",
    "ParamSpecKwargs",
    "Required",
    "reveal_type",
    "runtime_checkable",
    "Self",
    "Text",
    "TYPE_CHECKING",
    "TypeAlias",
    "TypeGuard",
    "Unpack",
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
from ._typeshed import (
    ConvertibleToFloat,
    ConvertibleToInt,
)
from ._decimal import (
    decimal,
    ConvertibleToDecimal,
)


# literals

# from .literal._character_encoding import CharacterEncoding
# from .literal._uuid import UUIDVersion

# * other common types from various standard libs/dependencies

# NOTE: typing_extensions is used over the default `typing` module for
# more compatibility with pydantic for these types
# TODO: add others where pydantic requires typing_extensions type
from typing_extensions import (
    TypedDict,
    NamedTuple,
)

# TODO.add collections
from collections import defaultdict, OrderedDict, deque
from queue import Queue, Empty, Full

from typing import (
    # --- omit
    # Tuple,
    # Type,
    # Deque,
    # Dict,
    # DefaultDict,
    # List,
    # OrderedDict,
    # Set,
    # Match,
    # Pattern,
    # --- omit
    Annotated,
    Any,
    Callable,
    ClassVar,
    Concatenate,
    Final,
    ForwardRef,
    Generic,
    Literal,
    Optional,
    ParamSpec,
    Protocol,
    TypeVar,
    TypeVarTuple,
    Union,
    AbstractSet,
    ByteString,
    Container,
    ContextManager,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Sized,
    ValuesView,
    Awaitable,
    AsyncIterator,
    AsyncIterable,
    Coroutine,
    Collection,
    AsyncGenerator,
    AsyncContextManager,
    Reversible,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsIndex,
    SupportsInt,
    SupportsRound,
    ChainMap,
    Counter,
    FrozenSet,
    Generator,
    BinaryIO,
    IO,
    TextIO,
    AnyStr,
    assert_type,
    assert_never,
    cast,
    clear_overloads,
    dataclass_transform,
    final,
    get_args,
    get_origin,
    get_overloads,
    get_type_hints,
    is_typeddict,
    LiteralString,
    Never,
    NewType,
    no_type_check,
    no_type_check_decorator,
    NoReturn,
    NotRequired,
    overload,
    ParamSpecArgs,
    ParamSpecKwargs,
    Required,
    reveal_type,
    runtime_checkable,
    Self,
    Text,
    TYPE_CHECKING,
    TypeAlias,
    TypeGuard,
    Unpack,
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


# class to:
#     """
#     Type Operations
#     """

#     @staticmethod
#     def serialize(): ...


# class lens: ...
