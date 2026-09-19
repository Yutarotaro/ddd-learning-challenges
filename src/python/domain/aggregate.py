from entity import Book
from value_object import BookCopyId, ISBN, LendingStatus, MemberId, MemberName, LoanLimit

## Aggregate Root

class BookCopy:
    """
    BookCopy / 蔵書
    図書館が所有し、実際に貸し出す1冊
    """
    id: BookCopyId
    isbn: ISBN
    status: LendingStatus

class Member:
    """
    Member / 利用者
    図書館の利用者
    """
    id: MemberId
    name: MemberName
    loan_limit: LoanLimit = LoanLimit(value=3)  # デフォルトの貸出冊数制限: 3冊

    def borrow(self, book_copy: BookCopy, loan_date: str):
        """
        蔵書を借りる
        ルール:
        - 蔵書の貸出状況がAVAILABLEであること（貸出中の蔵書は借りられない）
        """
        if book_copy.status != LendingStatus.AVAILABLE:
            raise ValueError("Book copy is not available for borrowing")
        # 蔵書の貸出状況を更新する
        book_copy.status = LendingStatus.LENT_OUT