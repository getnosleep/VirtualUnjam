FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /microservice
COPY requirements.txt /microservice/requirements.txt
RUN python -m pip install -r requirements.txt
COPY . /microservice

CMD 'python manage.py runserver'