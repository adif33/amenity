FROM python:3.8

RUN apt-get update && apt-get install net-tools
COPY /requierments /code/requierments
COPY /src /code/src
COPY /api /code/api
COPY /common /code/common
RUN touch /code/__init__.py
RUN pip install -r /code/requierments
