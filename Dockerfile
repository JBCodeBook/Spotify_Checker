FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies and SQLite
RUN apt-get update && apt-get install -y sqlite3 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
