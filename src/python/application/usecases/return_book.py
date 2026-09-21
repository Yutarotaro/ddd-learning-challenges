from domain.value_objects import MemberId, BookCopyId, LoanId
from application.ports.unit_of_work import UnitOfWork

from datetime import date


class ReturnBookUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ):
        self.unit_of_work = unit_of_work

    def execute(
        self,
        member_id: MemberId,
        loan_id: LoanId,
        return_date: date,
    ) -> None:
        with self.unit_of_work as uow:
            member = uow.member_repository.get(member_id)
            loan = member.get_loan(loan_id)
            book_copy = uow.book_copy_repository.get(loan.book_copy_id)

            member.return_book(loan_id, return_date)
            book_copy.mark_as_returned()

            uow.member_repository.save(member)
            uow.book_copy_repository.save(book_copy)

            uow.commit()

            return
