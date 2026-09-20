import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# Vercel's filesystem is read-only except for /tmp.
if not IS_VERCEL:
    os.makedirs(INSTANCE_DIR, exist_ok=True)

db_url = os.getenv("DATABASE_URL", "").strip()
if db_url.startswith("postgres://"):
    db_url = "postgresql+psycopg://" + db_url[len("postgres://"):]
elif db_url.startswith("postgresql://"):
    db_url = "postgresql+psycopg://" + db_url[len("postgresql://"):]

if db_url:
    database_uri = db_url
elif IS_VERCEL:
    # Temporary fallback so a preview can boot even before PostgreSQL is added.
    # This is NOT persistent storage and should not be used for production data.
    database_uri = "sqlite:////tmp/gyanpath-vercel.db"
else:
    database_uri = "sqlite:///" + os.path.join(INSTANCE_DIR, "gyanpath.db")

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

    # Default to true so a fresh Vercel PostgreSQL database can boot without
    # an extra migration command. Set AUTO_INIT_DB=false after the schema is
    # established if you want migrations to be the only schema manager.
    AUTO_INIT_DB = os.getenv("AUTO_INIT_DB", "true").lower() == "true"
    IS_VERCEL = IS_VERCEL
