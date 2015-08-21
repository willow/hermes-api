web: gunicorn -c gunicorn.py.ini wsgi:application

worker: python manage.py rqworker high default
