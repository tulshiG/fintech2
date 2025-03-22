from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, credit  # ✅ Ensure `credit.py` is imported properly

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register API routes
app.include_router(auth.router)  
app.include_router(credit.router)  # ✅ Ensure `credit.py` is included

@app.get("/")
def home():
    return {"message": "API is running"}
