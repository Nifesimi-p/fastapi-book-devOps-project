from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre

# ✅ Create an in-memory database class
class InMemoryDB:
    def __init__(self):
        self.books = {
            1: Book(id=1, title="The Hobbit", author="J.R.R. Tolkien", publication_year=1937, genre=Genre.FANTASY),
            2: Book(id=2, title="The Lord of the Rings", author="J.R.R. Tolkien", publication_year=1954, genre=Genre.FANTASY),
            3: Book(id=3, title="The Return of the King", author="J.R.R. Tolkien", publication_year=1955, genre=Genre.FANTASY),
        }

# ✅ Initialize the database only once
db = InMemoryDB()

# ✅ Define API router
router = APIRouter()

@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_books():
    """Retrieve all books in the database."""
    return list(db.books.values())  # ✅ Convert dict values to list

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    """
    Retrieve a book by its ID.
    - If the book exists, return its details.
    - If the book does not exist, return a 404 error.
    """
    book = db.books.get(book_id)  # ✅ Use `.get()` to prevent KeyError
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    return book  # ✅ Return book details

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    """
    Add a new book to the database.
    - Ensures unique book ID
    - Returns 400 if the ID already exists
    """
    if book.id in db.books:
        raise HTTPException(status_code=400, detail="Book ID already exists")

    db.books[book.id] = book  # ✅ Add book
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=book.model_dump())

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book):
    """Update an existing book's details."""
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    db.books[book_id] = book  # ✅ Update book
    return book  # ✅ Return updated book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Delete a book from the database."""
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    del db.books[book_id]  # ✅ Delete book
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
