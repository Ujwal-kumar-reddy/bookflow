from datetime import date, datetime
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the book")
    author: str = Field(..., min_length=1, max_length=255, description="Author of the book")
    category: str = Field(..., min_length=1, max_length=100, description="Category / Genre")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)

class BookCheckout(BaseModel):
    borrower_name: str = Field(..., min_length=1, max_length=255, description="Name of student borrowing the book")
    loan_days: int = Field(default=14, ge=1, le=90, description="Loan duration in days (1-90)")

class BookOut(BookBase):
    id: int
    status: str
    borrower_name: str | None = None
    due_date: date | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class BookStatsOut(BaseModel):
    total: int = 0
    available: int = 0
    borrowed: int = 0
    overdue: int = 0
