# IBHAX - Portfolio & Blog Platform

A modern Django-based portfolio and blog platform with real-time features, built for freelance developers and agencies.

## Features

- **Portfolio Showcase** - Personal and company project galleries
- **Blog System** - SEO-friendly URLs, threaded comments, moderation workflow
- **User Management** - Role-based permissions (Admin, Moderator, Member)
- **Real-time Logs** - WebSocket-powered admin log viewer (Mac terminal style)
- **Notifications** - Real-time notifications for posts, comments, and replies
- **Modern UI** - Tailwind CSS with dark theme, responsive design
- **WYSIWYG Editor** - TinyMCE integration for rich content editing

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/ibhax.git
cd ibhax

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run setup script
./setup.sh

# Start development server
python manage.py runserver
```

### Docker Deployment

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (insecure default) |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `TINYMCE_API_KEY` | TinyMCE editor API key | `no-api-key` |
| `DB_PATH` | SQLite database path | `db.sqlite3` |

## Project Structure

```
ibhax/
├── accounts/       # User authentication & profiles
├── blog/           # Blog posts, categories, tags
├── comments/       # Threaded comments (MPTT)
├── moderation/     # Content moderation tools
├── notifications/  # Real-time notifications
├── pages/          # Static pages, contact form
├── portfolio/      # Personal & company projects
├── templates/      # HTML templates
├── static/         # Static assets
└── ibhax/          # Project settings
```

## Admin Access

After running setup:
- **URL**: http://localhost:8000/admin/
- **Username**: `admin`
- **Password**: `admin123` (change in production!)

## Tech Stack

- **Backend**: Django 4.2, Django Channels (WebSocket)
- **Database**: SQLite (PostgreSQL ready)
- **Frontend**: Tailwind CSS, Alpine.js, HTMX
- **Server**: Daphne (ASGI)
- **Editor**: TinyMCE

## License

MIT License - See LICENSE file for details.

---

Built with ❤️ by [IBHAX](https://ibhax.com)
