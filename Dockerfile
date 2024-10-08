FROM python:3.9-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
