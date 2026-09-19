import os
from flask import Flask,render_template
from config import Config
from .extensions import db,login_manager,migrate,csrf
from .models import User
from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.admin import admin_bp
from .routes.phase2 import phase2_bp
def create_app(config_class=Config):
    app=Flask(__name__);app.config.from_object(config_class);db.init_app(app);migrate.init_app(app,db);login_manager.init_app(app);csrf.init_app(app);login_manager.login_view="auth.login"
    app.register_blueprint(public_bp);app.register_blueprint(auth_bp);app.register_blueprint(user_bp);app.register_blueprint(admin_bp);app.register_blueprint(phase2_bp)
    @app.errorhandler(404)
    def e404(e):return render_template("errors/error.html",code=404,message="Page not found"),404
    @app.errorhandler(500)
    def e500(e):db.session.rollback();return render_template("errors/error.html",code=500,message="Something went wrong"),500
    if app.config.get("AUTO_INIT_DB",True):
        with app.app_context(): db.create_all();ensure_demo()
    return app
def ensure_demo():
    if os.getenv("AUTO_SEED_DEMO","true").lower()!="true":return
    if not User.query.filter_by(email="admin.demo@gyanpath.local").first():
        u=User(name="Gyanpath Admin",email="admin.demo@gyanpath.local",role="admin");u.set_password("Gyanpath@Demo2026!");db.session.add(u)
    if not User.query.filter_by(email="user.demo@gyanpath.local").first():
        u=User(name="Demo User",email="user.demo@gyanpath.local",role="customer");u.set_password("Gyanpath@Demo2026!");db.session.add(u)
    db.session.commit()
