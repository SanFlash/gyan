import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR=os.path.join(BASE_DIR,"instance")
os.makedirs(INSTANCE_DIR,exist_ok=True)
db_url=os.getenv("DATABASE_URL","").strip()
if db_url.startswith("postgres://"): db_url="postgresql+psycopg://"+db_url[len("postgres://"):]
elif db_url.startswith("postgresql://"): db_url="postgresql+psycopg://"+db_url[len("postgresql://"):]
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","dev-only-change-me")
    SQLALCHEMY_DATABASE_URI=db_url or "sqlite:///"+os.path.join(INSTANCE_DIR,"gyanpath.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    WTF_CSRF_ENABLED=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Lax"
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE","false").lower()=="true"
    AUTO_INIT_DB=os.getenv("AUTO_INIT_DB","true").lower()=="true"
