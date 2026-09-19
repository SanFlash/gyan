from flask import Blueprint,render_template,request,redirect,url_for,flash
from email_validator import validate_email,EmailNotValidError
from ..extensions import db
from ..models import Project,Event,ContactMessage,SiteSetting
public_bp=Blueprint("public",__name__)
@public_bp.app_context_processor
def settings(): return {"site_settings":{x.key:x.value for x in SiteSetting.query.all()}}
@public_bp.get("/")
def home(): return render_template("public/home.html",projects=Project.query.filter_by(published=True).order_by(Project.created_at.desc()).limit(6).all(),events=Event.query.order_by(Event.created_at.desc()).limit(3).all())
@public_bp.get("/about")
def about(): return render_template("public/about.html")
@public_bp.get("/work")
def work(): return render_template("public/work.html")
@public_bp.get("/projects")
def projects(): return render_template("public/projects.html",projects=Project.query.filter_by(published=True).order_by(Project.created_at.desc()).all())
@public_bp.get("/projects/<slug>")
def project_detail(slug): return render_template("public/project_detail.html",project=Project.query.filter_by(slug=slug,published=True).first_or_404())
@public_bp.get("/events")
def events(): return render_template("public/events.html",events=Event.query.order_by(Event.created_at.desc()).all())
@public_bp.route("/contact",methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip(); message=request.form.get("message","").strip()
        try: validate_email(email)
        except EmailNotValidError: flash("Enter a valid email address.","error"); return render_template("public/contact.html")
        if not name or not message: flash("Name and message are required.","error")
        else: db.session.add(ContactMessage(name=name,email=email,phone=request.form.get("phone",""),subject=request.form.get("subject",""),message=message)); db.session.commit(); flash("Your message has been received.","success"); return redirect(url_for("public.contact"))
    return render_template("public/contact.html")
