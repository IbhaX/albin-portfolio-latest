# IBHAX Django Application
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ibhax.settings
ENV DB_PATH=/app/data/db.sqlite3

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Create directories for static files, media, and database
RUN mkdir -p /app/staticfiles /app/media /app/data

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run entrypoint
CMD ["/app/entrypoint.sh"]
