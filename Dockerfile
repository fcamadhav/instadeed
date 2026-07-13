# Stage 1: Build the Next.js Landing Page
FROM node:20-alpine AS builder
WORKDIR /app
# Install dependencies
COPY landing/package*.json ./landing/
RUN cd landing && npm install
# Copy the rest of the landing page code and build
COPY landing/ ./landing/
RUN cd landing && npm run build

# Stage 2: Final Python Image
FROM python:3.11-slim

# Create a non-root user with an explicit UID
RUN groupadd -r app -g 10001 && useradd -r -g app -u 10001 app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Overwrite landing/out with the cleanly built one from builder
COPY --from=builder /app/landing/out /app/landing/out

# Secure permissions
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["python", "server.py"]
