from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import db_manager

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await db_manager.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db_manager.close()

# Configure CORS to allow requests from your React frontend
# In development, Vite usually runs on localhost:5173
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Mental Health AI Backend is running!"}