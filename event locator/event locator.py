import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("event_locator_api")

app = FastAPI(title="Event Locator API", version="1.0")

EVENT_DB = [
    {"name": "Coldplay Concert", "location": "Delhi", "category": "concert"},
    {"name": "Startup Expo", "location": "Bangalore", "category": "business"},
    {"name": "Comic Con", "location": "Mumbai", "category": "entertainment"},
    {"name": "Food Fest", "location": "Chennai", "category": "food"},
    {"name": "AI Summit", "location": "Hyderabad", "category": "tech"},
]

class Event(BaseModel):
    name: str
    location: str
    category: str

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Event Locator API is online."}

@app.get("/find-events", response_model=List[Event], summary="Find local events")
def find_events(
    location: Optional[str] = Query(None, description="City or location"),
    category: Optional[str] = Query(None, description="Event category (e.g., concert, tech)"),
    limit: int = Query(5, ge=1, le=20)
):
    logger.info(f"Finding events for location={location}, category={category}, limit={limit}")

    results = EVENT_DB
    if location:
        results = [event for event in results if location.lower() in event["location"].lower()]
    if category:
        results = [event for event in results if category.lower() in event["category"].lower()]

    if not results:
        logger.warning("No events found.")
        raise HTTPException(status_code=404, detail="No events found for given filters.")

    random.shuffle(results)
    return results[:limit]

if __name__ == "__main__":
    uvicorn.run("event_locator_api:app", host="0.0.0.0", port=8002, workers=4, log_level="info")
