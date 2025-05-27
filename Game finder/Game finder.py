import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("game_finder_api")

app = FastAPI(title="Game Finder API", version="1.0")

GAME_DB = [
    {"title": "The Legend of Zelda: Breath of the Wild", "platform": "Nintendo", "genre": "adventure"},
    {"title": "God of War", "platform": "PlayStation", "genre": "action"},
    {"title": "Minecraft", "platform": "All", "genre": "sandbox"},
    {"title": "Hades", "platform": "PC", "genre": "roguelike"},
    {"title": "Elden Ring", "platform": "PC", "genre": "RPG"},
    {"title": "Stardew Valley", "platform": "All", "genre": "simulation"},
    {"title": "Fortnite", "platform": "All", "genre": "battle royale"},
    {"title": "Celeste", "platform": "PC", "genre": "platformer"},
]

class Game(BaseModel):
    title: str
    platform: str
    genre: str

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Game Finder API is online."}

@app.get("/suggest-games", response_model=List[Game], summary="Suggest video games to play")
def suggest_games(
    platform: Optional[str] = Query(None, description="Platform (e.g., PC, Nintendo)"),
    genre: Optional[str] = Query(None, description="Genre (e.g., RPG, adventure)"),
    limit: int = Query(5, ge=1, le=20, description="Number of games to recommend")
):
    logger.info(f"Suggesting games for platform={platform}, genre={genre}, limit={limit}")

    results = GAME_DB
    if platform:
        results = [game for game in results if platform.lower() in game["platform"].lower()]
    if genre:
        results = [game for game in results if genre.lower() in game["genre"].lower()]

    if not results:
        logger.warning("No matching games found.")
        raise HTTPException(status_code=404, detail="No games found for given filters.")

    random.shuffle(results)
    return results[:limit]

if __name__ == "__main__":
    uvicorn.run("game_finder_api:app", host="0.0.0.0", port=8001, workers=4, log_level="info")
