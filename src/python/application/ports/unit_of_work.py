from abc import ABC, abstractmethod

from .member_repository import MemberRepository
from .book_copy_repository import BookCopyRepository


class UnitOfWork(ABC):
    member_repository: MemberRepository
    book_copy_repository: BookCopyRepository

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError
