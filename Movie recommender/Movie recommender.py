import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import random
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("movie_recommender_api")

app = FastAPI(title="Movie Recommender API", version="1.0")

# Sample movie database
MOVIE_DB = [
    {"title": "Inception", "genre": "sci-fi", "language": "english", "year": 2010},
    {"title": "Interstellar", "genre": "sci-fi", "language": "english", "year": 2014},
    {"title": "Parasite", "genre": "thriller", "language": "korean", "year": 2019},
    {"title": "Dangal", "genre": "drama", "language": "hindi", "year": 2016},
    {"title": "Your Name", "genre": "romance", "language": "japanese", "year": 2016},
    {"title": "The Dark Knight", "genre": "action", "language": "english", "year": 2008},
    {"title": "Spirited Away", "genre": "fantasy", "language": "japanese", "year": 2001},
    {"title": "3 Idiots", "genre": "comedy", "language": "hindi", "year": 2009},
    # Add more entries as needed
]

# Response model
class Movie(BaseModel):
    title: str
    genre: str
    language: str
    year: int


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Movie Recommender API is running."}


@app.get("/recommend", response_model=List[Movie], summary="Get movie recommendations")
async def recommend_movies(
    genre: Optional[str] = Query(None, description="Preferred genre"),
    language: Optional[str] = Query(None, description="Preferred language"),
    year: Optional[int] = Query(None, ge=1900, le=2050, description="Preferred release year"),
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations to return")
):
    """
    Recommend movies based on genre, language, and year.
    If no filter is provided, random movies are returned.
    """
    logger.info(f"Received recommendation request with genre={genre}, language={language}, year={year}, limit={limit}")

    # Filter the movie DB based on query
    filtered = MOVIE_DB

    if genre:
        filtered = [m for m in filtered if m["genre"].lower() == genre.lower()]
    if language:
        filtered = [m for m in filtered if m["language"].lower() == language.lower()]
    if year:
        filtered = [m for m in filtered if m["year"] == year]

    if not filtered:
        logger.warning("No matching movies found")
        raise HTTPException(status_code=404, detail="No matching movies found.")

    # Shuffle and return up to `limit` results
    random.shuffle(filtered)
    logger.info(f"Returning {min(limit, len(filtered))} recommendations")
    return filtered[:limit]


if __name__ == "__main__":
    # Run with: uvicorn movie_recommender_api:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run("movie_recommender_api:app", host="0.0.0.0", port=8000, log_level="info", workers=4)
