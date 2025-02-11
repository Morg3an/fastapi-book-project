from typing import OrderedDict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    """Retrieve all books."""
    return list(db.books.values())

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
    """Retrieve a book by its ID."""
    book = db.books.get(book_id)
    if not book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    return book


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    """Update book details"""
    updated_book = db.update_book(book_id, book)
    if not updated_book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete a book by ID"""
    if book_id not in db.books:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    db.delete_book(book_id)
    return