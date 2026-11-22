from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
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
    MediaAsset,
)

public_bp = Blueprint("public", __name__)


def _page_sections(placement):
    """Return published CMS blocks for a page without breaking public rendering."""
    try:
        return SiteSection.query.filter_by(placement=placement, published=True).order_by(
            SiteSection.sort_order, SiteSection.id
        ).all()
    except Exception:
        db.session.rollback()
        return []


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
            Event.query.order_by(Event.event_date.desc().nullslast())
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
            {"value": "1992", "label": "Year GSSKS was established"},
            {"value": "4", "label": "Open Shelter Home units listed in Bhopal"},
            {"value": "50", "label": "Artisans at Gandhi Shilp Bazaar 2024"},
            {"value": "₹14.95L+", "label": "Reported sales at Gandhi Shilp Bazaar 2024"},
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
    return render_template("public/about.html", sections=_page_sections("about"))


@public_bp.get("/mission")
def mission():
    return render_template(
        "public/standard.html",
        eyebrow="Mission",
        title="Mission statement",
        body="""GSSKS works to provide care, protection and meaningful opportunities for children in need of care and protection. Its programme approach brings together safe shelter, nutrition, education, health support, counselling, recreation, vocational exposure and family reintegration. The work also recognises the wider circumstances affecting families in Bhopal’s gas-affected communities and the importance of connecting children with appropriate care and protection systems.\n\nThe organisation’s practical focus is to help children access safety, dignity, learning and support while strengthening the relationships and systems that contribute to their wellbeing.""",
    )


@public_bp.get("/vision")
def vision():
    return render_template(
        "public/standard.html",
        eyebrow="Vision",
        title="Vision statement",
        body="""A future in which children can grow up with safety, dignity, opportunity and the support they need to realise their potential. GSSKS’s work is directed towards stronger child-protection systems, supportive communities and access to care, learning and rehabilitation for children facing vulnerable circumstances.\n\nThis long-term direction is reflected in the organisation’s focus on child-first care, equality, inclusion, compassion, integrity and partnership.""",
    )


@public_bp.get("/work")
def work():
    return render_template("public/work.html", sections=_page_sections("work"))


@public_bp.get("/icps")
def icps():
    return render_template("public/icps.html", sections=_page_sections("icps"))


@public_bp.get("/open-shelter-home")
def open_shelter_home():
    return render_template("public/open_shelter_home.html",
                           sections=_page_sections("shelter_home"))


@public_bp.get("/education")
def education():
    return render_template(
        "public/standard.html",
        eyebrow="Education",
        title="Education",
        body="""Education is integrated into GSSKS’s Open Shelter Home programme as a practical pathway to stability, confidence and future opportunity. Support described across the programme includes assistance with government-school admission, basic literacy, bridge education, remedial learning, tuition and study support, textbooks and stationery, annual examinations, and computer or digital learning.\n\nLearning support is complemented by educational visits and activities that allow children to explore local heritage, participate in group experiences and connect classroom learning with the world around them. The programme also includes age-appropriate vocational exposure and basic computer training for adolescents.""",
    )


@public_bp.get("/women-empowerment")
def women():
    return render_template(
        "public/standard.html",
        eyebrow="Women Empowerment",
        title="Women Empowerment",
        body="""GSSKS’s child-centred approach recognises that children’s wellbeing is closely connected with the stability and support available to their families. The organisation’s programme information describes family counselling, restoration efforts, follow-up after restoration and community outreach as part of its wider care and protection work.\n\nThese activities are intended to strengthen supportive relationships around children and help connect families with appropriate guidance and child-protection processes. GSSKS also works within the broader framework of the Department of Women and Child Development and child-protection institutions. The focus of this page is family and community support; no separate women-only training or beneficiary programme is represented here.""",
    )


@public_bp.get("/skill-development")
def skills():
    return render_template(
        "public/standard.html",
        eyebrow="Skill Development",
        title="Skill Development",
        body="""Skill development is part of the Open Shelter Home programme’s preparation for children’s future independence. Programme activities include computer learning and, particularly for adolescents aged 14–17, exposure to crafts or trade skills, career guidance and pre-employment training. The 2024–25 activity record also includes employment-oriented training for children.\n\nThe approach combines practical learning with life-skills development, value education, communication, confidence-building and guidance. These experiences are intended to help young people recognise their interests and prepare for further education, training and livelihood pathways. Specific course titles and certification claims are not stated.""",
    )


@public_bp.get("/livelihood-development")
def livelihood():
    return render_template(
        "public/standard.html",
        eyebrow="Livelihood Development",
        title="Livelihood Development",
        body="""GSSKS’s documented livelihood-related initiative includes the Gandhi Shilp Bazaar exhibition held at Urban Haat, Gauhar Mahal, Bhopal, from 11 to 17 September 2024. The seven-day programme brought 50 artisans before the public and showcased traditional products and craft practices. Reported sales during the exhibition exceeded ₹14,95,577.\n\nThe initiative created a platform for artisans to display their work, interact with visitors and generate sales. It demonstrates GSSKS’s engagement with artisan visibility and market access alongside its core child-protection and social-development work.""",
    )


@public_bp.get("/handicrafts")
def handicrafts():
    return render_template(
        "public/standard.html",
        eyebrow="Handicrafts & Handlooms",
        title="Handicrafts & Handlooms",
        body="""GSSKS’s artisan and craft initiative is represented by the Gandhi Shilp Bazaar 2024 exhibition, held from 11 to 17 September at Urban Haat, Gauhar Mahal, Bhopal, under the MSS of the Ministry of Textiles, Government of India. The seven-day exhibition included 50 artisans and attracted members of the general public.\n\nThe displayed range included jute products, Assam bamboo products, dry-stone work, handmade bedsheets, Madhubani paintings, silk sarees, jute and POP pottery, patchwork, zari work, paintings and woollen or fibre-yarn crafts. Reported sales exceeded ₹14,95,577. The programme provided artisans with a public exhibition setting to present their products and connect with potential buyers.""",
    )


@public_bp.get("/projects")
def projects():
    projects = (
        Project.query.filter_by(published=True)
        .order_by(Project.created_at.desc())
        .all()
    )
    return render_template("public/projects.html", projects=projects, sections=_page_sections("projects"))




@public_bp.get("/gallery")
def gallery():
    items = (
        GalleryItem.query.filter_by(published=True)
        .order_by(GalleryItem.sort_order, GalleryItem.event_date.desc().nullslast())
        .all()
    )
    media = MediaAsset.query.filter_by(published=True).order_by(
        MediaAsset.sort_order, MediaAsset.created_at.desc()
    ).all()
    return render_template("public/gallery.html", items=items, media=media)


@public_bp.get("/local-media/<path:filename>")
def local_media(filename):
    """Serve local-only development uploads; production media uses Cloudinary."""
    import os
    from werkzeug.utils import safe_join
    media_dir = os.path.join(current_app.instance_path, "media")
    target = safe_join(media_dir, filename)
    if not target or not os.path.isfile(target):
        return "", 404
    return send_from_directory(media_dir, filename, conditional=True)


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
    return render_template("public/impact.html", stats=stats, sections=_page_sections("impact"))


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


@public_bp.get("/api/chat")
def ngo_chat():
    """Answer common GSSKS questions from verified public website information."""
    import re

    question = (request.args.get("q") or "").strip()
    if not question:
        return jsonify(error="Please enter a question."), 400
    if len(question) > 500:
        return jsonify(error="Please keep your question under 500 characters."), 400

    normal = re.sub(r"[^a-z0-9\s]", " ", question.lower())
    normal = re.sub(r"\s+", " ", normal).strip()
    words = set(normal.split())
    # Common Hindi/Hinglish words mapped to the same intent vocabulary.
    hinglish_aliases = {
        "kaun": "founder", "kaunse": "which", "kab": "year",
        "kahan": "location", "kidhar": "location", "pata": "address",
        "sampark": "contact", "baat": "contact", "phone": "phone",
        "madad": "support", "sahayata": "support", "help": "support",
        "bachche": "children", "bache": "children", "bacchon": "children",
        "padhai": "education", "school": "education", "swasthya": "health",
        "ilaaj": "medical", "dawai": "medicine", "daan": "donation",
        "shuru": "started", "sanstha": "organisation", "sangathan": "organisation",
        "kaam": "work", "seva": "services", "suvidha": "facilities",
        "karyakram": "programme", "yojana": "scheme", "umar": "age",
        "kitni": "how", "kitne": "how", "kaise": "how",
    }
    words.update(hinglish_aliases[token] for token in list(words) if token in hinglish_aliases)

    entries = [
        {
            "keys": ["hello", "hi", "hey", "namaste", "good morning", "good evening"],
            "terms": {"hello", "hi", "hey", "namaste", "morning", "evening"},
            "answer": "Hello! Welcome to Gyan Path Shiksha Evam Samaj Kalyan Samiti (GSSKS). I can help with information about our organisation, Open Shelter Homes, child protection services, locations, and ways to connect with us.",
            "suggestions": ["About GSSKS", "Open Shelter Home", "Contact details"]
        },
        {
            "keys": ["about", "organisation", "organization", "ngo", "gyan path", "gssks"],
            "terms": {"about", "organisation", "organization", "ngo", "gssks", "gyan", "path", "samiti"},
            "answer": "Gyan Path Shiksha Evam Samaj Kalyan Samiti (GSSKS) is a non-governmental organisation based in Bhopal, Madhya Pradesh. Established in 1992 and registered under No. 1262/92, GSSKS works in child protection, education, health, rehabilitation and community support, with particular attention to communities affected by the Bhopal Gas Tragedy.",
            "suggestions": ["Our work", "Open Shelter Home", "Contact details"]
        },
        {
            "keys": ["established", "founded", "started", "registration", "registered", "year"],
            "terms": {"established", "founded", "started", "registration", "registered", "year", "number", "1262"},
            "answer": "GSSKS was established in 1992. Its society registration number is 1262/92, dated 4 September 1992, under the Madhya Pradesh Society Registration Act, 1973.",
            "suggestions": ["About GSSKS", "Contact details"]
        },
        {
            "keys": ["founder", "director", "who leads", "leadership"],
            "terms": {"founder", "director", "leads", "leadership", "ishwar", "chauhan"},
            "answer": "The organisation's founder is Ishwar Singh Chouhan, also referred to as I. S. Chauhan.",
            "suggestions": ["About GSSKS", "Contact details"]
        },
        {
            "keys": ["mission", "vision", "aim", "objective", "purpose"],
            "terms": {"mission", "vision", "aim", "objective", "purpose", "goal"},
            "answer": "GSSKS's work focuses on care, protection and opportunities for children in need, strengthening child-protection systems, and supporting families and communities affected by the Bhopal Gas Tragedy.",
            "suggestions": ["Our work", "Child protection services"]
        },
        {
            "keys": ["open shelter", "shelter home", "boys home", "shelter"],
            "terms": {"open", "shelter", "home", "homes", "boys", "centre", "centres", "center", "centers"},
            "answer": "GSSKS's Open Shelter Home programme provides day-long care and support for children in need of care and protection. The programme combines safe care, meals, education, health support, counselling, recreation, life skills and family reintegration. Four units are listed in Bhopal. Read more at /open-shelter-home.",
            "suggestions": ["Age group", "Shelter locations", "Facilities and services"]
        },
        {
            "keys": ["age", "ages", "children age", "how old"],
            "terms": {"age", "ages", "old", "children", "child", "6", "17"},
            "answer": "The Open Shelter Home programme information describes support for children and adolescents aged 6 to 17 years.",
            "suggestions": ["Open Shelter Home", "Facilities and services"]
        },
        {
            "keys": ["service", "services", "facilities", "provide", "support", "what do you do"],
            "terms": {"service", "services", "facilities", "provide", "support", "care", "education", "health", "food", "counselling", "counseling"},
            "answer": "The Open Shelter Home programme includes safe accommodation and daily care, nutritious meals and essentials, school and bridge-learning support, computer learning, medical check-ups and immunisation, counselling and life skills, sports and cultural activities, vocational exposure for adolescents, family counselling and restoration follow-up.",
            "suggestions": ["Education support", "Health and counselling", "Vocational training"]
        },
        {
            "keys": ["education", "school", "study", "computer classes", "learning"],
            "terms": {"education", "school", "study", "computer", "classes", "learning", "literacy", "tuition"},
            "answer": "Education support includes school admission assistance, basic literacy, bridge education, remedial learning, study support, textbooks and stationery, and computer or digital learning.",
            "suggestions": ["Open Shelter Home", "Other services"]
        },
        {
            "keys": ["health", "medical", "doctor", "medicine", "vaccination", "immunisation", "immunization"],
            "terms": {"health", "medical", "doctor", "medicine", "vaccination", "immunisation", "immunization", "first", "aid"},
            "answer": "Health and wellbeing support described by GSSKS includes routine medical check-ups, immunisation, first-aid support, nutrition, physical fitness and sports.",
            "suggestions": ["Open Shelter Home", "Other services"]
        },
        {
            "keys": ["counselling", "counseling", "mental", "emotional", "trauma", "psychologist"],
            "terms": {"counselling", "counseling", "mental", "emotional", "trauma", "psychologist", "stress"},
            "answer": "The programme includes individual and group counselling, emotional support, trauma care, behaviour management, life-skills learning and stress-management support.",
            "suggestions": ["Open Shelter Home", "Health and wellbeing"]
        },
        {
            "keys": ["location", "address", "where", "centres", "centers", "branches"],
            "terms": {"location", "address", "where", "centres", "centers", "branches", "bhopal", "chhola", "pushpa", "nagar"},
            "answer": "Four Open Shelter Home locations are listed in Bhopal: Unit 1 — H.No. 1740, Block A, Ground Floor, Sundar Nagar, Chhola Road; Unit 2 — H.No. C-537, 538, Pushpa Nagar, Railway Station Road; Unit 3 — H.No. 1741, Sundar Nagar, Chhola Road; Unit 4 — H.No. 1740, Block B, First Floor, Sundar Nagar, Chhola Road. Please contact GSSKS before visiting to confirm current centre operations and visiting arrangements.",
            "suggestions": ["Contact details", "Open Shelter Home"]
        },
        {
            "keys": ["contact", "phone", "mobile", "email", "call", "whatsapp"],
            "terms": {"contact", "phone", "mobile", "email", "call", "whatsapp", "reach", "number"},
            "answer": "You can contact GSSKS at 0755-4278487 or by email at gyanpathngo.176@gmail.com. The website also lists mobile numbers 088893937454 and 09826366176. Visit the Contact page for the address, map and enquiry form.",
            "suggestions": ["Contact page", "Organisation address"]
        },
        {
            "keys": ["volunteer", "volunteering", "join", "help", "contribute", "donate", "donation"],
            "terms": {"volunteer", "volunteering", "join", "help", "contribute", "donate", "donation", "support"},
            "answer": "Thank you for your interest in supporting GSSKS. Please use the Get Involved or Contact page to reach the organisation and discuss volunteering, contributions or other ways to help. The team can confirm current opportunities and the appropriate process.",
            "suggestions": ["Get Involved", "Contact details"]
        },
        {
            "keys": ["icps", "mission vatsalya", "juvenile justice", "child protection", "cwc", "jjb"],
            "terms": {"icps", "mission", "vatsalya", "juvenile", "justice", "child", "protection", "cwc", "jjb", "act"},
            "answer": "GSSKS's Open Shelter Home work is described within the Integrated Child Protection Scheme (ICPS), now under Mission Vatsalya, and the Juvenile Justice (Care and Protection of Children) Act, 2015, with Central Rules, 2016. The programme includes coordination with Child Welfare Committees (CWC) and Juvenile Justice Boards (JJB).",
            "suggestions": ["ICPS programme", "Open Shelter Home"]
        },
        {
            "keys": ["gandhi shilp bazaar", "artisan", "artisans", "handicraft"],
            "terms": {"gandhi", "shilp", "bazaar", "artisan", "artisans", "handicraft", "craft"},
            "answer": "GSSKS also highlights Gandhi Shilp Bazaar 2024, a seven-day artisan exhibition held at Urban Haat, Gauhar Mahal, Bhopal, from 11 to 17 September 2024. The initiative reported participation by 50 artisans and sales of more than ₹14.95 lakh.",
            "suggestions": ["Our projects", "Contact details"]
        },
        {
            "keys": ["timing", "opening hours", "visiting hours", "when can i visit", "office hours"],
            "terms": {"timing", "timings", "opening", "hours", "visiting", "visit", "office"},
            "answer": "Current public visiting hours are not listed on the website. Please call GSSKS at 0755-4278487 before visiting to confirm availability and arrangements.",
            "suggestions": ["Contact details", "Shelter locations"]
        },
    ]

    best = None
    best_score = 0
    for entry in entries:
        score = sum(2 for phrase in entry["keys"] if phrase in normal)
        score += sum(1 for term in entry["terms"] if term in words)
        if score > best_score:
            best, best_score = entry, score

    if best and best_score >= 2:
        related_links = [
            {"label": "About GSSKS", "url": "/about"},
            {"label": "Open Shelter Home", "url": "/open-shelter-home"},
            {"label": "Contact GSSKS", "url": "/contact"},
        ]
        if any(term in words for term in {"icps", "vatsalya", "juvenile", "cwc", "jjb"}):
            related_links = [
                {"label": "ICPS programme", "url": "/icps"},
                {"label": "Open Shelter Home", "url": "/open-shelter-home"},
                {"label": "Contact GSSKS", "url": "/contact"},
            ]
        elif any(term in words for term in {"volunteer", "volunteering", "donate", "donation", "contribute", "join"}):
            related_links = [
                {"label": "Get involved", "url": "/get-involved"},
                {"label": "Contact GSSKS", "url": "/contact"},
            ]
        elif any(term in words for term in {"project", "projects", "artisan", "artisans", "bazaar", "gandhi", "shilp"}):
            related_links = [
                {"label": "Our projects", "url": "/projects"},
                {"label": "Gandhi Shilp Bazaar", "url": "/projects/gandhi-shilp-bazaar-2024"},
                {"label": "Contact GSSKS", "url": "/contact"},
            ]
        elif any(term in words for term in {"address", "location", "where", "bhopal", "chhola", "pushpa", "nagar"}):
            related_links = [
                {"label": "Shelter locations", "url": "/open-shelter-home"},
                {"label": "Contact & map", "url": "/contact"},
            ]
        return jsonify(answer=best["answer"], suggestions=best["suggestions"], links=related_links)

    return jsonify(
        answer="I can help with GSSKS information about the organisation, Open Shelter Homes, child protection, education, health services, centre locations, contact details and ways to get involved. I may not have the answer to that specific question yet. Please contact the GSSKS team at 0755-4278487 or gyanpathngo.176@gmail.com for confirmation.",
        suggestions=["About GSSKS", "Open Shelter Home", "Contact details", "Get Involved"],
        links=[
            {"label": "About GSSKS", "url": "/about"},
            {"label": "Contact GSSKS", "url": "/contact"},
        ]
    )


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
        url_for("public.open_shelter_home", _external=True),
        url_for("public.work", _external=True),
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
