#!/bin/bash
echo "========================================"
echo "IBHAX Django Setup Script"
echo "========================================"
echo
echo "[1/3] Migrating database..."
python manage.py makemigrations accounts
python manage.py makemigrations pages
python manage.py makemigrations blog
python manage.py makemigrations comments
python manage.py makemigrations portfolio
python manage.py makemigrations moderation
python manage.py migrate

echo
echo "[2/3] Loading initial data from profile.json..."
python manage.py shell -c "exec(open('scripts/load_initial_data.py').read())"

echo
echo "[3/3] Creating superuser..."
python manage.py shell -c "exec(open('scripts/create_superuser.py').read())"

echo
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo
echo "Admin login:"
echo "  URL: http://127.0.0.1:8000/admin/"
echo "  Username: admin"
echo "  Password: admin123 (change this!)"
echo
