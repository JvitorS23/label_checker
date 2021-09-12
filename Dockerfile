FROM python:3.7
MAINTAINER JvitorS23

ENV PYTHONUNBUFFERED=1

# Install system packages required by the application
RUN apt-get update --yes --quiet && \
	apt-get upgrade -y && \
	apt-get install --yes --quiet --no-install-recommends \
		build-essential \
		libpq-dev \
		libmariadbclient-dev \
		libjpeg62-turbo-dev \
		zlib1g-dev \
		libwebp-dev

RUN mkdir /app
WORKDIR /app
COPY ./app /app

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static





