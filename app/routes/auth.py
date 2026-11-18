from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(
            "admin.dashboard" if current_user.role == "admin" else "user.dashboard"
        ))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter(db.func.lower(User.email) == email).first()

        if user and user.is_active and user.check_password(password):
            login_user(user, remember=bool(request.form.get("remember")))
            next_url = request.args.get("next")
            # Do not redirect to an external URL supplied through the query string.
            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for(
                "admin.dashboard" if user.role == "admin" else "user.dashboard"
            ))

        # Keep the response generic so the login page does not disclose whether
        # an account exists or is inactive.
        flash("Invalid email or password. Check your credentials or contact the site administrator.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Name, email and an 8+ character password are required.", "error")
        elif User.query.filter(db.func.lower(User.email) == email).first():
            flash("Email already registered.", "error")
        else:
            user = User(name=name, email=email, role="customer", is_active=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.home"))
