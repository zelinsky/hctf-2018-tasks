FROM python:3

WORKDIR /usr/src/app

ADD app ./
ADD flag.txt /opt/
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -U gunicorn
CMD gunicorn -b 0.0.0.0:8000 -u gunicorn -g gunicorn wsgi:app
