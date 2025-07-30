from __future__ import annotations
import re
import string
from io import StringIO
from abc import abstractmethod
from typing import Callable, ClassVar, Literal, Protocol, Self, Any
from typically import pydantic
from ._standard import SoftConvertibleToStr, normalize

# TODO: ignore space param

DELIMITERS = "-_"
ACRONYMS = re.compile(r"([A-Z])(?=[A-Z])")

CasingName = Literal[
    "alternating",
    "camel",
    "cobol",
    "constant",
    "dot",
    "flat",
    "kebab",
    "lower",
    "macro",
    "pascal",
    "snake",
    "spaced",
    "title",
    "upper",
]


def stripable_punctuation(delimiters: str) -> str:
    """
    Construct a string of stripable punctuation based on delimiters.

    Stripable punctuation is defined as all punctuation that is not a delimiter.
    """
    return "".join([c for c in string.punctuation if c not in delimiters])


# TODO: refactor parameters
class CaseConverter(object):
    def __init__(
        self,
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> None:
        """Initialize a case conversion.

        On initialization, punctuation can be optionally stripped. If
        punctuation is not stripped, it will appear in the output at the
        same position as the input.

        BoundaryHandlers should take into consideration whether or not
        they are evaluating the first character in a string and whether or
        not a character is punctuation.

        Delimiters are taken into consideration when defining stripable
        punctuation.

        Delimiters will be reduced to single instances of a delimiter. This
        includes transforming `   -_-__  `  to `-`.

        During initialization, the raw input string will be passed through
        the prepare_string() method. Child classes should override this
        method if they wish to perform pre-conversion checks and manipulate
        the string accordingly.

        :param s: The raw string to convert.
        :type s: str
        :param delimiters: A set of delimiters used to identify boundaries.
            Defaults to DELIMITERS
        :type delimiters: str
        """
        if space_delimiter:
            delimiters = f" {delimiters}"
        self._delimiters: str = delimiters
        s = s.strip(delimiters)
        if strip_punctuation:
            punctuation = stripable_punctuation(delimiters)
            s = re.sub(r"[{}]+".format(re.escape(punctuation)), "", s)
        if ignore_acronyms:
            s = ACRONYMS.sub(rf"\1{delimiters[-1]}", s)
        # Change recurring delimiters into single delimiters.
        s = re.sub(r"[{}]+".format(re.escape(delimiters)), delimiters[0], s)
        self._raw_input = s
        self._input_buffer = StringIO(self.prepare_string(s))
        self._output_buffer = StringIO()
        self._boundary_handlers: list[BoundaryHandler] = []
        self.define_boundaries()

    @abstractmethod
    def define_boundaries(self) -> None:
        """Define boundary handlers.

        define_boundaries() is called when a CaseConverter is initialized.
        define_boundaries() should be overridden in a child class to add
        boundary handlers.

        A CaseConverter without boundary handlers makes little sense.
        """
        raise NotImplementedError()

    @abstractmethod
    def init(
        self,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        """Initialize the output buffer.

        Can be overridden.

        See convert() for call order.
        """
        raise NotImplementedError()

    @abstractmethod
    def mutate(self, c: str) -> str:
        """Mutate a character not on a boundary.

        Can be overridden.

        See convert() for call order.
        """
        return c

    def add_boundary_handler(self, handler: BoundaryHandler) -> None:
        """
        Add a boundary handler.

        :type handler: BoundaryHandler
        """
        self._boundary_handlers.append(handler)

    def delimiters(self) -> str:
        """Retrieve the delimiters.

        :rtype: str
        """
        return self._delimiters

    def raw(self) -> str:
        """Retrieve the raw string to be converted.

        :rtype: str
        """
        return self._raw_input

    def prepare_string(self, s: str) -> str:
        """Prepare the raw intput string for conversion.

        Executed during CaseConverter initialization providing an opportunity
        for child classes to manipulate the string. By default, the string
        is not manipulated.

        Can be overridden.

        :param s: The raw string supplied to the CaseConverter constructor.
        :type s: str
        :return: A raw string to be used in conversion.
        :rtype: str
        """
        return s

    def _is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> BoundaryHandler | None:
        """Determine if we've hit a boundary or not.

        :rtype: BoundaryHandler
        """
        for bh in self._boundary_handlers:
            if bh.is_boundary(pc, c):
                return bh

        return None

    def convert(self) -> str:
        """Convert the raw string.

        convert() follows a series of steps.

            1. Initialize the output buffer using `init()`.
            For every character in the input buffer:
            2. Check if the current position lies on a boundary as defined
               by the BoundaryHandler instances.
            3. If on a boundary, execute the handler.
            4. Else apply a mutation to the character via `mutate()` and add
               the mutated character to the output buffer.

        :return: The converted string.
        :rtype: str
        """
        self.init(self._input_buffer, self._output_buffer)

        # Previous character (pc) and current character (cc)
        pc = None
        cc = self._input_buffer.read(1)

        while cc:
            bh: BoundaryHandler | None = self._is_boundary(pc, cc)
            if bh:
                bh.handle(pc, cc, self._input_buffer, self._output_buffer)
            else:
                self._output_buffer.write(self.mutate(cc))

            pc = cc
            cc = self._input_buffer.read(1)

        return self._output_buffer.getvalue()


class BoundaryHandler(object):
    """Detect and handle boundaries in a string.

    The BoundaryHandler is an interface for a CaseConverter instance. It provides
    methods for detecting a boundary in a string as well as how to handle
    the boundary.
    """

    @abstractmethod
    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        """Determine if we're on a boundary.

        :param pc: Previous character
        :param cc: Current character
        :return: True if a boundary is found, else false.
        :rtype: boolean
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        """Handle a detected boundary.

        :param pc: Previous character
        :type pc: str
        :param cc: Current character
        :type cc: str
        :param input_buffer: The raw string wrapped in a buffer.
        :type input_buffer: StringBuffer
        :param output_buffer: The output buffer that stores the new string as
            it's constructed.
        :type output_buffer: StringBuffer
        """
        raise NotImplementedError()


class OnDelimiterUppercaseNext(BoundaryHandler):
    def __init__(
        self,
        delimiters: str,
        join_char: str = "",
    ) -> None:
        self._delimiters: str = delimiters
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return c in self._delimiters

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).upper())


class OnDelimiterLowercaseNext(BoundaryHandler):
    def __init__(
        self,
        delimiters: str,
        join_char: str = "",
    ) -> None:
        self._delimiters: str = delimiters
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return c in self._delimiters

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).lower())


class OnUpperPrecededByLowerAppendUpper(BoundaryHandler):
    def __init__(self, join_char: str = "") -> None:
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return pc != None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(self._join_char)
        output_buffer.write(cc)


class OnUpperPrecededByLowerAppendLower(BoundaryHandler):
    def __init__(self, join_char: str = "") -> None:
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return (
            (pc is not None) and pc.isalpha() and pc.islower() and c.isupper()
        )

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(self._join_char)
        output_buffer.write(cc.lower())


class OnUpperPrecededByUpperAppendJoin(BoundaryHandler):
    def __init__(self, join_char: str = "") -> None:
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return pc != None and pc.isalpha() and pc.isupper() and c.isupper()

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(self._join_char)
        output_buffer.write(cc)


class OnUpperPrecededByUpperAppendCurrent(BoundaryHandler):
    def __init__(self, join_char: str = "") -> None:
        self._join_char: str = join_char

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return pc != None and pc.isalpha() and pc.isupper() and c.isupper()

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(cc)


class Alternating(CaseConverter):

    def define_boundaries(self):
        self.add_boundary_handler(self.BoundaryOverride())

    def prepare_string(self, s: str):
        self._toggle_character = False
        return s.lower()

    def mutate(self, c):
        if not c.isalpha():
            return c

        if self._toggle_character:
            self._toggle_character = False
            return c.upper()

        self._toggle_character = True
        return c

    class BoundaryOverride(BoundaryHandler):
        def is_boundary(
            self,
            pc: str | None,
            c: str,
        ) -> bool:
            return False


class Camel(CaseConverter):
    def define_boundaries(self):
        self.add_boundary_handler(OnDelimiterUppercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper())

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Cobol(CaseConverter):

    JOIN_CHAR = "-"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimiterUppercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(
            OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR)
        )

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimiters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Cobol, self).convert()

    def mutate(self, c):
        return c.upper()


class Flat(CaseConverter):
    def define_boundaries(self):
        self.add_boundary_handler(OnDelimiterLowercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower())

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Kebab(CaseConverter):

    JOIN_CHAR = "-"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimiterLowercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(
            OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR)
        )

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Macro(CaseConverter):

    JOIN_CHAR = "_"

    def __init__(self, *args, delims_only=False, **kwargs):
        self._delims_only = delims_only
        super(Macro, self).__init__(*args, **kwargs)

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimiterUppercaseNext(self.delimiters(), self.JOIN_CHAR)
        )

        if not self._delims_only:
            self.add_boundary_handler(
                OnUpperPrecededByLowerAppendUpper(self.JOIN_CHAR)
            )
            self.add_boundary_handler(
                OnUpperPrecededByUpperAppendJoin(self.JOIN_CHAR)
            )

    def convert(self):
        if self.raw().isupper():
            return re.sub(
                "[{}]+".format(re.escape(self.delimiters())),
                self.JOIN_CHAR,
                self.raw(),
            )

        return super(Macro, self).convert()

    def mutate(self, c):
        return c.upper()


class Pascal(CaseConverter):
    def init(
        self,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(input_buffer.read(1).upper())

    def define_boundaries(self):
        self.add_boundary_handler(OnDelimiterUppercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendUpper())
        self.add_boundary_handler(OnUpperPrecededByUpperAppendCurrent())

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Snake(CaseConverter):

    JOIN_CHAR = "_"

    def define_boundaries(self):
        self.add_boundary_handler(
            OnDelimiterLowercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(
            OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR)
        )

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


class Title(CaseConverter):
    def init(
        self,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        # Capitalize the first character
        output_buffer.write(input_buffer.read(1).upper())

    def define_boundaries(self):
        # On delimiters, write the space and make the next character uppercase
        self.add_boundary_handler(
            OnDelimiterPreserveAndUpperNext(self.delimiters())
        )
        # Handle camelCase -> Title Case
        self.add_boundary_handler(OnUpperPrecededByLowerAddSpace())

    def prepare_string(self, s: str):
        if s.isupper():
            return s.lower()
        return s

    def mutate(self, c):
        return c.lower()


class OnDelimiterPreserveAndUpperNext(OnDelimiterUppercaseNext):
    """Boundary handler that preserves spaces"""

    def __init__(self, delimiters: str) -> None:
        super().__init__(delimiters)
        self._delimiters: str = delimiters

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        # Write a single space for any delimiter
        output_buffer.write(" ")
        # Get and capitalize the next character
        output_buffer.write(input_buffer.read(1).upper())


class OnUpperPrecededByLowerAddSpace(BoundaryHandler):
    """
    New boundary handler for camelCase
    """

    def is_boundary(
        self,
        pc: str | None,
        c: str,
    ) -> bool:
        return pc is not None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(
        self,
        pc: str | None,
        cc: str,
        input_buffer: StringIO,
        output_buffer: StringIO,
    ) -> None:
        output_buffer.write(" ")
        output_buffer.write(cc)


class Lower(CaseConverter):
    def define_boundaries(self) -> None:
        self.add_boundary_handler(OnDelimiterLowercaseNext(self.delimiters()))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower())

    def init(self, input_buffer: StringIO, output_buffer: StringIO) -> None:
        char = input_buffer.read(1)
        if char:
            output_buffer.write(char.lower())

    def prepare_string(self, s: str) -> str:
        if s.isupper():
            return s.lower()
        return s

    def mutate(self, c: str) -> str:
        return c.lower()


class Dot(CaseConverter):
    JOIN_CHAR = "."

    def define_boundaries(self) -> None:
        self.add_boundary_handler(
            OnDelimiterLowercaseNext(self.delimiters(), self.JOIN_CHAR)
        )
        self.add_boundary_handler(
            OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR)
        )

    def init(self, input_buffer: StringIO, output_buffer: StringIO) -> None:
        char = input_buffer.read(1)
        if char:
            output_buffer.write(char.lower())

    def prepare_string(self, s: str) -> str:
        if s.isupper():
            return s.lower()
        return s

    def mutate(self, c: str) -> str:
        return c.lower()


class Spaced(CaseConverter):
    def __init__(
        self,
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> None:
        raise NotImplementedError()
        super().__init__(
            s, delimiters, space_delimiter, strip_punctuation, ignore_acronyms
        )


class casing:
    @staticmethod
    def alternating(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to alternating case, or its better known name: mocking Spongebob case.

        Example

            Hello World => hElLo WoRlD

        """
        return Alternating(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def camel(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to camel case.

        Example

        Hello World => helloWorld

        """
        return Camel(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def cobol(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to cobol case

        Example

        Hello World => HELLO-WORLD

        """
        return Cobol(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def constant(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        return (
            Snake(
                s=s,
                delimiters=delimiters,
                space_delimiter=space_delimiter,
                strip_punctuation=strip_punctuation,
                ignore_acronyms=ignore_acronyms,
            )
            .convert()
            .upper()
        )

    @staticmethod
    def dot(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        return Dot(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def kebab(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to kebab case

        Example

            Hello World => hello-world

        """
        return Kebab(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def lower(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        return Lower(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def macro(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to macro case

        Example

            Hello World => HELLO_WORLD

        """
        return Macro(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def pascal(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to pascal case

        Example

            Hello World => HelloWorld
            hello world => HelloWorld

        """
        return Pascal(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def snake(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to snake case.

        Example

            Hello World => hello_world

        """
        return Snake(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def title(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to title case.

        Example:
            Hello world => Hello World
            hello-world => Hello World
            helloWorld => Hello World
        """
        return Title(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def flat(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        """Convert a string to flat case

        Example

            Hello World => helloworld

        """
        return Flat(
            s=s,
            delimiters=delimiters,
            space_delimiter=space_delimiter,
            strip_punctuation=strip_punctuation,
            ignore_acronyms=ignore_acronyms,
        ).convert()

    @staticmethod
    def upper(
        s: str,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> str:
        return (
            Lower(
                s=s,
                delimiters=delimiters,
                space_delimiter=space_delimiter,
                strip_punctuation=strip_punctuation,
                ignore_acronyms=ignore_acronyms,
            )
            .convert()
            .upper()
        )


class BaseCasedStr(str):
    converter: ClassVar[Callable[[str, str, bool, bool, bool], str]]

    def __new__(
        cls,
        value: SoftConvertibleToStr,
        delimiters: str = DELIMITERS,
        space_delimiter: bool = True,
        strip_punctuation: bool = True,
        ignore_acronyms: bool = True,
    ) -> Self:
        value = normalize(value)
        value = cls.converter(
            value,
            delimiters,
            space_delimiter,
            strip_punctuation,
            ignore_acronyms,
        )
        return str.__new__(cls, value)

    @classmethod
    def __serialize__(
        cls,
        value: Self,
        info: pydantic.SerializationInfo,
    ) -> str | Self:
        if not isinstance(value, cls):
            raise pydantic.PydanticSerializationUnexpectedValue(
                f"Expected `{cls}` but got `{type(value)}` with value `'{value}'` - serialized value may not be as expected."
            )
        if info.mode == "json":
            return str(value)
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
            value = normalize(value)
            return source.__new__(source, value)

        return pydantic.no_info_wrap_validator_function(
            wrapper,
            schema=pydantic.str_schema(),
            serialization=pydantic.plain_serializer_function_ser_schema(
                cls.__serialize__,
                info_arg=True,
                when_used="always",
            ),
        )


class cased:
    class alternating(BaseCasedStr):
        converter = casing.alternating

    class camel(BaseCasedStr):
        converter = casing.camel

    class cobol(BaseCasedStr):
        converter = casing.cobol

    class constant(BaseCasedStr):
        converter = casing.constant

    class dot(BaseCasedStr):
        converter = casing.dot

    class flat(BaseCasedStr):
        converter = casing.flat

    class kebab(BaseCasedStr):
        converter = casing.kebab

    class lower(BaseCasedStr):
        converter = casing.lower

    class macro(BaseCasedStr):
        converter = casing.macro

    class pascal(BaseCasedStr):
        converter = casing.pascal

    class snake(BaseCasedStr):
        converter = casing.snake

    # class spacedcase(CasedStr):
    #     converter = casing.spaced

    class title(BaseCasedStr):
        converter = casing.title

    class upper(BaseCasedStr):
        converter = casing.upper
