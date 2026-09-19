from functools import wraps
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from ..extensions import db
from ..models import User,Project,Event,ContactMessage
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")
def admin_required(f):
    @wraps(f)
    @login_required
    def w(*a,**k):
        if current_user.role!="admin": flash("Admin access required.","error"); return redirect(url_for("user.dashboard"))
        return f(*a,**k)
    return w
@admin_bp.get("/")
@admin_required
def dashboard(): return render_template("admin/dashboard.html",counts={"users":User.query.count(),"projects":Project.query.count(),"events":Event.query.count(),"enquiries":ContactMessage.query.count()})
@admin_bp.get("/projects")
@admin_required
def projects(): return render_template("admin/projects.html",projects=Project.query.order_by(Project.created_at.desc()).all())
@admin_bp.route("/projects/new",methods=["GET","POST"])
@admin_required
def project_new():
    if request.method=="POST":
        title=request.form.get("title","").strip(); slug=request.form.get("slug","").strip().lower(); cat=request.form.get("category","").strip()
        if not title or not slug or not cat: flash("Title, slug and category are required.","error")
        elif Project.query.filter_by(slug=slug).first(): flash("Slug already exists.","error")
        else:
            p=Project(title=title,slug=slug,category=cat,location=request.form.get("location",""),status=request.form.get("status","Upcoming"),short_description=request.form.get("short_description",""),description=request.form.get("description",""),published=bool(request.form.get("published"))); db.session.add(p); db.session.commit(); flash("Project created.","success"); return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html",project=None)
@admin_bp.route("/projects/<int:id>/edit",methods=["GET","POST"])
@admin_required
def project_edit(id):
    p=db.session.get(Project,id)
    if not p:return "Project not found",404
    if request.method=="POST":
        slug=request.form.get("slug","").strip().lower(); dup=Project.query.filter(Project.slug==slug,Project.id!=id).first()
        if not request.form.get("title") or not slug or not request.form.get("category"): flash("Required fields are missing.","error")
        elif dup: flash("Slug already exists.","error")
        else:
            p.title=request.form.get("title").strip(); p.slug=slug; p.category=request.form.get("category").strip(); p.location=request.form.get("location",""); p.status=request.form.get("status","Upcoming"); p.short_description=request.form.get("short_description",""); p.description=request.form.get("description",""); p.published=bool(request.form.get("published")); db.session.commit(); flash("Project updated.","success"); return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html",project=p)
@admin_bp.post("/projects/<int:id>/delete")
@admin_required
def project_delete(id):
    p=db.session.get(Project,id)
    if p:db.session.delete(p);db.session.commit();flash("Project deleted.","success")
    return redirect(url_for("admin.projects"))
@admin_bp.get("/users")
@admin_required
def users(): return render_template("admin/users.html",users=User.query.order_by(User.created_at.desc()).all())
@admin_bp.get("/messages")
@admin_required
def messages(): return render_template("admin/messages.html",messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
