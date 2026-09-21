from abc import ABC, abstractmethod

from domain.book_copy import BookCopyId, BookCopy


class BookCopyRepository(ABC):
    @abstractmethod
    def get(self, book_copy_id: BookCopyId) -> BookCopy:
        raise NotImplementedError

    @abstractmethod
    def save(self, book_copy: BookCopy) -> None:
        raise NotImplementedError
