# backend/app/main.py
from dotenv import load_dotenv
import os

# تحميل ملف البيئة المحلي
load_dotenv('.env.local')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import init_db
import logging

# إعداد logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telegram WebApp Backend (Prod)")

# طباعة DATABASE_URL للتحقق
logger.info(f"🔧 DATABASE_URL: {os.getenv('DATABASE_URL')}")

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
    try:
        init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

# ⭐ تضمين جميع routers مع معالجة الأخطاء ⭐

# 1. الرواتر الأساسية
try:
    from .api import auth, telegram, admin
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(telegram.router, prefix="/api/telegram", tags=["telegram"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    logger.info("✅ الأساسية routers loaded")
except ImportError as e:
    logger.warning(f"⚠️ Basic routers not available: {e}")

# 2. الرواتر المساعدة
try:
    from .api import auth_simple
    app.include_router(auth_simple.router, prefix="/api/auth", tags=["auth"])
    logger.info("✅ auth_simple router loaded")
except ImportError as e:
    logger.warning(f"⚠️ auth_simple not available: {e}")

try:
    from .api import admin_simple
    app.include_router(admin_simple.router, prefix="/api/admin", tags=["admin"])
    logger.info("✅ admin_simple router loaded")
except ImportError as e:
    logger.warning(f"⚠️ admin_simple not available: {e}")

try:
    from .api import simple_test
    app.include_router(simple_test.router, prefix="/api/test", tags=["test"])
    logger.info("✅ simple_test router loaded")
except ImportError as e:
    logger.warning(f"⚠️ simple_test not available: {e}")

try:
    from .api import dev
    app.include_router(dev.router, prefix="/api/dev", tags=["dev"])
    logger.info("✅ dev router loaded")
except ImportError as e:
    logger.warning(f"⚠️ dev not available: {e}")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Telegram WebApp Backend is running!", "docs": "/docs"}