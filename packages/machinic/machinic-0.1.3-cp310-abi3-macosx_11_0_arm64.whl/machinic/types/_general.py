from __future__ import annotations
import re
import inspect
import importlib
from decimal import Decimal, DecimalTuple, Context
from types import ModuleType as module
from typing import (
    Any,
    Generic,
    TypeVar,
    overload,
    get_args,
    TypeVar,
    Self,
    ClassVar,
    cast,
    Callable,
)
from typing_extensions import LiteralString
from pydantic import ValidatorFunctionWrapHandler
from pydantic_core import core_schema, PydanticSerializationUnexpectedValue
from pydantic.annotated_handlers import GetCoreSchemaHandler

# TODO: split into submodules once type interdependency graph is clearer
# TODO: may be useful to split numeric into scalar/vector modules
# TODO: reimplement fractions.Fraction + reciprocal prop

T = TypeVar("T")
P = TypeVar("P")
CT = TypeVar("CT", covariant=True)


ordered = list[T] | tuple[T, ...]



# Numeric = int | float | Decimal | decimal  # | Fraction | Rational
# Realish = Numeric | str

# N = TypeVar("N", bound=Numeric)

# from typing import Generic, TypeVar, Self, Literal
# from enum import Enum

# U = TypeVar("U", bound=LiteralString)

# U = TypeVar("U")

# # TODO: count of type T with prefix P - Generic[T, P]
# class count(int, Generic[U]):
#     __unit: U
#     __type: type[U]

#     @property
#     def unit(self) -> U:
#         return self.__unit

#     @property
#     def type(self) -> type[U]:
#         if self.__type is str:
#             return Literal[self.__unit] # type: ignore
#         raise
#         # return self.__type

#     def __new__(cls, value: int, unit: U, t: type[U] | None = None) -> count[U]:
#         inst = super(count, cls).__new__(cls, value)
#         inst.__unit = unit
#         inst.__type = t if t else type(unit)
#         return inst

#     def __repr__(self) -> str:
#         # return f"{super().__repr__()} [{self.__type.__name__}:{self.__unit}]"
#         return f"{super().__repr__()} [{self.__unit}]"

#     def __eq__(self, other) -> bool: ...

# U = TypeVar("U", bound=LiteralString)

# class _count(int, Generic[U]):
#     __unit: U

#     def __repr__(self) -> str:
#         return f"{super().__repr__()} [{self.__unit}]"

#     def __iter__(self):
#         for k, v in dict(value=int(self), unit=self.unit).items():
#             yield k, v

#     def __new__(cls, value: int, unit: U) -> count[U]:
#         inst = super(count, cls).__new__(cls, value)
#         inst.__unit = unit
#         return inst

#     @property
#     def unit(self) -> U:
#         return self.__unit

#     @unit.setter
#     def unit(self, u: U) -> None:
#         ...





# class ratio(pair[int]): ...


# # 2d point default?
# class point2(pair[decimal]): ...


# # TODO: should be float pair option iff importance(speed) > importance(accuracy)
# # class point(pair[real]):
# #     """
# #     n-dim point
# #     """
# #     ...


# class fpoint(pair[float]): ...


# class ndpoint(tuple[decimal, ...]):
#     @property
#     def dimensions(self) -> positive[int]: ...
