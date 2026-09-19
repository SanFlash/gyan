from app import create_app, db
from app.models import User
app=create_app({"TESTING":True})
with app.app_context():
    db.create_all(); print("Database OK; users:",User.query.count())
with app.test_client() as c:
    for path in ["/","/about","/projects","/events","/contact","/login"]:
        r=c.get(path); print(path,r.status_code)
