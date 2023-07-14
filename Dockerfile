# Stage 1: Build stage
FROM python:3.10 AS build
WORKDIR /app
COPY requirements.txt .
# Check pip version
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt
# Check pip version
RUN pip --version
COPY . .

# Stage 2: Runtime stage
FROM python:3.10
WORKDIR /app
COPY --from=build /app /app
# Check pip version
RUN pip --version
RUN apt-get update && \
    apt-get install -y --no-install-recommends sqlite3 && \
    rm -rf /var/lib/apt/lists/* \
# Check pip version
RUN pip --version
CMD ["python", "main.py"]
