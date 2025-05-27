import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("book_suggestor_api")

app = FastAPI(title="Book Suggestor API", version="1.0")

# Mocked book data
BOOK_DB = [
    {"title": "1984", "author": "George Orwell", "genre": "dystopian", "decade": 1940},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "romance", "decade": 1810},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy", "decade": 1930},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "drama", "decade": 1960},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "thriller", "decade": 2000},
    {"title": "Atomic Habits", "author": "James Clear", "genre": "self-help", "decade": 2010},
    {"title": "Dune", "author": "Frank Herbert", "genre": "science fiction", "decade": 1960},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "philosophical", "decade": 1980},
    # Add more as needed
]

class Book(BaseModel):
    title: str
    author: str
    genre: str
    decade: int

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Book Suggestor API is online."}


@app.get("/suggest-books", response_model=List[Book], summary="Suggest books based on filters")
def suggest_books(
    genre: Optional[str] = Query(None, description="Book genre (e.g., fantasy, drama)"),
    author: Optional[str] = Query(None, description="Author name"),
    decade: Optional[int] = Query(None, ge=1800, le=2020, description="Decade of publication"),
    limit: int = Query(5, ge=1, le=20, description="Number of books to recommend")
):
    logger.info(f"Suggesting books for genre={genre}, author={author}, decade={decade}, limit={limit}")

    results = BOOK_DB
    if genre:
        results = [book for book in results if book["genre"].lower() == genre.lower()]
    if author:
        results = [book for book in results if author.lower() in book["author"].lower()]
    if decade:
        results = [book for book in results if book["decade"] == decade]

    if not results:
        logger.warning("No matching books found.")
        raise HTTPException(status_code=404, detail="No books found for given filters.")

    random.shuffle(results)
    return results[:limit]


if __name__ == "__main__":
    uvicorn.run("book_suggestor_api:app", host="0.0.0.0", port=8000, workers=4, log_level="info")
