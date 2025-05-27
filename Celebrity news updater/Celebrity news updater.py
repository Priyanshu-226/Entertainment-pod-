from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import random
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("celebrity_news_api")

app = FastAPI(title="Celebrity News Updater API", version="1.0")

# Simulated celebrity news database
CELEBRITY_NEWS_DB = {
    "Taylor Swift": [
        "Taylor Swift announces new album release date.",
        "Taylor Swift's tour tickets sold out in 10 minutes.",
    ],
    "Tom Holland": [
        "Tom Holland signs on for new Spider-Man movie.",
        "Tom Holland and Zendaya spotted at award show.",
    ],
    "Zendaya": [
        "Zendaya wins Best Actress at the Emmys.",
        "Zendaya debuts new fashion line at Paris Fashion Week.",
    ],
    "Dwayne Johnson": [
        "Dwayne Johnson teases new action movie on Instagram.",
        "The Rock surprises fans at movie premiere.",
    ],
    "Billie Eilish": [
        "Billie Eilish drops new single overnight.",
        "Billie Eilish speaks about climate change activism.",
    ]
}

@app.get("/celebrity-news", summary="Get latest news about a celebrity")
def get_celebrity_news(
    name: Optional[str] = Query(None, description="Celebrity name to get news for")
) -> List[str]:
    """
    Returns recent news headlines about a given celebrity.
    If no name is provided, news from random celebrities will be returned.
    """
    logger.info(f"Fetching news for celebrity: {name or 'random selection'}")
    
    try:
        if name:
            name = name.strip().title()
            if name not in CELEBRITY_NEWS_DB:
                raise HTTPException(status_code=404, detail="Celebrity not found.")
            return CELEBRITY_NEWS_DB[name]
        else:
            # Randomly return 1 headline from 3 different celebrities
            random_celebrities = random.sample(list(CELEBRITY_NEWS_DB.items()), k=3)
            mixed_news = [random.choice(news_list) for _, news_list in random_celebrities]
            return mixed_news

    except Exception as e:
        logger.exception("Failed to fetch celebrity news")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    # Run with multiple workers for concurrency
    uvicorn.run("celebrity_news_api:app", host="0.0.0.0", port=8002, log_level="info", workers=4)
