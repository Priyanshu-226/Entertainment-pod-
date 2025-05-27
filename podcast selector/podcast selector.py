import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("podcast_selector_api")

app = FastAPI(title="Podcast Selector API", version="1.0")

# Sample podcast dataset
PODCAST_DB = [
    {"title": "Science Vs", "genre": "science"},
    {"title": "The Daily", "genre": "news"},
    {"title": "Hardcore History", "genre": "history"},
    {"title": "99% Invisible", "genre": "design"},
    {"title": "Darknet Diaries", "genre": "cybersecurity"},
    {"title": "My Favorite Murder", "genre": "true crime"},
]

# Response model
class Podcast(BaseModel):
    title: str
    genre: str

@app.get("/suggest-podcasts", response_model=List[Podcast], summary="Suggest podcasts based on genre")
def suggest_podcasts(
    genre: Optional[str] = Query(None, description="Podcast genre like science, news, history, etc."),
    limit: int = Query(5, ge=1, le=20, description="Number of podcast suggestions (1-20)")
):
    """
    Suggest a list of podcasts based on genre (optional) and limit.
    """
    logger.info(f"Received request: genre={genre}, limit={limit}")
    try:
        results = PODCAST_DB
        if genre:
            results = [podcast for podcast in results if genre.lower() in podcast["genre"].lower()]

        if not results:
            raise HTTPException(status_code=404, detail="No podcasts found for the given genre.")

        random.shuffle(results)
        return results[:limit]

    except Exception as e:
        logger.exception("Failed to suggest podcasts")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    # Run with multiple workers for handling concurrency
    uvicorn.run("podcast_selector_api:app", host="0.0.0.0", port=8000, log_level="info", workers=4)
