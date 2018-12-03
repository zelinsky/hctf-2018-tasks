FROM python:3

WORKDIR /usr/src/app

ADD app ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get -y install liblua5.1-0  # pandoc dependency
ADD pandoc.deb /tmp
RUN dpkg -i /tmp/pandoc.deb && rm /tmp/pandoc.deb
RUN useradd -U gunicorn
CMD gunicorn -b 0.0.0.0:8000 -u gunicorn -g gunicorn wsgi:app
