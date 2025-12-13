#!/bin/bash
set -e

echo "=========================================="
echo "IBHAX Django Application Starting..."
echo "=========================================="

# Wait for any dependent services (future-proofing for PostgreSQL)
# sleep 2

# Run migrations
echo "[1/3] Running database migrations..."
python manage.py migrate --noinput

# Load initial data if needed
echo "[2/3] Loading initial data..."
python manage.py shell -c "
from pages.models import SiteSettings
from accounts.models import User

# Ensure site settings exist
SiteSettings.load()

# Create superuser if none exists
if not User.objects.filter(is_superuser=True).exists():
    user = User.objects.create_superuser('admin', 'admin@ibhax.com', 'admin123')
    user.is_member = True
    user.role = 'admin'
    user.save()
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
" 2>/dev/null || echo "Initial data loading skipped"

echo "[3/3] Starting server..."
echo "=========================================="
echo "Server running at http://0.0.0.0:8000"
echo "=========================================="

# Start server with Daphne for WebSocket support
exec daphne -b 0.0.0.0 -p 8000 ibhax.asgi:application
