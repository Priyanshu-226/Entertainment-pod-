from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List, Dict
import random
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trivia_provider_api")

app = FastAPI(title="Trivia Provider API", version="1.0")

# Simulated trivia database
TRIVIA_DB: Dict[str, List[Dict[str, str]]] = {
    "general": [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
    ],
    "science": [
        {"question": "What is the chemical symbol for water?", "answer": "H₂O"},
        {"question": "What gas do plants absorb from the atmosphere?", "answer": "Carbon Dioxide"},
    ],
    "history": [
        {"question": "Who was the first President of the United States?", "answer": "George Washington"},
        {"question": "In which year did World War II end?", "answer": "1945"},
    ],
    "sports": [
        {"question": "How many players are there in a football team?", "answer": "11"},
        {"question": "Which country won the FIFA World Cup in 2018?", "answer": "France"},
    ],
    "tech": [
        {"question": "Who founded Microsoft?", "answer": "Bill Gates"},
        {"question": "What does 'CPU' stand for?", "answer": "Central Processing Unit"},
    ]
}

@app.get("/trivia", summary="Get a random trivia question")
def get_trivia(
    category: Optional[str] = Query("general", description="Category of trivia (e.g., general, science, history, sports, tech)")
) -> Dict[str, str]:
    """
    Returns a random trivia question and answer from a specified category.
    If no category is provided, 'general' is used as default.
    """
    logger.info(f"Fetching trivia for category: {category}")
    category = category.lower()

    if category not in TRIVIA_DB:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found.")

    try:
        trivia_item = random.choice(TRIVIA_DB[category])
        return trivia_item
    except Exception as e:
        logger.exception("Failed to fetch trivia")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("trivia_provider_api:app", host="0.0.0.0", port=8003, log_level="info", workers=4)
