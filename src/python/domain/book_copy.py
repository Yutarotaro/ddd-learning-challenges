from enum import StrEnum

from .book import ISBN
from .value_objects import BookCopyId

# Value Objects


class LendingStatus(StrEnum):
    """
    貸出状況
    """

    AVAILABLE = "available"  # 貸出可能
    LENT_OUT = "lent_out"  # 貸出中


class BookCopy:
    """
    BookCopy / 蔵書
    図書館が所有し、実際に貸し出す1冊
    """

    def __init__(self, id: BookCopyId, isbn: ISBN):
        self.id: BookCopyId = id
        self.isbn: ISBN = isbn
        self._status: LendingStatus = LendingStatus.AVAILABLE  # 初期状態はAVAILABLE

    @property
    def status(self) -> LendingStatus:  # ReadOnly
        return self._status

    def _is_available(self) -> bool:
        """
        蔵書が貸出可能かどうかを判定する
        """
        return self.status == LendingStatus.AVAILABLE

    def lend_out(self):
        """
        蔵書を貸し出す
        """
        # 蔵書が貸出可能かどうかを判定する
        if not self._is_available():
            raise ValueError("Book copy is not available for lending")

        # 蔵書の貸出状況を更新する
        self._status = LendingStatus.LENT_OUT

    def mark_as_return(self):
        """ "
        蔵書を返却する
        """
        self._status = LendingStatus.AVAILABLE
