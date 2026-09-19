import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///gyanpath.db").replace("postgres://","postgresql://",1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
