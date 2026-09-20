"""Dedicated Vercel/WSGI entrypoint.

Render continues to use run:app. Vercel loads this top-level app object.
"""
from app import create_app

app = create_app()

__all__ = ["app"]
