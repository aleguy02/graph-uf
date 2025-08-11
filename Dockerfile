FROM python:3.13-slim

WORKDIR /graphuf

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app/ app/
COPY src/ src/

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
