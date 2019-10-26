  
release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn expense_tracker.wsgi
