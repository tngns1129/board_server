# pull official base image
FROM python:3.12-rc-slim-buster

#set environment variables
# I don't want to generate pcy files
ENV PYTHONDONTWRITEBYTECODE 1
# ignore buffering
ENV PYTHONUNBUFFERED 1
# set encoding
ENV PYTHONENCODING utf-8

#set work directory
WORKDIR /workdir

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# for mysql, django의 DB로 msyql을 사용하지 않는다면 굳이 필요없다.
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc libffi-dev -y

# 배포할 경우 프로젝트 코드를 모두 도커 이미지에 넣는다.
COPY . /workdir/src

# python dependencies
RUN pip install --upgrade pip
RUN pip install django
RUN pip install gunicorn
RUN pip install -r /workdir/src/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]