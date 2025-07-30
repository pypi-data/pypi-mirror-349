import typing
from io import StringIO
from typically.literal import CharacterEncoding


@typing.runtime_checkable
class StrMethodDefined(typing.Protocol):
    def __str__(self) -> str: ...


# ? only `str` actually generates `str` when value passed as constructor?

StrDecodable = typing.Union[
    bytes,
    bytearray,
]

SoftConvertibleToStr = typing.Union[
    str,
    StrMethodDefined,
    StringIO,
    StrDecodable,
    # typing.AnyStr, # NOTE: messes with `builtins.isinstance`
]


def normalize(
    s: SoftConvertibleToStr,
    encoding: CharacterEncoding = "utf-8",
) -> str:
    if isinstance(s, str):
        return s
    elif isinstance(s, StrDecodable):
        return s.decode(encoding)
    elif isinstance(s, StringIO):
        return s.read()
    else:
        raise TypeError(s)
