import os
from flask import Flask, render_template
from config import Config
from .extensions import db, login_manager, migrate, csrf
from .models import User
from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.admin import admin_bp
from .routes.phase2 import phase2_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(phase2_bp)

    @app.errorhandler(404)
    def e404(e):
        return render_template("errors/error.html", code=404, message="Page not found"), 404

    @app.errorhandler(500)
    def e500(e):
        db.session.rollback()
        return render_template(
            "errors/error.html",
            code=500,
            message="Something went wrong. Check the server logs for the root cause.",
        ), 500

    # Render can keep using its existing auto-init behavior. Vercel should
    # normally use a persistent hosted PostgreSQL database and migrations.
    # The only automatic Vercel schema creation is the /tmp fallback used when
    # DATABASE_URL has not been configured for a preview.
    if app.config.get("AUTO_INIT_DB", True):
        with app.app_context():
            try:
                db.create_all()
                ensure_demo()
            except Exception as exc:
                app.logger.exception("Database initialization failed: %s", exc)

    return app


def ensure_demo():
    if os.getenv("AUTO_SEED_DEMO", "false").lower() != "true":
        return

    admin = User.query.filter_by(email="admin.demo@gyanpath.local").first() or User(
        name="Gyanpath Admin",
        email="admin.demo@gyanpath.local",
        role="admin",
    )
    admin.name = "Gyanpath Admin"
    admin.role = "admin"
    admin.is_active = True
    admin.set_password("Gyanpath@Demo2026!")
    db.session.add(admin)

    user = User.query.filter_by(email="user.demo@gyanpath.local").first() or User(
        name="Demo User",
        email="user.demo@gyanpath.local",
        role="customer",
    )
    user.name = "Demo User"
    user.role = "customer"
    user.is_active = True
    user.set_password("Gyanpath@Demo2026!")
    db.session.add(user)
    db.session.commit()
