from functools import wraps
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_required,current_user
from ..extensions import db
from ..models import User,Project,Event,ContactMessage,VolunteerApplication,Donation,Artisan,BlogPost,ImpactStatistic,Document,SiteSetting
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
def dashboard(): return render_template("admin/dashboard.html",counts={"users":User.query.count(),"projects":Project.query.count(),"events":Event.query.count(),"enquiries":ContactMessage.query.count(),"volunteers":VolunteerApplication.query.count(),"donations":Donation.query.count()})
@admin_bp.get("/projects")
@admin_required
def projects(): return render_template("admin/projects.html",projects=Project.query.order_by(Project.created_at.desc()).all())
def save_project(p):
 p.title=request.form.get("title","").strip();p.slug=request.form.get("slug","").strip().lower();p.category=request.form.get("category","").strip();p.location=request.form.get("location","").strip();p.status=request.form.get("status","Upcoming");p.short_description=request.form.get("short_description","").strip();p.description=request.form.get("description","").strip();p.published=bool(request.form.get("published"));p.featured=bool(request.form.get("featured"))
@admin_bp.route("/projects/new",methods=["GET","POST"])
@admin_required
def project_new():
 if request.method=="POST":
  p=Project();save_project(p)
  if not p.title or not p.slug or not p.category: flash("Title, slug and category are required.","error")
  elif Project.query.filter_by(slug=p.slug).first(): flash("Slug already exists.","error")
  else: db.session.add(p);db.session.commit();flash("Project created.","success");return redirect(url_for("admin.projects"))
 return render_template("admin/project_form.html",project=None)
@admin_bp.route("/projects/<int:id>/edit",methods=["GET","POST"])
@admin_required
def project_edit(id):
 p=db.session.get(Project,id)
 if not p:return "Project not found",404
 if request.method=="POST":
  save_project(p);dup=Project.query.filter(Project.slug==p.slug,Project.id!=id).first()
  if not p.title or not p.slug or not p.category: flash("Required fields are missing.","error")
  elif dup: flash("Slug already exists.","error")
  else: db.session.commit();flash("Project updated.","success");return redirect(url_for("admin.projects"))
 return render_template("admin/project_form.html",project=p)
@admin_bp.post("/projects/<int:id>/delete")
@admin_required
def project_delete(id):
 p=db.session.get(Project,id)
 if p:db.session.delete(p);db.session.commit();flash("Project deleted.","success")
 return redirect(url_for("admin.projects"))
@admin_bp.get("/events")
@admin_required
def events(): return render_template("admin/events.html",events=Event.query.order_by(Event.event_date.desc().nullslast()).all())
@admin_bp.route("/events/new",methods=["GET","POST"])
@admin_required
def event_new():
 if request.method=="POST":
  from datetime import datetime
  d=request.form.get("event_date") or None
  e=Event(title=request.form.get("title","").strip(),description=request.form.get("description",""),location=request.form.get("location",""),event_date=datetime.strptime(d,"%Y-%m-%d").date() if d else None,status=request.form.get("status","Upcoming"),registration_enabled=bool(request.form.get("registration_enabled")));db.session.add(e);db.session.commit();flash("Event created.","success");return redirect(url_for("admin.events"))
 return render_template("admin/event_form.html",event=None)
@admin_bp.route("/events/<int:id>/edit",methods=["GET","POST"])
@admin_required
def event_edit(id):
 from datetime import datetime
 e=db.session.get(Event,id)
 if not e:return "Event not found",404
 if request.method=="POST":
  d=request.form.get("event_date") or None;e.title=request.form.get("title","").strip();e.description=request.form.get("description","");e.location=request.form.get("location","");e.event_date=datetime.strptime(d,"%Y-%m-%d").date() if d else None;e.status=request.form.get("status","Upcoming");e.registration_enabled=bool(request.form.get("registration_enabled"));db.session.commit();flash("Event updated.","success");return redirect(url_for("admin.events"))
 return render_template("admin/event_form.html",event=e)
@admin_bp.post("/events/<int:id>/delete")
@admin_required
def event_delete(id):
 e=db.session.get(Event,id)
 if e:db.session.delete(e);db.session.commit();flash("Event deleted.","success")
 return redirect(url_for("admin.events"))
@admin_bp.get("/users")
@admin_required
def users(): return render_template("admin/users.html",users=User.query.order_by(User.created_at.desc()).all())
@admin_bp.get("/messages")
@admin_required
def messages(): return render_template("admin/messages.html",messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
@admin_bp.get("/volunteers")
@admin_required
def volunteers(): return render_template("admin/volunteers.html",items=VolunteerApplication.query.order_by(VolunteerApplication.created_at.desc()).all())
@admin_bp.get("/donations")
@admin_required
def donations(): return render_template("admin/donations.html",items=Donation.query.order_by(Donation.created_at.desc()).all())
@admin_bp.get("/artisans")
@admin_required
def artisans(): return render_template("admin/artisans.html",items=Artisan.query.order_by(Artisan.created_at.desc()).all())
@admin_bp.get("/blog")
@admin_required
def blog(): return render_template("admin/blog.html",items=BlogPost.query.order_by(BlogPost.created_at.desc()).all())
@admin_bp.get("/impact")
@admin_required
def impact(): return render_template("admin/impact.html",items=ImpactStatistic.query.order_by(ImpactStatistic.sort_order).all())
@admin_bp.get("/documents")
@admin_required
def documents(): return render_template("admin/documents.html",items=Document.query.order_by(Document.id.desc()).all())
@admin_bp.route("/settings",methods=["GET","POST"])
@admin_required
def settings():
 if request.method=="POST":
  for key,value in request.form.items():
   if key=="csrf_token":continue
   s=SiteSetting.query.filter_by(key=key).first() or SiteSetting(key=key);s.value=value;db.session.add(s)
  db.session.commit();flash("Site settings saved.","success")
 vals={s.key:s.value for s in SiteSetting.query.all()};return render_template("admin/settings.html",settings=vals)
