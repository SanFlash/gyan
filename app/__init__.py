import os
from flask import Flask, render_template, current_app
from config import Config
from .extensions import db, login_manager, migrate, csrf
from .models import User
from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.admin import admin_bp
from .routes.phase2 import phase2_bp
from .routes.events_detail import events_bp


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
    app.register_blueprint(events_bp)

    @app.errorhandler(404)
    def e404(e):
        return render_template("errors/error.html", code=404, message="Page not found"), 404

    @app.errorhandler(500)
    def e500(e):
        db.session.rollback()
        return render_template("errors/error.html", code=500, message="Something went wrong. Check deployment logs."), 500

    # Create missing tables without dropping or replacing existing records.
    if app.config.get("AUTO_INIT_DB", True):
        with app.app_context():
            try:
                db.create_all()
                ensure_demo()
                from .gssks_content import seed_gssks_events
                added = seed_gssks_events()
                if added:
                    app.logger.info("Added %s GSSKS programme/event entries.", added)
            except Exception:
                app.logger.exception("Database initialization or GSSKS content seeding failed")

    return app


def ensure_demo():
    """Provision the configured production admin only when credentials are supplied."""
    admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    admin_name = os.getenv("ADMIN_NAME", "Gyanpath Administrator").strip()

    if admin_email and admin_password:
        admin = User.query.filter(db.func.lower(User.email) == admin_email).first()
        if admin is None:
            admin = User(name=admin_name or "Gyanpath Administrator", email=admin_email, role="admin")
        admin.name = admin_name or "Gyanpath Administrator"
        admin.email = admin_email
        admin.role = "admin"
        admin.is_active = True
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        current_app.logger.info("Configured admin account is available: %s", admin_email)

    if os.getenv("AUTO_SEED_DEMO", "false").lower() != "true":
        return

    demo_password = os.getenv("DEMO_ADMIN_PASSWORD", "")
    demo_email = os.getenv("DEMO_ADMIN_EMAIL", "admin.demo@gyanpath.local").strip().lower()
    if not demo_password:
        current_app.logger.warning("AUTO_SEED_DEMO=true but DEMO_ADMIN_PASSWORD is empty; no demo admin was created.")
        return
    demo = User.query.filter(db.func.lower(User.email) == demo_email).first()
    if demo is None:
        demo = User(name="Gyanpath Demo Admin", email=demo_email, role="admin")
    demo.name = "Gyanpath Demo Admin"
    demo.role = "admin"
    demo.is_active = True
    demo.set_password(demo_password)
    db.session.add(demo)
    db.session.commit()
