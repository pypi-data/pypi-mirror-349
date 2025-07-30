"""
Useful types, not sure if they're 'hidden', but pylance struggles to recognize them.

If this module causes errors then LMK on github cause I think they would be fixed
with some try/except blocks, but don't want to both right now. EG:

```python
try:
    LiteralGenericAlias = typing._LiteralGenericAlias  # type: ignore
except:
    LiteralGenericAlias = type(typing.Literal[""])
```
"""
import typing

LiteralGenericAlias = typing._LiteralGenericAlias  # type: ignore
Final = typing._Final # type: ignore
NotIterable = typing._NotIterable # type: ignore
SpecialForm = typing._SpecialForm # type: ignore
AnyMeta = typing._AnyMeta # type: ignore
BaseGenericAlias = typing._BaseGenericAlias # type: ignore
GenericAlias = typing._GenericAlias # type: ignore
SpecialGenericAlias = typing._SpecialGenericAlias # type: ignore

# ~3.11
# TypedCacheSpecialForm = typing._TypedCacheSpecialForm # type: ignore
# Sentinel = typing._Sentinel # type: ignore

# TODO: add others as needed