import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# Vercel Functions have a read-only filesystem except for /tmp.
if not IS_VERCEL:
    os.makedirs(INSTANCE_DIR, exist_ok=True)

db_url = os.getenv("DATABASE_URL", "").strip()
if db_url.startswith("postgres://"):
    db_url = "postgresql+psycopg://" + db_url[len("postgres://"):]
elif db_url.startswith("postgresql://"):
    db_url = "postgresql+psycopg://" + db_url[len("postgresql://"):]

# Production Vercel should use DATABASE_URL with hosted PostgreSQL.
# /tmp is only a resilience fallback for an unconfigured preview.
if db_url:
    database_uri = db_url
elif IS_VERCEL:
    database_uri = "sqlite:////tmp/gyanpath-vercel.db"
else:
    database_uri = "sqlite:///" + os.path.join(INSTANCE_DIR, "gyanpath.db")

default_auto_init = "true" if (not IS_VERCEL or not db_url) else "false"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv(
        "SESSION_COOKIE_SECURE",
        "true" if IS_VERCEL else "false",
    ).lower() == "true"
    AUTO_INIT_DB = os.getenv("AUTO_INIT_DB", default_auto_init).lower() == "true"
    IS_VERCEL = IS_VERCEL
