FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENV FLASK_ENV=production
CMD ["python", "app.py"]
