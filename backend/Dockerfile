FROM python:3.10.6-slim

RUN mkdir /app

WORKDIR /app

COPY . ./

RUN pip3 install -r ./requirements.txt --no-cache-dir

CMD [ "gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]