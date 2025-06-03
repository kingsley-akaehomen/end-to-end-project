FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x /app/wait-for-it.sh

CMD uvicorn time-api:app --host=0.0.0.0 --reload
