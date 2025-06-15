FROM python:3.11-slim-buster

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY agent-development-461516-6af08ba7b1eb.json /app/key.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"

EXPOSE 8080

# Change this for debugging instead of running the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--graceful-timeout", "30", "--timeout", "60"]
