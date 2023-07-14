# Stage 1: Build stage
FROM python:3.10 AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Runtime stage
FROM python:3.10
WORKDIR /app
COPY --from=build /app /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/*
CMD ["python", "main.py"]
