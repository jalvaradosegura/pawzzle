FROM python:slim

ARG DB_CONNECTION_URL
ARG DOGS_FILE
ARG API_KEY

WORKDIR /app
COPY requirements.lock ./
RUN sed -i '/-e file:./d' requirements.lock
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

ENV DB_CONNECTION_URL=$DB_CONNECTION_URL
ENV DOGS_FILE=$DOGS_FILE
ENV API_KEY=$API_KEY

COPY src .

COPY alembic ./alembic
COPY alembic.ini .
RUN alembic upgrade heads || echo "Migration failed or already applied"

EXPOSE 80

CMD ["fastapi", "run", "pawzzle/main.py", "--port", "80"]
