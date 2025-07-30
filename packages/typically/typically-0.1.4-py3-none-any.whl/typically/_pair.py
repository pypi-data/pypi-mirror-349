from __future__ import annotations
import typing
from typically import pydantic as py

T = typing.TypeVar("T")


class pair(tuple[T, T]):
    @classmethod
    def __new_args__(cls, *args) -> pair[T]:
        match len(args):
            case 1:
                arg = args[0]
                if len(arg) == 2:
                    return tuple.__new__(cls, arg)
                else:
                    raise TypeError(
                        f"'{cls.__name__}' expects 2 args or an iterable of length 2, but received length {len(arg)}: '{arg}'",
                    )
            case 2:
                return tuple.__new__(cls, args)
            case _:
                raise TypeError(args)

    @classmethod
    def __new_kwargs__(cls, **kwargs) -> pair[T]:
        # FIXME
        keys = set(kwargs.keys())
        if keys == {"value"}:
            return cls.__new_args__(*kwargs["value"])
        elif keys == {"a", "b"}:
            return cls.__new_args__(kwargs["a"], kwargs["b"])
        else:
            raise TypeError(f"Invalid keyword arguments: {kwargs}")

    @typing.overload
    def __new__(cls, value: pair[T] | tuple[T, T] | list[T]) -> pair[T]: ...
    @typing.overload
    def __new__(cls, a: T, b: T) -> pair[T]: ...
    def __new__(cls, *args, **kwargs) -> pair[T]:
        if len(args):
            return cls.__new_args__(*args)
        elif len(kwargs):
            return cls.__new_kwargs__(**kwargs)
        else:
            raise TypeError(
                f"{cls.__name__} expects a pair of two items, or an iterable of length 2",
                args,
                kwargs,
            )

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    @property
    def a(self) -> T:
        return self[0]

    @property
    def b(self) -> T:
        return self[1]

    @classmethod
    def __serialize__(
        cls,
        value: pair[T],
        info: py.SerializationInfo,
    ) -> tuple[T, ...] | typing.Self:
        if not isinstance(value, cls):
            raise py.PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return tuple(value)
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[pair[T]],
        handler: py.GetCoreSchemaHandler,
    ) -> py.CoreSchema:
        def wrapper(
            value: typing.Any, wrap_handler: py.ValidatorFunctionWrapHandler
        ):
            generic_param_types: tuple[type, ...] = typing.get_args(source)
            match len(generic_param_types):
                case 0:
                    return source.__new__(source, value)
                case 1:
                    generic_type: type = generic_param_types[0]
                    new_value = list()
                    for item in value:
                        if isinstance(item, generic_type):
                            new_value.append(item)
                        else:
                            try:
                                new_value.append(generic_type(item))
                            except ValueError:
                                raise TypeError(
                                    f"Could not coerce value '{item}' to type '{generic_type.__name__}'"
                                )
                    return source.__new__(source, value.__class__(new_value))
                case _:
                    raise TypeError(
                        f"'pair' can only have one generic type, but has: '{generic_param_types}'"
                    )

        return py.no_info_wrap_validator_function(
            wrapper,
            schema=py.tuple_schema(
                [py.any_schema(), py.any_schema()],
                variadic_item_index=1,
                min_length=2,
                max_length=2,
                strict=True,
            ),
            serialization=py.plain_serializer_function_ser_schema(
                cls.__serialize__, info_arg=True, when_used="always"
            ),
        )
