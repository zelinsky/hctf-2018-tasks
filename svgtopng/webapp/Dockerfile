FROM python:3

WORKDIR /usr/src/app

ADD app ./
RUN pip install --no-cache-dir -r requirements.txt
COPY flag.txt /opt/key.txt
RUN useradd -U gunicorn
CMD gunicorn -b 0.0.0.0:8000 -u gunicorn -g gunicorn wsgi:app
