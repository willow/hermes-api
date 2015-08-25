# -u forces to run unbuffered: http://python-rq.org/patterns/
web: python -u `which gunicorn` -c gunicorn.py.ini wsgi:application
worker: python -u manage.py rqworker high default
