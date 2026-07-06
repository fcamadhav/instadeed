FROM python:3.11-slim

# Create a non-root user with an explicit UID
RUN groupadd -r app -g 10001 && useradd -r -g app -u 10001 app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Secure permissions
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["python", "server.py"]
