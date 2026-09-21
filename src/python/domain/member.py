from .errors import LoanLimitExceededError, NotFoundError
from .loan import Loan, LoanLimit
from .value_objects import BookCopyId, LoanId, MemberId

from dataclasses import dataclass
from datetime import date


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


class Member:
    """
    Member / 利用者
    図書館の利用者
    """

    def __init__(self, id: MemberId, name: MemberName):
        self._id = id
        self._name = name
        self._loan_limit = LoanLimit(value=3)  # デフォルトの貸出冊数制限: 3冊
        self._loans: dict[LoanId, Loan] = (
            {}
        )  # 貸出情報を保持するdictionary。キーはLoanId、値はLoanオブジェクト

    @property
    def id(self) -> MemberId:
        return self._id

    @property
    def name(self) -> MemberName:
        return self._name

    @property
    def loans(self):
        """
        利用者の貸出情報を取得する
        """
        return self._loans

    def get_loan(self, loan_id: LoanId):
        loan = self._loans.get(loan_id)
        if loan is None:
            raise NotFoundError("The loan is not found")
        return loan

    def borrow_book(self, book_copy_id: BookCopyId, loan_date: date) -> Loan:
        """
        利用者が蔵書を借りる処理を行う
        貸出: Loan オブジェクトを生成し、Memberの貸出情報に追加する
        """
        # ========= 蔵書が貸出可能かどうかを判定する ==========
        self._ensure_not_exceed_loan_limit()  # 貸出上限冊数に達していないことを確認する
        self._ensure_no_overdue_loans(
            loan_date
        )  # 未返却で延滞中の蔵書がないことを確認する
        self._ensure_not_already_borrowed(
            book_copy_id
        )  # 同じ蔵書を同じ会員が同時に重複して借りられない

        # ========== 蔵書の貸出状況を更新する ==========
        loan = Loan.create(
            book_copy_id=book_copy_id, member_id=self._id, loan_date=loan_date
        )
        if loan.id in self._loans:
            raise ValueError("Loan with this ID already exists for this member.")
        self._loans[loan.id] = loan  # Memberの貸出情報に追加
        return loan

    def return_book(self, loan_id: LoanId, return_date: date) -> None:
        """
        利用者が蔵書を返却する処理を行う
        """
        loan = self.get_loan(loan_id)
        loan.mark_as_returned(return_date)  # 貸出情報の返却日を更新する

    # Private Methods
    def _ensure_not_exceed_loan_limit(self):
        """
        貸出上限冊数に達していないことを確認する
        """
        active_loans_count = len(
            [loan for loan in self._loans.values() if not loan.is_returned]
        )
        if active_loans_count >= self._loan_limit.value:
            raise LoanLimitExceededError(
                "You have reached your loan limit. Please return a book before borrowing another."
            )

    def _ensure_no_overdue_loans(self, on_date: date):
        """
        未返却で延滞中の蔵書がないことを確認する
        """
        overdue_loans = [
            loan
            for loan in self._loans.values()
            if not loan.is_returned and loan.is_overdue(on_date)
        ]
        if overdue_loans:
            raise ValueError(
                "You have overdue loans. Please return them before borrowing another book."
            )

    def _ensure_not_already_borrowed(self, book_copy_id: BookCopyId):
        """
        同じ蔵書を同じ会員が現在借りていないことを確認する
        """
        if book_copy_id in [
            loan.book_copy_id for loan in self._loans.values() if not loan.is_returned
        ]:
            raise ValueError("You have already borrowed this book.")
