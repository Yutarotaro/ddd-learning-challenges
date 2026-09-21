from domain.value_objects import MemberId, BookCopyId, LoanId
from application.ports.unit_of_work import UnitOfWork

from datetime import date


class BorrowBookUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ):
        self.unit_of_work = unit_of_work

    def execute(
        self, member_id: MemberId, book_copy_id: BookCopyId, loan_date: date
    ) -> LoanId:
        with self.unit_of_work as uow:
            member = uow.member_repository.get(member_id)
            book_copy = uow.book_copy_repository.get(book_copy_id)

            loan = member.borrow_book(book_copy_id, loan_date)
            book_copy.lend_out()

            uow.member_repository.save(member)
            uow.book_copy_repository.save(book_copy)

            uow.commit()

            return loan.id
