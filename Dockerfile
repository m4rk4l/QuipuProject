FROM python:3.8-slim

WORKDIR /app
ADD . .
RUN pip install pipenv && pipenv install --system --deploy

# ENTRYPOINT /bin/bash
# running migrate because we only have a local db.
# FIXME:
# This only works through non http connections
ENTRYPOINT ./manage.py migrate && ./manage.py collectstatic && gunicorn -c conf/settings/gunicorn.py conf.wsgi:application
