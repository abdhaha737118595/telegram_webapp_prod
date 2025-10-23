import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, telegram, admin
from .db.database import init_db

app = FastAPI(title="Telegram WebApp Backend (Prod)")

origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize DB (create tables if not exist)
@app.on_event('startup')
def startup():
    init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(telegram.router, prefix="/api/telegram", tags=["telegram"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
