import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("music_playlist_curator_api")

app = FastAPI(title="Music Playlist Curator API", version="1.0")

# Sample music track database (mocked)
MUSIC_DB = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "mood": "energetic", "decade": 2020},
    {"title": "Someone Like You", "artist": "Adele", "genre": "pop", "mood": "sad", "decade": 2010},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "rock", "mood": "dramatic", "decade": 1970},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "rock", "mood": "angsty", "decade": 1990},
    {"title": "Lose Yourself", "artist": "Eminem", "genre": "hip-hop", "mood": "motivational", "decade": 2000},
    {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "pop", "mood": "romantic", "decade": 2010},
    {"title": "Hallelujah", "artist": "Leonard Cohen", "genre": "folk", "mood": "peaceful", "decade": 1980},
    {"title": "Levitating", "artist": "Dua Lipa", "genre": "pop", "mood": "happy", "decade": 2020},
    {"title": "Imagine", "artist": "John Lennon", "genre": "rock", "mood": "hopeful", "decade": 1970},
    {"title": "Blowin' in the Wind", "artist": "Bob Dylan", "genre": "folk", "mood": "thoughtful", "decade": 1960},
    # Add more tracks as needed
]

# Response model
class Track(BaseModel):
    title: str
    artist: str
    genre: str
    mood: str
    decade: int


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Music Playlist Curator API is running."}


@app.get("/curate-playlist", response_model=List[Track], summary="Generate a music playlist")
async def curate_playlist(
    genre: Optional[str] = Query(None, description="Preferred music genre (e.g., pop, rock, hip-hop)"),
    mood: Optional[str] = Query(None, description="Preferred mood (e.g., happy, sad, energetic)"),
    decade: Optional[int] = Query(None, ge=1950, le=2020, description="Preferred decade (e.g., 1980)"),
    limit: int = Query(5, ge=1, le=20, description="Number of songs to include in the playlist")
):
    """
    Create a personalized music playlist based on genre, mood, and decade.
    Defaults to a random mix if no filter is provided.
    """
    logger.info(f"Received request: genre={genre}, mood={mood}, decade={decade}, limit={limit}")

    filtered_tracks = MUSIC_DB

    if genre:
        filtered_tracks = [track for track in filtered_tracks if track["genre"].lower() == genre.lower()]
    if mood:
        filtered_tracks = [track for track in filtered_tracks if track["mood"].lower() == mood.lower()]
    if decade:
        filtered_tracks = [track for track in filtered_tracks if track["decade"] == decade]

    if not filtered_tracks:
        logger.warning("No matching tracks found.")
        raise HTTPException(status_code=404, detail="No matching tracks found.")

    random.shuffle(filtered_tracks)
    selected = filtered_tracks[:limit]
    logger.info(f"Returning {len(selected)} tracks.")
    return selected


if __name__ == "__main__":
    # Run with: uvicorn music_playlist_curator_api:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run("music_playlist_curator_api:app", host="0.0.0.0", port=8000, log_level="info", workers=4)
