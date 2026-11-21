# Gyanpath NGO Platform

Premium, responsive Flask NGO website and local administration workspace for **Gyanpath Shiksha Evam Samaj Kalyan Samiti, Bhopal, Madhya Pradesh**.

## Included
- Premium responsive navbar, footer and mobile navigation
- Animated hero with optional lightweight Three.js 3D scene
- Education, women empowerment, skill development, livelihood and craft programme pages
- Projects and project publishing workflow
- Events and public registration
- Volunteer applications
- Support/donation request capture with production payment gateway extension point
- Artisans
- News/blog
- Impact statistics
- Public reports/documents
- Contact/enquiry inbox
- Customer accounts
- Role-protected admin workspace
- Admin CRUD for projects, events, artisans, news and impact statistics
- Admin views for users, volunteers, donations, enquiries and documents
- Site settings
- SQLite local development and PostgreSQL production
- Render/Gunicorn configuration
- CSRF-protected forms
- Responsive and reduced-motion support
- Public JSON health and project endpoints

## Local development

Python 3.13.x:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

SQLite is automatically used when `DATABASE_URL` is not set.

### Local demo admin

```
Email: admin.demo@gyanpath.local
Password: Gyanpath@Demo2026!
```

Admin: `/admin/`

## Production

Use managed PostgreSQL and set:

```
SECRET_KEY=<strong-random-secret>
DATABASE_URL=<postgresql-connection-string>
AUTO_INIT_DB=true
AUTO_SEED_DEMO=false
SESSION_COOKIE_SECURE=true
```

Render uses Gunicorn on `0.0.0.0:$PORT`.

## Content safety

The project deliberately does not invent registration numbers, beneficiaries, impact totals, government partnerships, CSR partners or other official facts. Add verified information through the admin workspace.

## Payment

The current support form safely records support requests. Razorpay can be enabled after adding production credentials and implementing the server-side order/signature verification flow; do not expose secret keys in frontend code.

## Security

Never deploy the demo password. Use a strong `SECRET_KEY`, HTTPS, managed PostgreSQL, backups, rate limiting and production email/payment credentials.


## Media library (photos and videos)

The admin workspace includes a dedicated **Media Library** at `/admin/media`. It stores media metadata in the configured SQL database and stores original files in a media object store.

### Recommended production storage: Cloudinary Free

1. Create a free Cloudinary account at https://cloudinary.com/users/register/free.
2. In the Cloudinary Console, copy the cloud name, API key and API secret.
3. Add these as environment variables to the Render service (do not commit secrets to GitHub):

```
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
MAX_CONTENT_LENGTH=262144000
```

4. Redeploy the Render service.
5. Sign in to the GSSKS admin workspace, open **Media Library**, upload a photo or video, add its title and description, and publish it when approved.

Images and videos are uploaded to separate `gyanpath/media/photos` and `gyanpath/media/videos` folders. Videos use chunked uploads. The database stores the asset URL, type, MIME type, dimensions, duration, byte size, provider and publication state. The public Gallery page displays only published media. Existing Gallery photographs and Documents remain supported.

Cloudinary's free tier has a monthly credit allowance shared across storage, transformations and delivery bandwidth; it is not unlimited storage. Monitor usage in the Cloudinary Console and upgrade or move to another object-storage provider if usage grows.

### Local development

When Cloudinary credentials are absent outside production, media files can be stored under the Flask instance media directory and served by the local development route. This local filesystem is for development only. Render free services have ephemeral filesystems, so production uploads are deliberately blocked until Cloudinary credentials are configured. Never rely on local uploads for production persistence.

### Media publishing and privacy

Only publish media approved by GSSKS. Obtain appropriate consent before publishing identifiable people, especially children. Draft items are excluded from the public gallery.
