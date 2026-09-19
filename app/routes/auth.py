from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,current_user
from ..extensions import db
from ..models import User
auth_bp=Blueprint("auth",__name__)
@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:return redirect(url_for("admin.dashboard" if current_user.role=="admin" else "user.dashboard"))
    if request.method=="POST":
        u=User.query.filter_by(email=request.form.get("email","").strip().lower()).first()
        if u and u.is_active and u.check_password(request.form.get("password","")):
            login_user(u); return redirect(url_for("admin.dashboard" if u.role=="admin" else "user.dashboard"))
        flash("Invalid email or password.","error")
    return render_template("auth/login.html")
@auth_bp.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:return redirect(url_for("public.home"))
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); pw=request.form.get("password","")
        if not name or not email or len(pw)<8: flash("Name, email and an 8+ character password are required.","error")
        elif User.query.filter_by(email=email).first(): flash("Email already registered.","error")
        else:
            u=User(name=name,email=email,role="customer",is_active=True); u.set_password(pw); db.session.add(u); db.session.commit(); flash("Account created.","success"); return redirect(url_for("auth.login"))
    return render_template("auth/register.html")
@auth_bp.get("/logout")
def logout(): logout_user(); return redirect(url_for("public.home"))
