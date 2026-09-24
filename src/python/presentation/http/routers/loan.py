from fastapi import APIRouter, Depends

from presentation.http.models.loan import BorrowBookRequest, BorrowBookResponse
from application.usecases.borrow_book import BorrowBookUseCase
from domain.value_objects import BookCopyId, MemberId

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
)


def get_borrow_book_use_case() -> BorrowBookUseCase:
    raise NotImplementedError


@router.post("")
def borrow_book(
    request: BorrowBookRequest,
    usecase: BorrowBookUseCase = Depends(get_borrow_book_use_case),
) -> BorrowBookResponse:
    loan_id = usecase.execute(
        member_id=MemberId(request.member_id),
        book_copy_id=BookCopyId(request.book_copy_id),
        loan_date=request.loan_date,
    )

    return BorrowBookResponse(loan_id=loan_id.value)
