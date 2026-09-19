# Gyanpath NGO — Fixed Responsive Build

## Local
The app automatically uses SQLite at `instance/gyanpath.db` when `DATABASE_URL` is not set. The database is created on startup and a local demo admin is created automatically.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

### Local admin
- Email: `admin.demo@gyanpath.local`
- Password: `Gyanpath@Demo2026!`

## Production
Set `DATABASE_URL` to managed PostgreSQL and `SECRET_KEY` to a strong secret. Render binds Gunicorn to `0.0.0.0:$PORT`, making the deployed site publicly reachable. Production disables demo-user seeding.

## Admin
`/admin/` supports project creation, editing, publishing/unpublishing and deletion, plus user and enquiry views. A published project appears on the public website.

## Responsive fixes
The latest build removes oversized padding, prevents horizontal overflow, adds a mobile menu, tightens grids/sections, and hides the 3D canvas for reduced-motion users.

## Content
Official organizational facts should be entered and verified by the organization. Placeholder wording is used where information is not available.
