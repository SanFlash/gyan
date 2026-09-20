from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import text
from email_validator import validate_email, EmailNotValidError

from ..extensions import db
from ..models import (
    Project,
    Event,
    ContactMessage,
    SiteSetting,
    BlogPost,
    ImpactStatistic,
    Document,
    GalleryItem,
    SiteSection,
)

public_bp = Blueprint("public", __name__)


@public_bp.app_context_processor
def settings():
    # The public site must remain renderable if PostgreSQL is briefly
    # unavailable during a serverless cold start.
    try:
        values = {x.key: x.value for x in SiteSetting.query.all()}
    except Exception:
        db.session.rollback()
        values = {}
    return {"site_settings": values}


@public_bp.get("/")
def home():
    gallery = []
    stats = []
    projects = []
    events = []
    sections = []

    try:
        gallery = (
            GalleryItem.query.filter_by(published=True)
            .order_by(GalleryItem.sort_order, GalleryItem.id.desc())
            .limit(6)
            .all()
        )
        stats = (
            ImpactStatistic.query.filter_by(published=True)
            .order_by(ImpactStatistic.sort_order)
            .limit(4)
            .all()
        )
        projects = (
            Project.query.filter_by(published=True)
            .order_by(Project.created_at.desc())
            .limit(6)
            .all()
        )
        events = (
            Event.query.order_by(Event.event_date.asc().nullslast())
            .limit(3)
            .all()
        )
        sections = (SiteSection.query.filter_by(placement="home", published=True).order_by(SiteSection.sort_order, SiteSection.id).all())
    except Exception:
        db.session.rollback()
        # Keep the public homepage available while the database is being
        # configured or recovering. The database health endpoint exposes the
        # underlying connectivity state.

    if not stats:
        stats = [
            {"value": "410", "label": "Artisans listed in an MSME SFURTI cluster record"},
            {"value": "Rs. 233.92L", "label": "GOI grant / NA share in that record"},
            {"value": "Rs. 20.16L", "label": "IA / SPV share in that record"},
            {"value": "2023–24", "label": "Government handicrafts marketing calendar reference"},
        ]

    return render_template(
        "public/home.html",
        projects=projects,
        events=events,
        stats=stats,
        gallery=gallery,
        sections=sections,
    )


@public_bp.get("/about")
def about():
    return render_template("public/about.html")


@public_bp.get("/mission")
def mission():
    return render_template(
        "public/standard.html",
        eyebrow="Mission",
        title="Mission statement",
        body="The official mission statement will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/vision")
def vision():
    return render_template(
        "public/standard.html",
        eyebrow="Vision",
        title="Vision statement",
        body="The official vision statement will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/work")
def work():
    return render_template("public/work.html")


@public_bp.get("/icps")
def icps():
    return render_template("public/icps.html")


@public_bp.get("/recognition")
def recognition():
    return render_template("public/recognition.html")


@public_bp.get("/education")
def education():
    return render_template(
        "public/standard.html",
        eyebrow="Education",
        title="Education",
        body="Verified education programme information will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/women-empowerment")
def women():
    return render_template(
        "public/standard.html",
        eyebrow="Women Empowerment",
        title="Women Empowerment",
        body="Verified programme information will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/skill-development")
def skills():
    return render_template(
        "public/standard.html",
        eyebrow="Skill Development",
        title="Skill Development",
        body="Training details will be updated by the organization.",
    )


@public_bp.get("/livelihood-development")
def livelihood():
    return render_template(
        "public/standard.html",
        eyebrow="Livelihood Development",
        title="Livelihood Development",
        body="Verified livelihood programme information will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/handicrafts")
def handicrafts():
    return render_template(
        "public/standard.html",
        eyebrow="Handicrafts & Handlooms",
        title="Handicrafts & Handlooms",
        body="Verified craft and artisan programme information will be published after GSSKS provides and approves it.",
    )


@public_bp.get("/projects")
def projects():
    projects = (
        Project.query.filter_by(published=True)
        .order_by(Project.created_at.desc())
        .all()
    )
    return render_template("public/projects.html", projects=projects)




@public_bp.get("/gallery")
def gallery():
    items = (
        GalleryItem.query.filter_by(published=True)
        .order_by(GalleryItem.sort_order, GalleryItem.event_date.desc().nullslast())
        .all()
    )
    return render_template("public/gallery.html", items=items)


@public_bp.get("/news-events")
def news_events():
    posts = (
        BlogPost.query.filter_by(published=True)
        .order_by(BlogPost.created_at.desc())
        .limit(6)
        .all()
    )
    events = Event.query.order_by(Event.event_date.desc().nullslast()).limit(6).all()
    return render_template("public/news_events.html", posts=posts, events=events)


@public_bp.get("/get-involved")
def get_involved():
    return render_template("public/get_involved.html")


@public_bp.get("/projects/gandhi-shilp-bazaar-2024")
def gandhi_shilp_bazaar():
    return render_template("public/gandhi_shilp_bazaar.html")


@public_bp.get("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template("public/project_detail.html", project=project)


@public_bp.get("/events")
def events():
    events = Event.query.order_by(Event.event_date.asc().nullslast()).all()
    return render_template("public/events.html", events=events)


@public_bp.get("/blog")
def blog():
    posts = (
        BlogPost.query.filter_by(published=True)
        .order_by(BlogPost.created_at.desc())
        .all()
    )
    return render_template("public/blog.html", posts=posts)


@public_bp.get("/impact")
def impact():
    stats = (
        ImpactStatistic.query.filter_by(published=True)
        .order_by(ImpactStatistic.sort_order)
        .all()
    )
    return render_template("public/impact.html", stats=stats)


@public_bp.get("/reports")
def reports():
    documents = (
        Document.query.filter_by(visibility="public")
        .order_by(Document.year.desc().nullslast())
        .all()
    )
    return render_template("public/reports.html", documents=documents)


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("Enter a valid email address.", "error")
            return render_template("public/contact.html")

        if not name or not message:
            flash("Name and message are required.", "error")
        else:
            db.session.add(
                ContactMessage(
                    name=name,
                    email=email,
                    phone=request.form.get("phone", ""),
                    subject=request.form.get("subject", ""),
                    message=message,
                )
            )
            db.session.commit()
            flash("Your message has been received.", "success")
            return redirect(url_for("public.contact"))

    return render_template("public/contact.html")


@public_bp.get("/api/health")
def health():
    database = "ok"
    try:
        db.session.execute(text("SELECT 1"))
    except Exception as exc:
        db.session.rollback()
        database = f"error: {type(exc).__name__}"

    return jsonify(
        ok=database == "ok",
        service="gyanpath",
        database=database,
        vercel=bool(__import__("os").getenv("VERCEL") or __import__("os").getenv("VERCEL_ENV")),
    ), (200 if database == "ok" else 503)


@public_bp.get("/api/debug")
def debug():
    """Deployment diagnostics for Vercel/Render. Does not expose secrets."""
    import os
    result = {
        "vercel": bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV")),
        "database_url_configured": bool(os.getenv("DATABASE_URL")),
        "database": "ok",
    }
    try:
        db.session.execute(text("SELECT 1"))
    except Exception as exc:
        db.session.rollback()
        result["database"] = f"error: {type(exc).__name__}: {exc}"

    try:
        render_template(
            "public/home.html",
            projects=[],
            events=[],
            stats=[],
            gallery=[],
        )
        result["home_template"] = "ok"
    except Exception as exc:
        result["home_template"] = f"error: {type(exc).__name__}: {exc}"

    return jsonify(result)


@public_bp.get("/api/projects")
def api_projects():
    projects = Project.query.filter_by(published=True).all()
    return jsonify(
        items=[
            {
                "title": project.title,
                "slug": project.slug,
                "category": project.category,
                "status": project.status,
            }
            for project in projects
        ]
    )


@public_bp.get("/robots.txt")
def robots():
    return "User-agent: *\nAllow: /\nSitemap: " + url_for("public.sitemap", _external=True), 200, {"Content-Type": "text/plain; charset=utf-8"}


@public_bp.get("/sitemap.xml")
def sitemap():
    urls = [
        url_for("public.home", _external=True),
        url_for("public.about", _external=True),
        url_for("public.icps", _external=True),
        url_for("public.work", _external=True),
        url_for("public.recognition", _external=True),
        url_for("public.projects", _external=True),
        url_for("public.impact", _external=True),
        url_for("public.gallery", _external=True),
        url_for("public.news_events", _external=True),
        url_for("public.get_involved", _external=True),
        url_for("public.reports", _external=True),
        url_for("public.contact", _external=True),
        url_for("public.gandhi_shilp_bazaar", _external=True),
    ]
    body = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>"
    return body, 200, {"Content-Type": "application/xml; charset=utf-8"}
