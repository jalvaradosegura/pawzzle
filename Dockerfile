FROM python:slim

ARG DB_CONNECTION_URL
ARG DOGS_FILE

WORKDIR /app
COPY requirements.lock ./
RUN sed -i '/-e file:./d' requirements.lock
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

ENV DB_CONNECTION_URL=$DB_CONNECTION_URL
ENV DOGS_FILE=$DOGS_FILE

EXPOSE 80

COPY src .
CMD ["fastapi", "run", "pawzzle/main.py", "--port", "80"]
