from flask import Blueprint, abort, render_template
from .extensions import db
from .models import Event

events_bp = Blueprint("events_detail", __name__)


@events_bp.get("/events/<int:event_id>")
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        abort(404)
    return render_template("public/event_detail.html", event=event)
