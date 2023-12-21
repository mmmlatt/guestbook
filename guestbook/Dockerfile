# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /guestbook

# Copy the current directory contents into the container at /app
COPY . /guestbook

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Define environment variables
ENV SECRET_KEY=${SECRET_KEY}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV DJANGO_SETTINGS_MODULE=guestbook.settings

# Collect static files
RUN python manage.py collectstatic --noinput

# Migrate db, seems to want to migrate the app separately
RUN python manage.py makemigrations
RUN python manage.py makemigrations guestbookapp

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "guestbook.wsgi:application"]