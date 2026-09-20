from dataclasses import dataclass
from typing import Self
import uuid


@dataclass(frozen=True, slots=True)
class MemberId:
    """利用者ID"""

    value: uuid.UUID

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> Self:
        return cls(value=uuid.uuid4())


@dataclass(frozen=True, slots=True)
class BookCopyId:
    """蔵書ID"""

    value: uuid.UUID

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> Self:
        return cls(value=uuid.uuid4())


@dataclass(frozen=True, slots=True)
class LoanId:
    """貸出ID"""

    value: uuid.UUID

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> Self:
        return cls(value=uuid.uuid4())
