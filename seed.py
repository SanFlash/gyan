from app import create_app, db
from app.models import User, Project, Event, SiteSetting

app = create_app()
with app.app_context():
    db.create_all()
    def ensure_user(email, password, role):
        u=User.query.filter_by(email=email).first()
        if not u:
            u=User(email=email, role=role); db.session.add(u)
        u.set_password(password); u.role=role
        return u
    ensure_user("admin.demo@gyanpath.local","Gyanpath@Demo2026!","admin")
    ensure_user("staff.demo@gyanpath.local","Gyanpath@Demo2026!","staff")
    ensure_user("user.demo@gyanpath.local","Gyanpath@Demo2026!","user")
    if Project.query.count()==0:
        db.session.add(Project(title="Community Development Initiative",slug="community-development-initiative",description="Demo Content — update this project from the admin panel with verified organizational information.",short_description="Demo Content — organization-managed project information.",status="Draft",featured=True,published=False))
    if Event.query.count()==0:
        db.session.add(Event(title="Community Event — Demo",description="Demo Content — event details will be updated by the organization.",location="Bhopal, Madhya Pradesh",published=False))
    for k,v in {"site_name":"Gyanpath Shiksha Evam Samaj Kalyan Samiti","site_tagline":"Empowering Communities. Creating Opportunities. Building a Better Future.","content_notice":"Information will be updated by the organization."}.items():
        s=SiteSetting.query.filter_by(key=k).first()
        if not s: db.session.add(SiteSetting(key=k,value=v))
        else: s.value=v
    db.session.commit()
    print("Seed completed.")
