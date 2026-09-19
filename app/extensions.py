from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db=SQLAlchemy()
login_manager=LoginManager()
migrate=Migrate()
csrf=CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    try: return db.session.get(User,int(user_id))
    except (TypeError,ValueError): return None
