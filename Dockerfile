FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /test

COPY ./requirements.txt /test/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt

COPY . /test

EXPOSE 8000
