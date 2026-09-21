from fastapi import APIRouter, Depends


from presentation.http.models.loan import BorrowBookRequest, BorrowBookResponse
from application.usecases.borrow_book import BorrowBookUseCase
from domain.member import MemberId
from domain.book_copy import BookCopyId

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
)


@router.post("")
def borrow_book(
    request: BorrowBookRequest, usecase: BorrowBookUseCase = Depends(...)
) -> BorrowBookResponse:
    loan_id = usecase.execute(
        member_id=MemberId(request.member_id),
        book_copy_id=BookCopyId(request.book_copy_id),
        loan_date=request.loan_date,
    )

    return BorrowBookResponse(loan_id=loan_id.value)
