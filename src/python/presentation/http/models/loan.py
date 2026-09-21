from pydantic import BaseModel
from uuid import UUID
from datetime import date


class BorrowBookRequest(BaseModel):
    member_id: UUID
    book_copy_id: UUID
    loan_date: date


class BorrowBookResponse(BaseModel):
    loan_id: UUID
