from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, taxonomy, question  # Import your auth routes


app = FastAPI(title="Misconception Detector API")

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Angular URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include your authentication endpoints
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# Register the split routers to activate the API mapping network
app.include_router(taxonomy.router, prefix="/api/v1")
app.include_router(question.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Misconception Detection API"}