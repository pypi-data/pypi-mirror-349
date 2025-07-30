from __future__ import annotations
from typing import Literal


CommonChecksumAlgorithm = Literal["sha265", "md5"]


class Checksum(str):
    algorithm: CommonChecksumAlgorithm
    value: str

    def __new__(
        cls,
        value: str,
        algorithm: CommonChecksumAlgorithm | None = None,
    ) -> Checksum: ...
