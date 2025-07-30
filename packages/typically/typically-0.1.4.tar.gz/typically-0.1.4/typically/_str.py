from __future__ import annotations
import builtins
from typing import Iterable, SupportsIndex, overload
from typing_extensions import LiteralString
from typically.lt._uuid import UUIDVersion


class str(builtins.str):

    # @property
    # def encoding(self) -> literal.CharacterEncoding: ...

    def isuuid(self, version: UUIDVersion) -> bool: ...

    # def tocase(self, casing: ...): ...

    def dedent(self) -> str: ...
    def escape(self) -> str: ...
    def apply(self): ...
    def duplicate(self): ...

    # TODO: regex utils

    # @overload
    # def replace(
    #     self: LiteralString,
    #     old: LiteralString,
    #     new: LiteralString,
    #     /,
    #     count: SupportsIndex = -1,
    # ) -> LiteralString: ...
    # @overload
    # def replace(
    #     self,
    #     old: str,
    #     new: str,
    #     /,
    #     count: SupportsIndex = -1,
    # ) -> str: ...  # type: ignore[misc]
    # @overload
    # def replace(self, mapping: dict[str, str]) -> str: ...  # TODO

    # @overload
    # def replace(self: builtins.str, *args, **kwargs) -> builtins.str: ...
    # @overload
    # def replace(self: str, *args, **kwargs) -> str: ...
    # def replace(self, *args, **kwargs) -> str:
    #     return super().replace(*args, **kwargs)

    def fuzzysearch(
        self, query: str, window: int | None = None, n: int = 1
    ) -> _fuzzy_search_result | list[_fuzzy_search_result]: ...

    @overload
    def cjoin(
        self: LiteralString, iterable: Iterable[LiteralString], /
    ) -> str: ...
    @overload
    def cjoin(self, iterable: Iterable[str], /) -> str: ...  # type: ignore[misc]
    def cjoin(
        self: LiteralString | str | str,
        iterable: Iterable[str] | Iterable[LiteralString],
        /,
        exclude_none: bool = True,
    ) -> str: ...


# class _estr_slice(str): ...
class _fuzzy_search_result(str): ...


class substring: ...


class line: ...
