# pull official base image
FROM python:3.11.4

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY src .
COPY config.ini.docker ./config.ini

CMD ["uwsgi", "--ini", "wsgi.ini"]
