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
        return render_template(
            "errors/error.html",
            code=404,
            message="Page not found",
        ), 404

    @app.errorhandler(500)
    def e500(e):
        db.session.rollback()
        return render_template(
            "errors/error.html",
            code=500,
            message="Something went wrong. Check deployment logs.",
        ), 500

    # A fresh deployment must be able to boot. create_all() is intentionally
    # limited to startup initialization; existing tables/data are preserved.
    # Render and Vercel can disable this later once migrations are established.
    if app.config.get("AUTO_INIT_DB", True):
        with app.app_context():
            try:
                db.create_all()
                ensure_demo()
            except Exception:
                # Do not make the entire Flask import fail because a database
                # is temporarily unavailable. Database-backed requests will
                # report their own error and /api/health exposes DB status.
                app.logger.exception("Database initialization failed")

    return app


def ensure_demo():
    """Provision the configured production admin only when credentials are supplied.

    Set ADMIN_EMAIL and ADMIN_PASSWORD in the hosting provider's environment.
    AUTO_SEED_DEMO is retained only for local demo accounts.
    """
    admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    admin_name = os.getenv("ADMIN_NAME", "Gyanpath Administrator").strip()

    if admin_email and admin_password:
        admin = User.query.filter(
            db.func.lower(User.email) == admin_email
        ).first()
        if admin is None:
            admin = User(name=admin_name or "Gyanpath Administrator",
                         email=admin_email, role="admin")
        admin.name = admin_name or "Gyanpath Administrator"
        admin.email = admin_email
        admin.role = "admin"
        admin.is_active = True
        # Re-apply the configured password so the environment remains the
        # source of truth for this dedicated bootstrap administrator.
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Configured admin account is available: %s", admin_email)

    if os.getenv("AUTO_SEED_DEMO", "false").lower() != "true":
        return

    # Demo accounts are local/testing-only. Never enable AUTO_SEED_DEMO on a
    # public production deployment.
    demo_password = os.getenv("DEMO_ADMIN_PASSWORD", "")
    demo_email = os.getenv("DEMO_ADMIN_EMAIL", "admin.demo@gyanpath.local").strip().lower()
    if not demo_password:
        app.logger.warning(
            "AUTO_SEED_DEMO=true but DEMO_ADMIN_PASSWORD is empty; "
            "no demo admin was created."
        )
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
