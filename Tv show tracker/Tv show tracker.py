from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import logging

# Logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tv_show_tracker_api")

app = FastAPI(title="TV Show Tracker API", version="1.0")

# In-memory simulated DB for simplicity
USER_SHOWS_DB: Dict[str, Dict[str, int]] = {}
TV_SHOWS = {
    "Stranger Things": 8,
    "The Office": 24,
    "Breaking Bad": 13,
    "Game of Thrones": 10,
    "The Mandalorian": 8
}

class TrackRequest(BaseModel):
    username: str
    show_name: str
    episode_watched: int

class WatchedResponse(BaseModel):
    message: str

class NextEpisodeResponse(BaseModel):
    next_episode: Optional[int]
    total_episodes: int
    show_name: str

@app.post("/track-episode", response_model=WatchedResponse, summary="Track a watched episode")
def track_episode(data: TrackRequest):
    logger.info(f"Tracking episode for {data.username}: {data.show_name} ep {data.episode_watched}")

    if data.show_name not in TV_SHOWS:
        raise HTTPException(status_code=404, detail="TV show not found.")

    total_eps = TV_SHOWS[data.show_name]
    if data.episode_watched < 1 or data.episode_watched > total_eps:
        raise HTTPException(status_code=400, detail=f"Invalid episode. Must be between 1 and {total_eps}.")

    user_shows = USER_SHOWS_DB.setdefault(data.username, {})
    user_shows[data.show_name] = max(user_shows.get(data.show_name, 0), data.episode_watched)

    return WatchedResponse(message="Episode tracked successfully.")

@app.get("/next-episode", response_model=NextEpisodeResponse, summary="Get next episode to watch")
def next_episode(
    username: str = Query(..., description="Username"),
    show_name: str = Query(..., description="TV show name")
):
    logger.info(f"Fetching next episode for {username} - {show_name}")

    if show_name not in TV_SHOWS:
        raise HTTPException(status_code=404, detail="TV show not found.")

    total_eps = TV_SHOWS[show_name]
    watched = USER_SHOWS_DB.get(username, {}).get(show_name, 0)

    if watched >= total_eps:
        return NextEpisodeResponse(show_name=show_name, total_episodes=total_eps, next_episode=None)

    return NextEpisodeResponse(show_name=show_name, total_episodes=total_eps, next_episode=watched + 1)

if __name__ == "__main__":
    uvicorn.run("tv_show_tracker_api:app", host="0.0.0.0", port=8001, log_level="info", workers=4)
