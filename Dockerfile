FROM python:3.11.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade -r requirements.txt
RUN pip install alembic
CMD ["alembic", "upgrade", "head"]

