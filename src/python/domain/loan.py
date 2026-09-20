from .value_objects import BookCopyId, LoanId, MemberId

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Self


# Value Objects
@dataclass(frozen=True, slots=True)
class LoanLimit:
    """
    貸出上限数
    """

    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Loan limit must be a positive integer")


@dataclass(frozen=True, slots=True)
class LoanPeriod:
    """
    貸出期間
    """

    loan_date: date
    DURATION_DAYS = 14  # 貸出期間は14日間

    @property
    def due_date(self) -> date:
        """
        返却期限日を計算する
        """
        return self.loan_date + timedelta(
            days=self.DURATION_DAYS - 1
        )  # 貸出日を含めて14日間


# Entity
class Loan:
    """
    Loan / 貸出
    """

    def __init__(
        self,
        loan_id: LoanId,
        book_copy_id: BookCopyId,
        member_id: MemberId,
        loan_date: date,
        returned_date: date = None,
    ):
        self._id: LoanId = loan_id
        self._book_copy_id: BookCopyId = book_copy_id
        self._member_id: MemberId = member_id
        self._loan_date: date = loan_date  # 貸出日
        self._loan_period: LoanPeriod = LoanPeriod(
            loan_date=loan_date
        )  # 貸出期間 .due_dateで貸出期限
        self._returned_date: date | None = (
            returned_date  # 返却日を初期化（未返却の場合はNone）
        )

    @property
    def id(self) -> LoanId:
        return self._id

    @property
    def book_copy_id(self) -> BookCopyId:
        return self._book_copy_id

    @property
    def is_returned(self) -> bool:
        """
        貸出が返却済みかどうかを判定する
        """
        return self._returned_date is not None

    def is_overdue(self, on_date: date | None = None) -> bool:
        """
        貸出が期限切れかどうかを判定する
        """
        if self.is_returned:
            return False  # 返却済みの場合は期限切れではない

        today = on_date or date.today()  # 引数がNoneの場合は今日の日付を使用
        return (
            today > self._loan_period.due_date
        )  # 今日の日付が返却期限日を過ぎているかどうかを判定

    @classmethod
    def create(
        cls, book_copy_id: BookCopyId, member_id: MemberId, loan_date: date
    ) -> Self:
        """
        新しい貸出を作成する
        args:
            book_copy_id (BookCopyId): 蔵書ID
            member_id (MemberId): 利用者ID
            loan_date (date): 貸出日
        returns:
            Loan: 新しい貸出オブジェクト
        """
        return cls(
            loan_id=LoanId.generate(),
            book_copy_id=book_copy_id,
            member_id=member_id,
            loan_date=loan_date,
        )

    def mark_as_returned(self, returned_date: date):
        """
        貸出を返却済みにする
        """
        # ========== 返却可能か確認する ==========
        if self.is_returned:
            raise ValueError("This loan is already returned")

        if returned_date < self._loan_date:
            raise ValueError("The return date must be after the loan date")

        # ========== 貸出を返却済みにする ========
        self._returned_date = returned_date
