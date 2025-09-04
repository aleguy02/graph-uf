FROM python:3.13-slim

WORKDIR /graphuf

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ app/
COPY src/ src/

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]

EXPOSE 3000
