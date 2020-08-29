FROM python:3.6-slim

RUN pip install --upgrade requests lxml

WORKDIR /app
COPY ./ /app/

ENTRYPOINT ["python", "-u", "/app/run.py"]