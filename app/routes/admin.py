from functools import wraps
from flask import Blueprint,render_template,request,redirect,url_for,flash
import os
from flask_login import login_required,current_user
from ..extensions import db
from ..models import User,Project,ProjectBrief,Event,ContactMessage,VolunteerApplication,Donation,Artisan,BlogPost,ImpactStatistic,Document,GalleryItem,SiteSetting
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")
def _media_url(field_name, folder):
 f=request.files.get(field_name)
 if f and f.filename:
  try:
   import cloudinary
   import cloudinary.uploader
   cloudinary.config(cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME",""),api_key=os.getenv("CLOUDINARY_API_KEY",""),api_secret=os.getenv("CLOUDINARY_API_SECRET",""),secure=True)
   if os.getenv("CLOUDINARY_CLOUD_NAME") and os.getenv("CLOUDINARY_API_KEY") and os.getenv("CLOUDINARY_API_SECRET"):
    return cloudinary.uploader.upload(f,folder=folder)["secure_url"]
  except Exception:
   flash("Media upload failed. You can use an approved hosted image URL instead.","error")
 return request.form.get(field_name+"_url","").strip()

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
 p.title=request.form.get("title","").strip();p.slug=request.form.get("slug","").strip().lower();p.category=request.form.get("category","").strip();p.location=request.form.get("location","").strip();p.status=request.form.get("status","Upcoming");p.short_description=request.form.get("short_description","").strip();p.description=request.form.get("description","").strip();p.published=bool(request.form.get("published"));p.featured=bool(request.form.get("featured"));b=getattr(p,"brief",None) or ProjectBrief(project=p);b.duration=request.form.get("duration","").strip();b.objective=request.form.get("objective","").strip();b.beneficiaries=request.form.get("beneficiaries","").strip();b.activities=request.form.get("activities","").strip();b.outcomes=request.form.get("outcomes","").strip();b.photos_url=request.form.get("photos_url","").strip();b.partners=request.form.get("partners","").strip();db.session.add(b)
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
@admin_bp.route("/artisans/new",methods=["GET","POST"])
@admin_required
def artisan_new():
 if request.method=="POST":
  a=Artisan(name=request.form.get("name","").strip(),slug=request.form.get("slug","").strip().lower(),location=request.form.get("location",""),craft=request.form.get("craft",""),biography=request.form.get("biography",""),image_url=request.form.get("image_url",""),published=bool(request.form.get("published")));db.session.add(a);db.session.commit();flash("Artisan created.","success");return redirect(url_for("admin.artisans"))
 return render_template("admin/artisan_form.html",item=None)
@admin_bp.route("/artisans/<int:id>/edit",methods=["GET","POST"])
@admin_required
def artisan_edit(id):
 a=db.session.get(Artisan,id)
 if not a:return "Artisan not found",404
 if request.method=="POST":
  a.name=request.form.get("name","").strip();a.slug=request.form.get("slug","").strip().lower();a.location=request.form.get("location","");a.craft=request.form.get("craft","");a.biography=request.form.get("biography","");a.image_url=request.form.get("image_url","");a.published=bool(request.form.get("published"));db.session.commit();flash("Artisan updated.","success");return redirect(url_for("admin.artisans"))
 return render_template("admin/artisan_form.html",item=a)
@admin_bp.post("/artisans/<int:id>/delete")
@admin_required
def artisan_delete(id):
 a=db.session.get(Artisan,id)
 if a:db.session.delete(a);db.session.commit();flash("Artisan deleted.","success")
 return redirect(url_for("admin.artisans"))
@admin_bp.get("/blog")
@admin_required
def blog(): return render_template("admin/blog.html",items=BlogPost.query.order_by(BlogPost.created_at.desc()).all())
@admin_bp.route("/blog/new",methods=["GET","POST"])
@admin_required
def blog_new():
 if request.method=="POST":
  p=BlogPost(title=request.form.get("title","").strip(),slug=request.form.get("slug","").strip().lower(),excerpt=request.form.get("excerpt",""),content=request.form.get("content",""),published=bool(request.form.get("published")));db.session.add(p);db.session.commit();flash("News post created.","success");return redirect(url_for("admin.blog"))
 return render_template("admin/blog_form.html",item=None)
@admin_bp.route("/blog/<int:id>/edit",methods=["GET","POST"])
@admin_required
def blog_edit(id):
 p=db.session.get(BlogPost,id)
 if not p:return "Post not found",404
 if request.method=="POST":
  p.title=request.form.get("title","").strip();p.slug=request.form.get("slug","").strip().lower();p.excerpt=request.form.get("excerpt","");p.content=request.form.get("content","");p.published=bool(request.form.get("published"));db.session.commit();flash("News post updated.","success");return redirect(url_for("admin.blog"))
 return render_template("admin/blog_form.html",item=p)
@admin_bp.post("/blog/<int:id>/delete")
@admin_required
def blog_delete(id):
 p=db.session.get(BlogPost,id)
 if p:db.session.delete(p);db.session.commit();flash("News post deleted.","success")
 return redirect(url_for("admin.blog"))
@admin_bp.get("/impact")
@admin_required
def impact(): return render_template("admin/impact.html",items=ImpactStatistic.query.order_by(ImpactStatistic.sort_order).all())
@admin_bp.route("/impact/new",methods=["GET","POST"])
@admin_required
def impact_new():
 if request.method=="POST":
  x=ImpactStatistic(label=request.form.get("label","").strip(),value=request.form.get("value","0").strip(),sort_order=int(request.form.get("sort_order","0") or 0),published=bool(request.form.get("published")));db.session.add(x);db.session.commit();flash("Impact statistic created.","success");return redirect(url_for("admin.impact"))
 return render_template("admin/impact_form.html",item=None)
@admin_bp.route("/impact/<int:id>/edit",methods=["GET","POST"])
@admin_required
def impact_edit(id):
 x=db.session.get(ImpactStatistic,id)
 if not x:return "Statistic not found",404
 if request.method=="POST":
  x.label=request.form.get("label","").strip();x.value=request.form.get("value","0").strip();x.sort_order=int(request.form.get("sort_order","0") or 0);x.published=bool(request.form.get("published"));db.session.commit();flash("Impact statistic updated.","success");return redirect(url_for("admin.impact"))
 return render_template("admin/impact_form.html",item=x)
@admin_bp.post("/impact/<int:id>/delete")
@admin_required
def impact_delete(id):
 x=db.session.get(ImpactStatistic,id)
 if x:db.session.delete(x);db.session.commit();flash("Impact statistic deleted.","success")
 return redirect(url_for("admin.impact"))
@admin_bp.get("/gallery")
@admin_required
def gallery(): return render_template("admin/gallery.html",items=GalleryItem.query.order_by(GalleryItem.sort_order,GalleryItem.id.desc()).all())

@admin_bp.route("/gallery/new",methods=["GET","POST"])
@admin_required
def gallery_new():
 if request.method=="POST":
  x=GalleryItem(title=request.form.get("title","").strip(),category=request.form.get("category","Other").strip(),image_url=_media_url("image","gyanpath/gallery"),location=request.form.get("location","").strip(),description=request.form.get("description","").strip(),published=bool(request.form.get("published")),sort_order=int(request.form.get("sort_order","0") or 0))
  d=request.form.get("event_date") or None
  if d:
   from datetime import datetime
   x.event_date=datetime.strptime(d,"%Y-%m-%d").date()
  if not x.title or not x.image_url: flash("Title and an approved image URL/upload are required.","error")
  else: db.session.add(x);db.session.commit();flash("Gallery item saved.","success");return redirect(url_for("admin.gallery"))
 return render_template("admin/gallery_form.html",item=None)

@admin_bp.route("/gallery/<int:id>/edit",methods=["GET","POST"])
@admin_required
def gallery_edit(id):
 x=db.session.get(GalleryItem,id)
 if not x:return "Gallery item not found",404
 if request.method=="POST":
  x.title=request.form.get("title","").strip();x.category=request.form.get("category","Other").strip();new_url=_media_url("image","gyanpath/gallery");x.image_url=new_url or x.image_url;x.location=request.form.get("location","").strip();x.description=request.form.get("description","").strip();x.published=bool(request.form.get("published"));x.sort_order=int(request.form.get("sort_order","0") or 0)
  d=request.form.get("event_date") or None
  from datetime import datetime
  x.event_date=datetime.strptime(d,"%Y-%m-%d").date() if d else None
  db.session.commit();flash("Gallery item updated.","success");return redirect(url_for("admin.gallery"))
 return render_template("admin/gallery_form.html",item=x)

@admin_bp.post("/gallery/<int:id>/delete")
@admin_required
def gallery_delete(id):
 x=db.session.get(GalleryItem,id)
 if x: db.session.delete(x);db.session.commit();flash("Gallery item deleted.","success")
 return redirect(url_for("admin.gallery"))

@admin_bp.get("/documents")
@admin_required
def documents(): return render_template("admin/documents.html",items=Document.query.order_by(Document.year.desc().nullslast(),Document.id.desc()).all())

@admin_bp.route("/documents/new",methods=["GET","POST"])
@admin_required
def document_new():
 if request.method=="POST":
  x=Document(title=request.form.get("title","").strip(),category=request.form.get("category","Other").strip(),year=int(request.form.get("year") or 0) or None,description=request.form.get("description","").strip(),file_url=request.form.get("file_url","").strip(),visibility=request.form.get("visibility","private"))
  if not x.title or not x.file_url: flash("Title and approved document URL are required.","error")
  else: db.session.add(x);db.session.commit();flash("Document added.","success");return redirect(url_for("admin.documents"))
 return render_template("admin/document_form.html",item=None)

@admin_bp.route("/documents/<int:id>/edit",methods=["GET","POST"])
@admin_required
def document_edit(id):
 x=db.session.get(Document,id)
 if not x:return "Document not found",404
 if request.method=="POST":
  x.title=request.form.get("title","").strip();x.category=request.form.get("category","Other").strip();x.year=int(request.form.get("year") or 0) or None;x.description=request.form.get("description","").strip();x.file_url=request.form.get("file_url","").strip();x.visibility=request.form.get("visibility","private");db.session.commit();flash("Document updated.","success");return redirect(url_for("admin.documents"))
 return render_template("admin/document_form.html",item=x)

@admin_bp.post("/documents/<int:id>/delete")
@admin_required
def document_delete(id):
 x=db.session.get(Document,id)
 if x: db.session.delete(x);db.session.commit();flash("Document deleted.","success")
 return redirect(url_for("admin.documents"))
@admin_bp.route("/settings",methods=["GET","POST"])
@admin_required
def settings():
 if request.method=="POST":
  for key,value in request.form.items():
   if key=="csrf_token":continue
   s=SiteSetting.query.filter_by(key=key).first() or SiteSetting(key=key);s.value=value;db.session.add(s)
  db.session.commit();flash("Site settings saved.","success")
 vals={s.key:s.value for s in SiteSetting.query.all()};return render_template("admin/settings.html",settings=vals)

@admin_bp.post("/status/<model>/<int:id>")
@admin_required
def status_update(model,id):
 cls={"volunteer":VolunteerApplication,"donation":Donation,"message":ContactMessage}.get(model)
 obj=db.session.get(cls,id) if cls else None
 if obj:
  obj.status=request.form.get("status",obj.status);db.session.commit();flash("Status updated.","success")
 return redirect(request.referrer or url_for("admin.dashboard"))
