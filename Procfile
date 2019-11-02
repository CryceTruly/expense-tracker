  
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput

web: gunicorn expense_tracker.wsgi
