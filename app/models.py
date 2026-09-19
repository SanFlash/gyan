from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from .extensions import db
class T:
    created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
class User(UserMixin,T,db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); email=db.Column(db.String(255),unique=True,nullable=False,index=True); password_hash=db.Column(db.String(255),nullable=False); role=db.Column(db.String(40),default="customer",nullable=False); is_active=db.Column(db.Boolean,default=True,nullable=False); phone=db.Column(db.String(40),default=""); address=db.Column(db.Text,default="")
    def set_password(self,p): self.password_hash=generate_password_hash(p)
    def check_password(self,p): return check_password_hash(self.password_hash,p)
class Project(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); slug=db.Column(db.String(200),unique=True,nullable=False,index=True); category=db.Column(db.String(100),nullable=False); location=db.Column(db.String(180),default=""); status=db.Column(db.String(30),default="Upcoming"); short_description=db.Column(db.Text,default=""); description=db.Column(db.Text,default=""); published=db.Column(db.Boolean,default=True); featured=db.Column(db.Boolean,default=False)
class Event(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180),nullable=False); description=db.Column(db.Text,default=""); location=db.Column(db.String(180),default=""); event_date=db.Column(db.Date,nullable=True); start_time=db.Column(db.Time,nullable=True); end_time=db.Column(db.Time,nullable=True); registration_enabled=db.Column(db.Boolean,default=False); status=db.Column(db.String(30),default="Upcoming")
class EventRegistration(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); event_id=db.Column(db.Integer,db.ForeignKey("event.id"),nullable=False); user_id=db.Column(db.Integer,db.ForeignKey("user.id")); name=db.Column(db.String(120),nullable=False); email=db.Column(db.String(255),nullable=False); phone=db.Column(db.String(40),default=""); status=db.Column(db.String(30),default="Registered"); event=db.relationship("Event",backref="registrations")
class VolunteerApplication(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id")); name=db.Column(db.String(120),nullable=False); email=db.Column(db.String(255),nullable=False); phone=db.Column(db.String(40),default=""); city=db.Column(db.String(120),default=""); skills=db.Column(db.Text,default=""); availability=db.Column(db.String(120),default=""); message=db.Column(db.Text,default=""); consent=db.Column(db.Boolean,default=False); status=db.Column(db.String(30),default="Pending")
class Donation(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey("user.id")); donor_name=db.Column(db.String(120),nullable=False); donor_email=db.Column(db.String(255),nullable=False); donor_phone=db.Column(db.String(40),default=""); amount=db.Column(db.Numeric(12,2),nullable=False); currency=db.Column(db.String(10),default="INR"); purpose=db.Column(db.String(180),default=""); anonymous=db.Column(db.Boolean,default=False); status=db.Column(db.String(30),default="Pending")
class ContactMessage(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),nullable=False); email=db.Column(db.String(255),nullable=False); phone=db.Column(db.String(40),default=""); subject=db.Column(db.String(180),default=""); message=db.Column(db.Text,nullable=False); status=db.Column(db.String(30),default="New")
class Artisan(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(140),nullable=False); slug=db.Column(db.String(160),unique=True,nullable=False); location=db.Column(db.String(180),default=""); craft=db.Column(db.String(140),default=""); biography=db.Column(db.Text,default=""); image_url=db.Column(db.String(700),default=""); published=db.Column(db.Boolean,default=True)
class BlogPost(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(220),nullable=False); slug=db.Column(db.String(240),unique=True,nullable=False); excerpt=db.Column(db.Text,default=""); content=db.Column(db.Text,default=""); published=db.Column(db.Boolean,default=False)
class ImpactStatistic(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); label=db.Column(db.String(120),nullable=False); value=db.Column(db.String(60),default="0"); published=db.Column(db.Boolean,default=True); sort_order=db.Column(db.Integer,default=0)
class Document(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); category=db.Column(db.String(100),default="Other"); year=db.Column(db.Integer); description=db.Column(db.Text,default=""); file_url=db.Column(db.String(700),nullable=False); visibility=db.Column(db.String(30),default="public")
class ProjectBrief(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); project_id=db.Column(db.Integer,db.ForeignKey("project.id"),unique=True,nullable=False); duration=db.Column(db.String(180),default=""); objective=db.Column(db.Text,default=""); beneficiaries=db.Column(db.Text,default=""); activities=db.Column(db.Text,default=""); outcomes=db.Column(db.Text,default=""); photos_url=db.Column(db.Text,default=""); partners=db.Column(db.Text,default=""); project=db.relationship("Project",backref=db.backref("brief",uselist=False,cascade="all, delete-orphan"))
class GalleryItem(T,db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); category=db.Column(db.String(100),default="Other"); image_url=db.Column(db.String(700),default=""); location=db.Column(db.String(180),default=""); event_date=db.Column(db.Date,nullable=True); description=db.Column(db.Text,default=""); published=db.Column(db.Boolean,default=False); sort_order=db.Column(db.Integer,default=0)
class SiteSetting(db.Model):
    id=db.Column(db.Integer,primary_key=True); key=db.Column(db.String(100),unique=True,nullable=False); value=db.Column(db.Text,default="")
