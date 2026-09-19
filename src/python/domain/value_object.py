from dataclasses import dataclass
from enum import StrEnum

import uuid
from typing import Self

## Value Objects

@dataclass(frozen=True, slots=True)
class ISBN:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("ISBN cannot be empty")
        if self.value.strip() == "":
            raise ValueError("ISBN cannot be whitespace only")

    def __str__(self):
        return self.value

@dataclass(frozen=True, slots=True)
class BookTitle:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Book title cannot be empty")
        if self.value.strip() == "":
            raise ValueError("Book title cannot be whitespace only")

    def __str__(self):
        return self.value

@dataclass(frozen=True, slots=True)
class BookCopyId:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("BookCopyId cannot be empty")
        if self.value.strip() == "":
            raise ValueError("BookCopyId cannot be whitespace only")

    def __str__(self):
        return self.value

class LendingStatus(StrEnum):
    """
    貸出状況
    """
    AVAILABLE = "available"
    LENT_OUT = "lent_out"

@dataclass(frozen=True, slots=True)
class MemberId:
    """
    利用者ID
    """
    value: uuid.UUID

    def __str__(self):
        return str(self.value)

    @classmethod
    def generate(cls) -> Self:
        """
        新しい利用者IDを生成する
        """
        return cls(value=uuid.uuid4())

@dataclass(frozen=True, slots=True)
class MemberName:
    """
    利用者名
    """
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Name must be a string")
        if len(self.value) == 0:
            raise ValueError("Member name cannot be empty")
        if len(self.value) > 50:
            raise ValueError("Member name cannot exceed 50 characters")
        if self.value.strip() == "":
            raise ValueError("Member name cannot be whitespace only")

    def __str__(self):
        return self.value

@dataclass(frozen=True, slots=True)
class LoanLimit:
    """
    貸出上限数
    """
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Loan limit must be a positive integer")