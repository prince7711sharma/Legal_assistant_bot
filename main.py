from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from groq_helper import get_legal_response
from utils import generate_pdf

app = FastAPI()

# Enable CORS for all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to the static directory
STATIC_DIR = "backend/static"

# Ensure the static directory exists
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Define the root path
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Define the data model for incoming requests
class Query(BaseModel):
    question: str

# Define the endpoint to handle legal bot queries# Import your custom modules
@app.post("/ask")
async def ask_legal_bot(query: Query):
    response = get_legal_response(query.question)
    filename = generate_pdf(query.question, response)
    return {"response": response, "pdf": filename}


