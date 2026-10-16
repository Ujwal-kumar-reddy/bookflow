from datetime import date, timedelta
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select, or_
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .db import get_db
from .models import Book
from .schemas import (
    BookCheckout,
    BookCreate,
    BookOut,
    BookStatsOut,
    BookUpdate,
)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Student Library Book-Lending Tracker API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "description": "Student Library Book-Lending Tracker API",
    }

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(select(func.count(Book.id)))
        return {"status": "READY"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database not ready: {str(e)}",
        )

@app.get("/api/books", response_model=list[BookOut])
def list_books(
    status_filter: str | None = Query(default=None, alias="status"),
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = select(Book)
    if status_filter:
        query = query.where(Book.status == status_filter.upper())
    if category:
        query = query.where(Book.category == category)
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
                Book.borrower_name.ilike(search_term),
            )
        )
    return list(db.scalars(query.order_by(Book.id.desc())))

@app.get("/api/books/stats", response_model=BookStatsOut)
def book_stats(db: Session = Depends(get_db)):
    today = date.today()
    all_books = list(db.scalars(select(Book)))
    total = len(all_books)
    available = sum(1 for b in all_books if b.status == "AVAILABLE")
    borrowed = sum(1 for b in all_books if b.status == "BORROWED")
    overdue = sum(
        1 for b in all_books if b.status == "BORROWED" and b.due_date and b.due_date < today
    )
    return BookStatsOut(
        total=total,
        available=available,
        borrowed=borrowed,
        overdue=overdue,
    )

@app.get("/api/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book

@app.post("/api/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = Book(
        title=payload.title.strip(),
        author=payload.author.strip(),
        category=payload.category.strip(),
        status="AVAILABLE",
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.put("/api/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    if payload.title is not None:
        book.title = payload.title.strip()
    if payload.author is not None:
        book.author = payload.author.strip()
    if payload.category is not None:
        book.category = payload.category.strip()
    db.commit()
    db.refresh(book)
    return book

@app.delete("/api/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    db.delete(book)
    db.commit()
    return {"message": f"Book '{book.title}' successfully deleted", "id": book_id}

@app.post("/api/books/{book_id}/checkout", response_model=BookOut)
def checkout_book(book_id: int, payload: BookCheckout, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    if book.status == "BORROWED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book is already checked out to '{book.borrower_name}'",
        )
    book.status = "BORROWED"
    book.borrower_name = payload.borrower_name.strip()
    book.due_date = date.today() + timedelta(days=payload.loan_days)
    db.commit()
    db.refresh(book)
    return book

@app.post("/api/books/{book_id}/return", response_model=BookOut)
def return_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    if book.status == "AVAILABLE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is already available in the library and not currently borrowed",
        )
    book.status = "AVAILABLE"
    book.borrower_name = None
    book.due_date = None
    db.commit()
    db.refresh(book)
    return book
