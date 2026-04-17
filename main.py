from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Score(BaseModel):
    player: str = "Anonymous"
    score: int

# In-memory storage for high scores
# A real application would use a database
high_scores: List[Dict] = []

@app.post("/scores", response_model=Score)
async def submit_score(score: Score):
    """
    Submits a new player score.
    The list is sorted and trimmed to keep only the top N scores.
    """
    # Sanitize player name
    score.player = score.player.strip()
    if not score.player:
        score.player = "Anonymous"
    
    high_scores.append({"player": score.player, "score": score.score})
    
    # Sort scores in descending order
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Keep only the top 10 scores
    global high_scores
    high_scores = high_scores[:10] 
    
    return score

@app.get("/scores", response_model=List[Score])
async def get_high_scores():
    """
    Retrieves the list of stored high scores.
    """
    return high_scores

@app.get("/")
async def read_root():
    """
    Root endpoint for basic API status check.
    """
    return {"message": "Welcome to the Snake Game API! Navigate to /scores for high scores."}