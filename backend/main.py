from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cortex API",
    description="Backend for Cortex Personalized Learning Intelligence System",
    version="0.1.0",
)

# Configure CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cortex API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
