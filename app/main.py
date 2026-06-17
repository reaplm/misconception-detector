from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Angular URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)