"""Idempotent production-safe seed/bootstrap for GSSKS.

Run locally against the intended PostgreSQL database with:
    python seed.py

The seed only writes verified/public information already approved for this
website. It does not fabricate gallery images, partners, beneficiaries, or
additional programmes.
"""
from datetime import date
from app import create_app, db
from app.models import User, Project, SiteSetting, ImpactStatistic


app = create_app()


def ensure_user(email, password, role, name):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
    user.name = name
    user.set_password(password)
    user.role = role
    user.is_active = True
    return user


def ensure_setting(key, value):
    setting = SiteSetting.query.filter_by(key=key).first()
    if not setting:
        setting = SiteSetting(key=key)
        db.session.add(setting)
    setting.value = value


def ensure_project():
    project = Project.query.filter_by(slug="gandhi-shilp-bazaar-2024").first()
    if not project:
        project = Project(slug="gandhi-shilp-bazaar-2024")
        db.session.add(project)

    project.title = "Gandhi Shilp Bazaar 2024"
    project.category = "Artisan & Livelihood Development"
    project.location = "Urban Haat, Gauhar Mahal, Bhopal"
    project.status = "Completed"
    project.short_description = (
        "Gandhi Shilp Bazaar held from 11–17 September 2024 at Urban Haat, "
        "Gauhar Mahal, Bhopal."
    )
    project.description = (
        "A documented seven-day Gandhi Shilp Bazaar programme conducted by "
        "Gyan Path Shiksha Evam Samaj Kalyan Samiti at Urban Haat, Gauhar Mahal, "
        "Bhopal, from 11–17 September 2024. The supplied organisational brief "
        "records 50 artisans and reported sales of more than ₹14,95,577."
    )
    project.published = True
    project.featured = True
    return project


def ensure_stat(value, label, sort_order):
    stat = ImpactStatistic.query.filter_by(label=label).first()
    if not stat:
        stat = ImpactStatistic(label=label)
        db.session.add(stat)
    stat.value = value
    stat.published = True
    stat.sort_order = sort_order


with app.app_context():
    db.create_all()

    # Demo/admin accounts remain opt-in. Do not enable AUTO_SEED_DEMO in
    # production unless these credentials are intentionally required.
    if __import__("os").getenv("AUTO_SEED_DEMO", "false").lower() == "true":
        ensure_user(
            "admin.demo@gyanpath.local",
            "Gyanpath@Demo2026!",
            "admin",
            "Gyanpath Admin",
        )
        ensure_user(
            "staff.demo@gyanpath.local",
            "Gyanpath@Demo2026!",
            "staff",
            "Gyanpath Staff",
        )
        ensure_user(
            "user.demo@gyanpath.local",
            "Gyanpath@Demo2026!",
            "customer",
            "Demo User",
        )

    ensure_setting(
        "site_name",
        "Gyan Path Shiksha Evam Samaj Kalyan Samiti",
    )
    ensure_setting("site_short_name", "GSSKS")
    ensure_setting(
        "site_tagline",
        "Education · Awareness · Empowerment",
    )
    ensure_setting("established", "1992")
    ensure_setting("registration_no", "1262/92")
    ensure_setting(
        "recognition",
        "Recognised by the Government of Madhya Pradesh",
    )
    ensure_setting(
        "address",
        "Sunder Nagar, Chhola Road, Behind Dussehra Maidan, Block Fanda, "
        "Bhopal, Madhya Pradesh – 462001",
    )
    ensure_setting("phone", "0755-4278487")
    ensure_setting("mobile", "088893937454")
    ensure_setting("email", "gyanpathngo.176@gmail.com")

    ensure_project()

    ensure_stat("1992", "Year established", 1)
    ensure_stat("50", "Artisans benefited in Gandhi Shilp Bazaar 2024", 2)
    ensure_stat("₹14,95,577+", "Reported sales during Gandhi Shilp Bazaar 2024", 3)

    db.session.commit()
    print("GSSKS seed completed successfully.")
