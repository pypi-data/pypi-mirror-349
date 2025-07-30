from __future__ import annotations
from decimal import Decimal, Context, DecimalTuple
from typing import Any, TypeVar, Self


# TODO: real needs pydantic schema impl.
# TODO: reimplement in rust
# TODO: add precision/precise number of significant figures
# TODO: optimize, lot of bloat
# ? real, precise, decimal
class decimal(Decimal):
    """
    Same as decimal but with greater interoperability across other numeric types.

    NOTE: `float` to `str` cast
        Instantiating `Decimal(3.14)` yields the decimal:

        `Decimal('3.140000000000000124344978758017532527446746826171875')`

        This is probably because even though `Decimal` has arbitrary precision,
        the float passed in doesn't. As such input floats are converted to strings
        before being passed to the constructor.

    NOTE: Infinity
        ```python
        x = Decimal(0) / Decimal('inf')
        ```

        In the code above, `x == Decimal('0E-1000026')`.
        Accordingly infinity has just been blocked from being a valid value.
        May re-evaluate later.
    """

    # precision: ClassVar[int] = 16

    # TODO: test with numpy/sympy types, make sure this works w/ array, sparse matrices, etc

    # * core methods

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__str__()})"

    def __hash__(self) -> int:
        return super().__hash__()

    def __copy__(self) -> decimal:
        return decimal(super().__copy__())

    def __deepcopy__(self, memo: Any) -> decimal:
        return decimal(super().__deepcopy__(memo))

    # * constructors

    def __new__(
        cls,
        value: ConvertibleToDecimal,
        context: Context | None = None,
    ) -> decimal:
        if isinstance(value, float):
            value = str(value)
        lstr = str(value).lower()
        if "inf" in lstr:
            raise TypeError(f"'{cls.__name__}' does not allow infinite value")
        if "nan" in lstr:
            raise TypeError(f"'{cls.__name__}' does not allow nan values")
        return Decimal.__new__(cls, value=value, context=context)

    @classmethod
    def from_numeric(cls, value: Numeric) -> decimal:
        if isinstance(value, str):
            raise TypeError(f"{type(value)}: '{value}'")
        return cls(value)

    @classmethod
    def from_float(cls, f: float) -> Self:
        return cls(str(f))

    # * type conversion

    def __bool__(self) -> bool:
        return super().__bool__()

    def __float__(self) -> float:
        return super().__float__()

    def __int__(self) -> int:
        return super().__int__()

    def __complex__(self) -> complex:
        return super().__complex__()

    @property
    def decimal(self) -> Decimal:
        return Decimal(self)

    def as_integer_ratio(
        self,
    ) -> tuple[int, int]: ...  # TODO: replace with ratio / pair[int]

    # * formatting

    def to_eng_string(self, context: Context | None = None) -> str:
        return super().to_eng_string(context=context)

    def __format__(
        self, specifier: str, context: Context | None = None
    ) -> str:
        return super().__format__(specifier, context)

    # * comparison

    def __eq__(self, value: object) -> bool:  # type: ignore
        if not isinstance(value, Numeric):
            return False
        return super().__eq__(decimal.from_numeric(value))

    def __ne__(self, value: object) -> bool:  # type: ignore
        if not isinstance(value, Numeric):
            return True
        return super().__ne__(decimal.from_numeric(value))

    def __ge__(self, value: Numeric) -> bool:  # type: ignore
        return super().__ge__(decimal.from_numeric(value))

    def __gt__(self, value: Numeric) -> bool:  # type: ignore
        return super().__gt__(decimal.from_numeric(value))

    def __le__(self, value: Numeric) -> bool:  # type: ignore
        return super().__le__(decimal.from_numeric(value))

    def __lt__(self, value: Numeric) -> bool:  # type: ignore
        return super().__lt__(decimal.from_numeric(value))

    # * sign

    def __abs__(self) -> decimal:
        return decimal(super().__abs__())

    def __neg__(self) -> decimal:
        return decimal(super().__neg__())

    def __pos__(self) -> decimal:
        return decimal(super().__pos__())

    # * addition

    def __add__(self, value: Numeric) -> decimal:
        return decimal(super().__add__(decimal.from_numeric(value)))

    def __radd__(self, value: Numeric) -> decimal:
        return decimal(super().__radd__(decimal.from_numeric(value)))

    # * subtraction

    def __sub__(self, value: Numeric) -> decimal:
        return decimal(super().__sub__(decimal.from_numeric(value)))

    def __rsub__(self, value: Numeric) -> decimal:
        return decimal(super().__rsub__(decimal.from_numeric(value)))

    # * multiplication

    def __mul__(self, value: Numeric) -> decimal:
        return decimal(super().__mul__(decimal.from_numeric(value)))

    def __rmul__(self, value: Numeric) -> decimal:
        return decimal(super().__rmul__(decimal.from_numeric(value)))

    # * division

    def __truediv__(self, value: Numeric) -> decimal:
        return decimal(super().__truediv__(decimal.from_numeric(value)))

    def __rtruediv__(self, value: Numeric) -> decimal:
        return decimal(super().__rtruediv__(decimal.from_numeric(value)))

    def __floordiv__(self, value: Numeric) -> decimal:
        return decimal(super().__floordiv__(decimal.from_numeric(value)))

    def __rfloordiv__(self, value: Numeric) -> decimal:
        return decimal(super().__rfloordiv__(decimal.from_numeric(value)))

    # * modulo

    def __mod__(self, value: Numeric) -> decimal:
        return decimal(super().__mod__(decimal.from_numeric(value)))

    def __rmod__(self, value: Numeric) -> decimal:
        return decimal(super().__rmod__(decimal.from_numeric(value)))

    def __divmod__(self, value: Numeric) -> tuple[decimal, decimal]:
        dt = super().__divmod__(decimal.from_numeric(value))
        return (decimal(dt[0]), decimal(dt[1]))

    def __rdivmod__(self, value: Numeric) -> tuple[Decimal, Decimal]:
        raise NotImplementedError()

    # * exponentation / logarithms

    def __pow__(self, value: Numeric, mod: Numeric | None = None) -> decimal:
        mod = decimal(mod).decimal if mod else None
        return decimal(
            super().__pow__(decimal.from_numeric(value).decimal, mod)
        )

    def __rpow__(self, value: Numeric, mod: Context | None = None) -> decimal:
        return decimal(
            super().__rpow__(decimal.from_numeric(value).decimal, mod)
        )

    def exp(self, context: Context | None = None) -> decimal:
        return decimal(super().exp(context))

    def sqrt(self, context: Context | None = None) -> decimal:
        return decimal(super().sqrt(context))

    def ln(self, context: Context | None = None) -> decimal:
        return decimal(super().ln(context))

    def log10(self, context: Context | None = None) -> decimal:
        return decimal(super().log10(context))

    def logb(self, context: Context | None = None) -> decimal:
        return decimal(super().logb(context))

    # * rounding

    def __round__(self, ndigits: int = 0) -> decimal:  # type: ignore
        return decimal(super().__round__(ndigits))

    def __floor__(self) -> int:
        return super().__floor__()

    def __ceil__(self) -> int:
        return super().__ceil__()

    # * stats
    def max(self, other: Numeric, context: Context | None = None) -> decimal:
        return decimal(super().max(decimal(other).decimal, context))

    def min(self, other: Numeric, context: Context | None = None) -> decimal:
        return decimal(super().min(decimal(other).decimal, context))

    # TODO
    @property
    def real(self) -> Self: ...
    @property
    def imag(self) -> decimal: ...
    def __trunc__(self) -> int: ...
    def conjugate(self) -> decimal: ...
    def remainder_near(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def normalize(self, context: Context | None = None) -> decimal: ...
    def fma(
        self, other: Numeric, third: Numeric, context: Context | None = None
    ) -> decimal: ...
    def quantize(
        self,
        exp: Numeric,
        rounding: str | None = None,
        context: Context | None = None,
    ) -> decimal: ...
    def same_quantum(
        self, other: Numeric, context: Context | None = None
    ) -> bool: ...
    def to_integral_exact(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def to_integral_value(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def to_integral(
        self, rounding: str | None = None, context: Context | None = None
    ) -> decimal: ...
    def adjusted(self) -> int: ...
    def canonical(self) -> decimal: ...
    def compare_signal(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def compare_total(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def compare_total_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def copy_abs(self) -> decimal: ...
    def copy_negate(self) -> decimal: ...
    def copy_sign(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def is_canonical(self) -> bool: ...
    def is_finite(self) -> bool: ...
    def is_infinite(self) -> bool: ...
    def is_nan(self) -> bool: ...
    def is_normal(self, context: Context | None = None) -> bool: ...
    def is_qnan(self) -> bool: ...
    def is_signed(self) -> bool: ...
    def is_snan(self) -> bool: ...
    def is_subnormal(self, context: Context | None = None) -> bool: ...
    def is_zero(self) -> bool: ...
    def logical_and(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def logical_invert(self, context: Context | None = None) -> decimal: ...
    def logical_or(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def logical_xor(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def max_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def min_mag(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def next_minus(self, context: Context | None = None) -> decimal: ...
    def next_plus(self, context: Context | None = None) -> decimal: ...
    def next_toward(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def number_class(self, context: Context | None = None) -> str: ...
    def radix(self) -> decimal: ...
    def rotate(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def scaleb(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def shift(
        self, other: Numeric, context: Context | None = None
    ) -> decimal: ...
    def __reduce__(self) -> tuple[type[Self], tuple[str]]: ...
    def as_tuple(self) -> DecimalTuple: ...


# * type redefinitions

Numeric = int | float | Decimal | decimal  # | Fraction | Rational
ConvertibleToDecimal = Numeric | str

N = TypeVar("N", bound=Numeric)