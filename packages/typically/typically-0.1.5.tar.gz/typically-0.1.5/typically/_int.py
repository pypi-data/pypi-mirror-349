from __future__ import annotations
import builtins
from abc import abstractmethod
from typing import Self, Protocol, Any
from ._typeshed import ConvertibleToInt
from . import pydantic


class IsOddError(ValueError): ...


class IsEvenError(ValueError): ...


class AbstractPydanticIntSerializer(Protocol):
    @abstractmethod
    def __new__(cls, value: ConvertibleToInt) -> Self: ...

    @classmethod
    def __serialize__(
        cls,
        value: Self,
        info: pydantic.SerializationInfo,
    ) -> int | Self:
        if not isinstance(value, cls):
            raise pydantic.PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return int(value)  # type: ignore
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Self],
        handler: pydantic.GetCoreSchemaHandler,
    ) -> pydantic.CoreSchema:
        def wrapper(
            value: Any,
            wrap_handler: pydantic.ValidatorFunctionWrapHandler,
        ) -> Self:
            return source.__new__(source, value)

        return pydantic.no_info_wrap_validator_function(
            wrapper,
            schema=pydantic.int_schema(),
            serialization=pydantic.plain_serializer_function_ser_schema(
                cls.__serialize__,
                info_arg=True,
                when_used="always",
            ),
        )


class odd(int, AbstractPydanticIntSerializer):
    def __new__(cls, value: ConvertibleToInt) -> odd:
        value = int(value)
        if not (value % 2):
            raise IsEvenError(value)
        return int.__new__(cls, value)


class even(int, AbstractPydanticIntSerializer):
    def __new__(cls, value: ConvertibleToInt) -> even:
        value = int(value)
        if value % 2:
            raise IsOddError(value)
        return int.__new__(cls, value)


# class whole(int): ...

# class natural(int): ...
