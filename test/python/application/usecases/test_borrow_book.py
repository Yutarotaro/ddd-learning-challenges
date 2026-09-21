from datetime import date

from application.usecases.borrow_book import BorrowBookUseCase
from domain.book import ISBN
from domain.book_copy import BookCopy, LendingStatus
from domain.member import Member, MemberName
from domain.value_objects import BookCopyId, MemberId


def test_borrow_book_adds_loan_lends_copy_saves_aggregates_and_commits():
    class FakeRepository:
        def __init__(self, entity):
            self.entity = entity
            self.saved = []

        def get(self, entity_id):
            return self.entity

        def save(self, entity):
            self.saved.append(entity)

    class FakeUnitOfWork:
        def __init__(self, member, book_copy):
            self.member_repository = FakeRepository(member)
            self.book_copy_repository = FakeRepository(book_copy)
            self.committed = False

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return None

        def commit(self):
            self.committed = True

    member = Member(MemberId.generate(), MemberName("Alice"))
    book_copy = BookCopy(BookCopyId.generate(), ISBN("978-4-123456-78-9"))
    unit_of_work = FakeUnitOfWork(member, book_copy)
    use_case = BorrowBookUseCase(unit_of_work)

    loan_id = use_case.execute(member.id, book_copy.id, date(2026, 9, 21))

    assert loan_id in member.loans
    assert book_copy.status == LendingStatus.LENT_OUT
    assert unit_of_work.member_repository.saved == [member]
    assert unit_of_work.book_copy_repository.saved == [book_copy]
    assert unit_of_work.committed
