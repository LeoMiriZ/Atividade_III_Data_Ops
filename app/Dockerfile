FROM python:3.12-slim

WORKDIR /app

COPY script_api.py .

RUN pip install psycopg2-binary flask flask-restx gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:80", "script_api:app"]