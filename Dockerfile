FROM python:3

MAINTAINER hi@michaelerasm.us

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system

ENTRYPOINT ["stripe-pipeline"]
