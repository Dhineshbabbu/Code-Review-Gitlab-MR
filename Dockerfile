FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENV GOOGLE_APPLICATION_CREDENTIALS="agent-development-461516-c58cccfe9b84.json"
CMD ["python", "app.py"]
