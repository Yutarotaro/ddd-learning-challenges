from dataclasses import dataclass


# Value Objects
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
