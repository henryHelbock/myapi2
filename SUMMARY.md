# Books API — Summary Documentation

## Overview

A RESTful API built with **FastAPI** and **Supabase** (PostgreSQL) for managing a book collection. The API supports full CRUD operations via the standard HTTP methods.

**Live Server:** `https://<your-render-url>.onrender.com`  
**Swagger UI:** `https://<your-render-url>.onrender.com/docs`  
**ReDoc:** `https://<your-render-url>.onrender.com/redoc`

---

## Database Schema

| Column         | Type                     | Description              |
|----------------|--------------------------|--------------------------|
| id             | bigint (auto-increment)  | Primary key              |
| title          | text (not null)          | Book title               |
| author         | text (not null)          | Author name              |
| genre          | text                     | Genre (optional)         |
| published_year | integer                  | Year published (optional)|
| isbn           | text                     | ISBN (optional)          |
| inserted_at    | timestamptz              | Created timestamp (UTC)  |
| updated_at     | timestamptz              | Last updated (UTC)       |

---

## HTTP Methods

### 1. GET /books — List All Books

Retrieves all book records ordered by ID.

**Swagger UI:** Navigate to `/docs`, expand `GET /books`, click "Try it out", then "Execute".

**curl:**
```bash
curl -X GET https://<your-render-url>.onrender.com/books
```

**Postman:**
- Method: `GET`
- URL: `https://<your-render-url>.onrender.com/books`
- Click "Send"

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "genre": "Fiction",
    "published_year": 1925,
    "isbn": "978-0743273565",
    "inserted_at": "2026-04-07T...",
    "updated_at": "2026-04-07T..."
  }
]
```

---

### 2. GET /books/{book_id} — Get a Single Book

Retrieves one book by its ID.

**Swagger UI:** Expand `GET /books/{book_id}`, enter the ID, click "Execute".

**curl:**
```bash
curl -X GET https://<your-render-url>.onrender.com/books/1
```

**Postman:**
- Method: `GET`
- URL: `https://<your-render-url>.onrender.com/books/1`

**Response (200):**
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "genre": "Fiction",
  "published_year": 1925,
  "isbn": "978-0743273565",
  "inserted_at": "2026-04-07T...",
  "updated_at": "2026-04-07T..."
}
```

---

### 3. POST /books — Create a New Book

Creates a new book record. Requires `title` and `author`; other fields are optional.

**Swagger UI:** Expand `POST /books`, click "Try it out", fill in the JSON body, click "Execute".

**curl:**
```bash
curl -X POST https://<your-render-url>.onrender.com/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Brave New World",
    "author": "Aldous Huxley",
    "genre": "Dystopian",
    "published_year": 1932,
    "isbn": "978-0060850524"
  }'
```

**Postman:**
- Method: `POST`
- URL: `https://<your-render-url>.onrender.com/books`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "title": "Brave New World",
  "author": "Aldous Huxley",
  "genre": "Dystopian",
  "published_year": 1932,
  "isbn": "978-0060850524"
}
```

**Response (201):**
```json
{
  "id": 6,
  "title": "Brave New World",
  "author": "Aldous Huxley",
  "genre": "Dystopian",
  "published_year": 1932,
  "isbn": "978-0060850524",
  "inserted_at": "2026-04-07T...",
  "updated_at": "2026-04-07T..."
}
```

---

### 4. PUT /books/{book_id} — Replace a Book (Full Update)

Replaces all fields of a book. All required fields (`title`, `author`) must be provided.

**Swagger UI:** Expand `PUT /books/{book_id}`, enter the ID and full JSON body, click "Execute".

**curl:**
```bash
curl -X PUT https://<your-render-url>.onrender.com/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby (Revised)",
    "author": "F. Scott Fitzgerald",
    "genre": "Classic Fiction",
    "published_year": 1925,
    "isbn": "978-0743273565"
  }'
```

**Postman:**
- Method: `PUT`
- URL: `https://<your-render-url>.onrender.com/books/1`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "title": "The Great Gatsby (Revised)",
  "author": "F. Scott Fitzgerald",
  "genre": "Classic Fiction",
  "published_year": 1925,
  "isbn": "978-0743273565"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "The Great Gatsby (Revised)",
  "author": "F. Scott Fitzgerald",
  "genre": "Classic Fiction",
  "published_year": 1925,
  "isbn": "978-0743273565",
  "inserted_at": "2026-04-07T...",
  "updated_at": "2026-04-07T..."
}
```

---

### 5. PATCH /books/{book_id} — Partial Update

Updates only the provided fields. At least one field must be supplied.

**Swagger UI:** Expand `PATCH /books/{book_id}`, enter the ID and partial JSON body, click "Execute".

**curl:**
```bash
curl -X PATCH https://<your-render-url>.onrender.com/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "American Classic"
  }'
```

**Postman:**
- Method: `PATCH`
- URL: `https://<your-render-url>.onrender.com/books/1`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "genre": "American Classic"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "The Great Gatsby (Revised)",
  "author": "F. Scott Fitzgerald",
  "genre": "American Classic",
  "published_year": 1925,
  "isbn": "978-0743273565",
  "inserted_at": "2026-04-07T...",
  "updated_at": "2026-04-07T..."
}
```

---

### 6. DELETE /books/{book_id} — Delete a Book

Deletes a book by its ID.

**Swagger UI:** Expand `DELETE /books/{book_id}`, enter the ID, click "Execute".

**curl:**
```bash
curl -X DELETE https://<your-render-url>.onrender.com/books/1
```

**Postman:**
- Method: `DELETE`
- URL: `https://<your-render-url>.onrender.com/books/1`

**Response (200):**
```json
{
  "message": "Book deleted successfully"
}
```

---

## Technology Stack

| Component  | Technology       |
|------------|------------------|
| Framework  | FastAPI (Python) |
| Database   | Supabase (PostgreSQL) |
| Hosting    | Render           |
| Docs       | Swagger UI (auto-generated by FastAPI) |
