from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client, Client
from datetime import datetime, timezone
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Books API", description="A RESTful API for managing a book collection, backed by Supabase.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("Missing SUPABASE_URL")
if not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# --- Pydantic Models ---

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300, examples=["The Great Gatsby"])
    author: str = Field(..., min_length=1, max_length=200, examples=["F. Scott Fitzgerald"])
    genre: Optional[str] = Field(None, max_length=100, examples=["Fiction"])
    published_year: Optional[int] = Field(None, ge=0, le=2100, examples=[1925])
    isbn: Optional[str] = Field(None, max_length=20, examples=["978-0743273565"])


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[str] = Field(None, max_length=100)
    published_year: Optional[int] = Field(None, ge=0, le=2100)
    isbn: Optional[str] = Field(None, max_length=20)


# --- Endpoints ---

@app.get("/")
async def root():
    response = supabase.table("book").select("*", count="exact").execute()
    return {
        "message": "Books API is running",
        "book_count": response.count
    }


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/books")
async def list_books():
    """Retrieve all books, ordered by ID."""
    response = supabase.table("book").select("*").order("id").execute()
    return response.data


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    """Retrieve a single book by its ID."""
    response = supabase.table("book").select("*").eq("id", book_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")
    return response.data[0]


@app.post("/books", status_code=201)
async def create_book(book: BookCreate):
    """Create a new book record."""
    payload = {
        "title": book.title.strip(),
        "author": book.author.strip(),
        "genre": book.genre.strip() if book.genre else None,
        "published_year": book.published_year,
        "isbn": book.isbn.strip() if book.isbn else None,
        "updated_at": utc_now_iso(),
    }
    response = supabase.table("book").insert(payload).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create book")
    return response.data[0]


@app.put("/books/{book_id}")
async def replace_book(book_id: int, book: BookCreate):
    """Full replacement of a book record (PUT)."""
    payload = {
        "title": book.title.strip(),
        "author": book.author.strip(),
        "genre": book.genre.strip() if book.genre else None,
        "published_year": book.published_year,
        "isbn": book.isbn.strip() if book.isbn else None,
        "updated_at": utc_now_iso(),
    }
    response = supabase.table("book").update(payload).eq("id", book_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")
    return response.data[0]


@app.patch("/books/{book_id}")
async def update_book(book_id: int, book: BookUpdate):
    """Partial update of a book record (PATCH)."""
    update_data = book.model_dump(exclude_none=True)

    for field in ("title", "author", "genre", "isbn"):
        if field in update_data and isinstance(update_data[field], str):
            update_data[field] = update_data[field].strip()

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    update_data["updated_at"] = utc_now_iso()

    response = supabase.table("book").update(update_data).eq("id", book_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")
    return response.data[0]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Delete a book by its ID."""
    response = supabase.table("book").delete().eq("id", book_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
