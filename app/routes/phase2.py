from decimal import Decimal,InvalidOperation
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import current_user
from ..extensions import db
from ..models import Artisan,Event,EventRegistration,VolunteerApplication,Donation,BlogPost,ImpactStatistic,Document
phase2_bp=Blueprint("phase2",__name__)
@phase2_bp.get("/artisans")
def artisans(): return render_template("public/artisans.html",artisans=Artisan.query.filter_by(published=True).all())
@phase2_bp.get("/artisans/<slug>")
def artisan_detail(slug): return render_template("public/artisan_detail.html",artisan=Artisan.query.filter_by(slug=slug,published=True).first_or_404())
@phase2_bp.route("/volunteer",methods=["GET","POST"])
def volunteer():
    if request.method=="POST":
        if not request.form.get("consent"): flash("Consent is required.","error")
        else:
            a=VolunteerApplication(user_id=current_user.id if current_user.is_authenticated else None,name=request.form.get("name",""),email=request.form.get("email",""),phone=request.form.get("phone",""),city=request.form.get("city",""),skills=request.form.get("skills",""),availability=request.form.get("availability",""),message=request.form.get("message",""),consent=True);db.session.add(a);db.session.commit();flash("Volunteer application received.","success");return redirect(url_for("phase2.volunteer"))
    return render_template("public/volunteer.html")
@phase2_bp.route("/events/<int:id>/register",methods=["POST"])
def event_register(id):
    e=db.session.get(Event,id)
    if not e or not e.registration_enabled: flash("Registration is not available.","error")
    else: db.session.add(EventRegistration(event_id=id,user_id=current_user.id if current_user.is_authenticated else None,name=request.form.get("name",""),email=request.form.get("email",""),phone=request.form.get("phone","")));db.session.commit();flash("Registration received.","success")
    return redirect(url_for("public.events"))
@phase2_bp.route("/donate",methods=["GET","POST"])
def donate():
    if request.method=="POST":
        try:a=Decimal(request.form.get("amount","0"))
        except InvalidOperation:a=Decimal("0")
        if a<=0:flash("Enter a valid amount.","error")
        else: db.session.add(Donation(user_id=current_user.id if current_user.is_authenticated else None,donor_name=request.form.get("name",""),donor_email=request.form.get("email",""),donor_phone=request.form.get("phone",""),amount=a,purpose=request.form.get("purpose",""),anonymous=bool(request.form.get("anonymous"))));db.session.commit();flash("Donation request recorded. Payment gateway can be enabled with production credentials.","success");return redirect(url_for("phase2.donate"))
    return render_template("public/donate.html")
@phase2_bp.get("/blog")
def blog(): return render_template("public/blog.html",posts=BlogPost.query.filter_by(published=True).all())
@phase2_bp.get("/impact")
def impact(): return render_template("public/impact.html",stats=ImpactStatistic.query.filter_by(published=True).order_by(ImpactStatistic.sort_order).all())
@phase2_bp.get("/reports")
def reports(): return render_template("public/reports.html",documents=Document.query.filter_by(visibility="public").all())
