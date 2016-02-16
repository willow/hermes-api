# -u forces to run unbuffered: http://python-rq.org/patterns/
# http://stackoverflow.com/questions/12634447/running-heroku-background-tasks-with-only-1-web-dyno-and-0-worker-dynos
web: python -u `which gunicorn` -c gunicorn.py.ini wsgi:application
worker: bin/worker
