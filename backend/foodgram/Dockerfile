FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000" ]
